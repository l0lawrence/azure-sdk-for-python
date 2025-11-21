# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Operations routing and proxy layer."""

from typing import Any
from ._enums import ServiceType


class OperationsProxy:
    """Proxy for operation groups that routes calls to service implementations.
    
    This class wraps operation groups from service-specific clients and provides
    a transparent pass-through to the underlying operations. It exists primarily
    to maintain a clean abstraction layer and enable future enhancements like
    logging, metrics, or result transformation.
    
    Args:
        operations_group: The actual operations group from a service client.
        service: The ServiceType this operations group belongs to.
        name: The operation group name.
    
    Example:
        >>> # OperationsProxy transparently forwards all calls
        >>> proxy = OperationsProxy(storage_client.storage_accounts, ServiceType.STORAGE, "storage_accounts")
        >>> accounts = proxy.list()  # Calls storage_accounts.list()
    """
    
    def __init__(self, operations_group: Any, service: ServiceType, name: str):
        """Initialize OperationsProxy.
        
        Args:
            operations_group: The underlying operations group to proxy.
            service: The ServiceType enum.
            name: The operation group name.
        """
        self._operations_group = operations_group
        self._service = service
        self._name = name
    
    def __getattr__(self, name: str) -> Any:
        """Forward attribute access to the underlying operations group.
        
        This enables transparent pass-through of all operation calls
        (list, get, create_or_update, delete, etc.) to the actual
        service implementation.
        
        Args:
            name: The attribute/method name.
            
        Returns:
            The attribute from the underlying operations group.
        """
        # Avoid recursion for private attributes
        if name.startswith('_'):
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
        
        # Get the attribute from the underlying operations group
        attr = getattr(self._operations_group, name)
        
        # If it's a callable (method), we could wrap it here for logging/metrics
        # For now, just return it directly for transparent pass-through
        return attr
    
    def __dir__(self):
        """Support tab-completion by exposing underlying operations."""
        # Combine our attributes with the underlying operations group's attributes
        return sorted(set(
            dir(self._operations_group) +
            ['_operations_group', '_service', '_name']
        ))
    
    def __repr__(self) -> str:
        """Return string representation."""
        return (
            f"<OperationsProxy "
            f"service={self._service.value} "
            f"operations={self._name}>"
        )


class OperationCallWrapper:
    """Wrapper for individual operation calls (future enhancement).
    
    This class can be used to wrap individual method calls for:
    - Automatic logging of operations
    - Metrics collection
    - Result transformation (e.g., converting to ResourceBase)
    - Retry logic
    - Error handling
    
    Currently not implemented but kept as placeholder for future enhancements.
    """
    
    def __init__(self, func: Any, service: ServiceType, operation_name: str, method_name: str):
        """Initialize OperationCallWrapper.
        
        Args:
            func: The actual function to call.
            service: The ServiceType.
            operation_name: The operation group name.
            method_name: The method name (e.g., 'list', 'get').
        """
        self._func = func
        self._service = service
        self._operation_name = operation_name
        self._method_name = method_name
    
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """Call the wrapped function.
        
        This is where we could add:
        - Pre-call logging
        - Parameter validation
        - Post-call result transformation
        - Error handling
        
        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.
            
        Returns:
            The result from the wrapped function.
        """
        # Future: Add logging
        # logger.debug(f"Calling {self._service.value}.{self._operation_name}.{self._method_name}")
        
        # Call the actual function
        result = self._func(*args, **kwargs)
        
        # Future: Transform result to common base models
        # if isinstance(result, ItemPaged):
        #     result = transform_paged_result(result)
        
        return result
