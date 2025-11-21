# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Unified Azure Management Client."""

import importlib
from typing import Any, Dict, Optional, TYPE_CHECKING
from azure.core.credentials import TokenCredential
from azure.mgmt.core import ARMPipelineClient
from azure.mgmt.core.policies import ARMChallengeAuthenticationPolicy
from azure.core.pipeline.policies import (
    ContentDecodePolicy,
    DistributedTracingPolicy,
    HttpLoggingPolicy,
    RequestIdPolicy,
    RetryPolicy,
    UserAgentPolicy,
)

from ._enums import ServiceType
from ._api_versions import ServiceAPIVersions
from ._service_registry import get_service_for_operation, get_service_metadata
from ._operations import OperationsProxy

if TYPE_CHECKING:
    from azure.core.pipeline import PipelineClient


class UnifiedManagementClient:
    """Unified client for Azure Management Plane operations.
    
    This client provides a single entry point for all Azure management services,
    automatically routing operations to the appropriate service implementation.
    
    Args:
        credential: Azure credential for authentication.
        subscription_id: Azure subscription ID.
        service: Optional ServiceType to scope this client to a specific service.
        api_versions: Optional dictionary of custom API versions per service.
        base_url: Base URL for Azure Management API (default: https://management.azure.com).
        credential_scopes: Authentication scopes (default: Azure Management scope).
        **kwargs: Additional keyword arguments passed to underlying service clients.
    
    Example:
        >>> from azure.identity import DefaultAzureCredential
        >>> from azure.mgmt.unified import UnifiedManagementClient, ServiceType
        >>> 
        >>> credential = DefaultAzureCredential()
        >>> subscription_id = "00000000-0000-0000-0000-000000000000"
        >>> 
        >>> # Multi-service client
        >>> client = UnifiedManagementClient(credential, subscription_id)
        >>> storage_accounts = client.storage_accounts.list()
        >>> vms = client.virtual_machines.list(resource_group_name="my-rg")
        >>> 
        >>> # Service-scoped client
        >>> storage_client = UnifiedManagementClient(
        ...     credential, 
        ...     subscription_id,
        ...     service=ServiceType.STORAGE
        ... )
        >>> accounts = storage_client.storage_accounts.list()
    """
    
    def __init__(
        self,
        credential: TokenCredential,
        subscription_id: str,
        service: Optional[ServiceType] = None,
        api_versions: Optional[Dict[ServiceType, str]] = None,
        base_url: str = "https://management.azure.com",
        credential_scopes: Optional[list] = None,
        **kwargs: Any
    ):
        """Initialize UnifiedManagementClient."""
        self._credential = credential
        self._subscription_id = subscription_id
        self._service = service
        self._base_url = base_url
        self._credential_scopes = credential_scopes or ["https://management.azure.com/.default"]
        self._kwargs = kwargs
        
        # Initialize API version manager
        self._api_versions = ServiceAPIVersions(api_versions)
        
        # Cache for service clients
        self._service_clients: Dict[ServiceType, Any] = {}
        
        # Cache for operation proxies
        self._operation_proxies: Dict[str, OperationsProxy] = {}
        
        # Shared ARM pipeline client
        self._create_shared_pipeline()
    
    def _create_shared_pipeline(self) -> None:
        """Create shared ARM pipeline for all services."""
        # Build authentication policy
        authentication_policy = ARMChallengeAuthenticationPolicy(
            self._credential,
            *self._credential_scopes,
            **self._kwargs
        )
        
        # Build policies
        policies = [
            RequestIdPolicy(**self._kwargs),
            UserAgentPolicy(**self._kwargs),
            ContentDecodePolicy(**self._kwargs),
            RetryPolicy(**self._kwargs),
            authentication_policy,
            DistributedTracingPolicy(**self._kwargs),
            HttpLoggingPolicy(**self._kwargs),
        ]
        
        # Create ARM pipeline client
        self._pipeline_client: ARMPipelineClient = ARMPipelineClient(
            base_url=self._base_url,
            policies=policies,
            **self._kwargs
        )
    
    def _load_service_client(self, service: ServiceType) -> Any:
        """Load and cache a service client.
        
        Args:
            service: The ServiceType to load.
            
        Returns:
            The loaded service management client.
        """
        if service in self._service_clients:
            return self._service_clients[service]
        
        # Get service metadata
        metadata = get_service_metadata(service)
        package_name = metadata["package"]
        client_class_name = metadata["client_class"]
        
        try:
            # Dynamically import the service client
            module = importlib.import_module(package_name)
            client_class = getattr(module, client_class_name)
            
            # Get API version for this service
            api_version = self._api_versions.get(service)
            
            # Create client instance
            client = client_class(
                credential=self._credential,
                subscription_id=self._subscription_id,
                base_url=self._base_url,
                credential_scopes=self._credential_scopes,
                api_version=api_version,
                **self._kwargs
            )
            
            # Cache the client
            self._service_clients[service] = client
            return client
            
        except ImportError as e:
            raise ImportError(
                f"Failed to import {package_name}. "
                f"Make sure the package is installed: "
                f"pip install azure-mgmt-unified[{service.value}]"
            ) from e
        except Exception as e:
            raise RuntimeError(
                f"Failed to create client for service {service.value}: {e}"
            ) from e
    
    def __getattr__(self, name: str) -> OperationsProxy:
        """Dynamically load operation groups.
        
        This method intercepts attribute access and creates OperationsProxy
        instances for operation groups, which then route to the appropriate
        service implementation.
        
        Args:
            name: The operation group name (e.g., 'storage_accounts').
            
        Returns:
            An OperationsProxy that routes operations to the correct service.
        """
        # Avoid recursion for private attributes
        if name.startswith('_'):
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
        
        # Check if we already have this proxy cached
        if name in self._operation_proxies:
            return self._operation_proxies[name]
        
        # Determine which service this operation belongs to
        if self._service:
            # Service-scoped client - use the specified service
            service = self._service
        else:
            # Multi-service client - detect service from operation name
            try:
                service = get_service_for_operation(name)
            except KeyError as e:
                raise AttributeError(
                    f"Operation '{name}' not found. "
                    f"If this operation exists in multiple services, "
                    f"create a service-scoped client with service=ServiceType.XXX"
                ) from e
        
        # Load the service client
        service_client = self._load_service_client(service)
        
        # Get the actual operation group from the service client
        try:
            operations_group = getattr(service_client, name)
        except AttributeError as e:
            raise AttributeError(
                f"Service {service.value} does not have operation group '{name}'"
            ) from e
        
        # Create and cache an OperationsProxy
        proxy = OperationsProxy(operations_group, service, name)
        self._operation_proxies[name] = proxy
        
        return proxy
    
    def get_service_client(self, service: ServiceType) -> Any:
        """Explicitly get a service client.
        
        This method allows direct access to the underlying service-specific
        management client if needed for advanced scenarios.
        
        Args:
            service: The ServiceType to get the client for.
            
        Returns:
            The service management client.
        
        Example:
            >>> client = UnifiedManagementClient(credential, subscription_id)
            >>> storage_client = client.get_service_client(ServiceType.STORAGE)
            >>> # Now you have direct access to StorageManagementClient
        """
        return self._load_service_client(service)
    
    def close(self) -> None:
        """Close all service clients and cleanup resources."""
        # Close all cached service clients
        for client in self._service_clients.values():
            if hasattr(client, 'close'):
                client.close()
        
        # Close pipeline client
        if hasattr(self._pipeline_client, 'close'):
            self._pipeline_client.close()
        
        # Clear caches
        self._service_clients.clear()
        self._operation_proxies.clear()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, *exc_details):
        """Context manager exit."""
        self.close()
    
    def __repr__(self) -> str:
        """Return string representation."""
        if self._service:
            return (
                f"<UnifiedManagementClient "
                f"service={self._service.value} "
                f"subscription={self._subscription_id[:8]}...>"
            )
        return (
            f"<UnifiedManagementClient "
            f"multi-service "
            f"subscription={self._subscription_id[:8]}...>"
        )
