# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""API version management for Azure Management services."""

from typing import Dict, Optional
from ._enums import ServiceType
from ._service_registry import SERVICE_REGISTRY


class ServiceAPIVersions:
    """Manager for API versions across Azure Management services.
    
    This class provides centralized management of API versions with:
    - Default versions per service from service registry
    - Custom version overrides per service
    - Easy retrieval of versions for operations
    
    Example:
        >>> # Use default versions
        >>> api_versions = ServiceAPIVersions()
        >>> api_versions.get(ServiceType.STORAGE)
        '2023-05-01'
        
        >>> # Override specific service versions
        >>> api_versions = ServiceAPIVersions({
        ...     ServiceType.STORAGE: '2022-09-01',
        ...     ServiceType.COMPUTE: '2023-09-01'
        ... })
        >>> api_versions.get(ServiceType.STORAGE)
        '2022-09-01'
    """
    
    def __init__(self, custom_versions: Optional[Dict[ServiceType, str]] = None):
        """Initialize ServiceAPIVersions manager.
        
        Args:
            custom_versions: Optional dictionary mapping ServiceType to custom API version strings.
                            These override the default versions from the service registry.
        """
        # Load default versions from service registry
        self._default_versions: Dict[ServiceType, str] = {
            service: metadata["default_api_version"]
            for service, metadata in SERVICE_REGISTRY.items()
        }
        
        # Apply custom overrides
        self._custom_versions: Dict[ServiceType, str] = custom_versions or {}
        
        # Merged versions (custom overrides defaults)
        self._versions: Dict[ServiceType, str] = {
            **self._default_versions,
            **self._custom_versions
        }
    
    def get(self, service: ServiceType) -> str:
        """Get the API version for a service.
        
        Args:
            service: The ServiceType enum.
            
        Returns:
            The API version string for the service.
            
        Raises:
            KeyError: If the service is not registered.
        """
        if service not in self._versions:
            raise KeyError(f"Service {service} not found in API version registry")
        return self._versions[service]
    
    def set(self, service: ServiceType, version: str) -> None:
        """Set a custom API version for a service.
        
        Args:
            service: The ServiceType enum.
            version: The API version string (e.g., '2023-05-01').
        """
        self._custom_versions[service] = version
        self._versions[service] = version
    
    def reset(self, service: ServiceType) -> None:
        """Reset a service's API version to its default.
        
        Args:
            service: The ServiceType enum.
        """
        if service in self._custom_versions:
            del self._custom_versions[service]
        self._versions[service] = self._default_versions[service]
    
    def get_default(self, service: ServiceType) -> str:
        """Get the default API version for a service.
        
        Args:
            service: The ServiceType enum.
            
        Returns:
            The default API version string.
        """
        return self._default_versions[service]
    
    def is_custom(self, service: ServiceType) -> bool:
        """Check if a service has a custom API version set.
        
        Args:
            service: The ServiceType enum.
            
        Returns:
            True if a custom version is set, False otherwise.
        """
        return service in self._custom_versions
    
    def list_all(self) -> Dict[ServiceType, str]:
        """Get all API versions (default + custom).
        
        Returns:
            Dictionary mapping ServiceType to API version strings.
        """
        return self._versions.copy()
    
    def list_custom(self) -> Dict[ServiceType, str]:
        """Get only custom API versions.
        
        Returns:
            Dictionary mapping ServiceType to custom API version strings.
        """
        return self._custom_versions.copy()
    
    def __repr__(self) -> str:
        """Return string representation."""
        custom_count = len(self._custom_versions)
        total_count = len(self._versions)
        return (
            f"<ServiceAPIVersions "
            f"services={total_count} "
            f"custom={custom_count}>"
        )
