# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""Common base models for all Azure Management resources."""

from typing import Any, Dict, Optional, List
from typing_extensions import TypedDict


class ResourceBase:
    """Base class for all Azure resources.
    
    All Azure resources share these common properties defined by
    Azure Resource Manager (ARM).
    
    Attributes:
        id: Fully qualified resource ID.
        name: Resource name.
        type: Resource type (e.g., Microsoft.Storage/storageAccounts).
        location: Resource location.
        tags: Resource tags as key-value pairs.
    """
    
    def __init__(
        self,
        id: Optional[str] = None,  # pylint: disable=redefined-builtin
        name: Optional[str] = None,
        type: Optional[str] = None,  # pylint: disable=redefined-builtin
        location: Optional[str] = None,
        tags: Optional[Dict[str, str]] = None,
        **kwargs: Any
    ):
        """Initialize a ResourceBase instance.
        
        Args:
            id: Fully qualified resource ID.
            name: Resource name.
            type: Resource type.
            location: Resource location.
            tags: Resource tags.
            **kwargs: Additional resource-specific properties.
        """
        self.id = id
        self.name = name
        self.type = type
        self.location = location
        self.tags = tags or {}
        
        # Store additional properties
        self._additional_properties = kwargs
    
    def __getattr__(self, name: str) -> Any:
        """Get additional properties not defined in base class.
        
        This allows service-specific properties to be accessed even though
        they're not defined in the base class.
        """
        if name.startswith('_'):
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
        return self._additional_properties.get(name)
    
    def __setattr__(self, name: str, value: Any) -> None:
        """Set attribute, storing additional properties separately."""
        if name in ('id', 'name', 'type', 'location', 'tags', '_additional_properties'):
            super().__setattr__(name, value)
        else:
            if not hasattr(self, '_additional_properties'):
                super().__setattr__('_additional_properties', {})
            self._additional_properties[name] = value
    
    def as_dict(self) -> Dict[str, Any]:
        """Return the resource as a dictionary.
        
        Returns:
            Dictionary representation of the resource.
        """
        result = {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'location': self.location,
            'tags': self.tags,
        }
        result.update(self._additional_properties)
        return {k: v for k, v in result.items() if v is not None}
    
    def __repr__(self) -> str:
        """Return string representation."""
        return f"<{self.type or 'Resource'} name={self.name!r} id={self.id!r}>"


class TrackedResourceBase(ResourceBase):
    """Base class for tracked resources (resources with location).
    
    Tracked resources are resources that have a location property and appear
    in resource group listings.
    """
    
    def __init__(
        self,
        location: str,
        id: Optional[str] = None,  # pylint: disable=redefined-builtin
        name: Optional[str] = None,
        type: Optional[str] = None,  # pylint: disable=redefined-builtin
        tags: Optional[Dict[str, str]] = None,
        **kwargs: Any
    ):
        """Initialize a TrackedResourceBase instance.
        
        Args:
            location: Resource location (required for tracked resources).
            id: Fully qualified resource ID.
            name: Resource name.
            type: Resource type.
            tags: Resource tags.
            **kwargs: Additional resource-specific properties.
        """
        if not location:
            raise ValueError("Location is required for tracked resources")
        super().__init__(id=id, name=name, type=type, location=location, tags=tags, **kwargs)


class ProxyResourceBase(ResourceBase):
    """Base class for proxy resources (resources without location).
    
    Proxy resources are resources that don't have a location property and
    are typically child resources of other resources.
    """
    
    def __init__(
        self,
        id: Optional[str] = None,  # pylint: disable=redefined-builtin
        name: Optional[str] = None,
        type: Optional[str] = None,  # pylint: disable=redefined-builtin
        **kwargs: Any
    ):
        """Initialize a ProxyResourceBase instance.
        
        Args:
            id: Fully qualified resource ID.
            name: Resource name.
            type: Resource type.
            **kwargs: Additional resource-specific properties.
        """
        super().__init__(id=id, name=name, type=type, location=None, tags=None, **kwargs)


class ResourceListResult:
    """Result of a resource list operation.
    
    Attributes:
        value: List of resources.
        next_link: URL to get the next set of resources.
    """
    
    def __init__(
        self,
        value: Optional[List[ResourceBase]] = None,
        next_link: Optional[str] = None,
        **kwargs: Any
    ):
        """Initialize a ResourceListResult instance.
        
        Args:
            value: List of resources.
            next_link: URL to get the next page.
            **kwargs: Additional properties.
        """
        self.value = value or []
        self.next_link = next_link
        self._additional_properties = kwargs
    
    def __iter__(self):
        """Iterate over resources in the result."""
        return iter(self.value)
    
    def __len__(self) -> int:
        """Get count of resources in the result."""
        return len(self.value)
    
    def __repr__(self) -> str:
        """Return string representation."""
        return f"<ResourceListResult count={len(self.value)} next_link={self.next_link!r}>"


class SystemData:
    """Metadata about resource creation and modification.
    
    Attributes:
        created_by: Identity that created the resource.
        created_by_type: Type of identity (User, Application, ManagedIdentity, Key).
        created_at: Timestamp of resource creation.
        last_modified_by: Identity that last modified the resource.
        last_modified_by_type: Type of identity.
        last_modified_at: Timestamp of last modification.
    """
    
    def __init__(
        self,
        created_by: Optional[str] = None,
        created_by_type: Optional[str] = None,
        created_at: Optional[str] = None,
        last_modified_by: Optional[str] = None,
        last_modified_by_type: Optional[str] = None,
        last_modified_at: Optional[str] = None,
        **kwargs: Any
    ):
        """Initialize SystemData."""
        self.created_by = created_by
        self.created_by_type = created_by_type
        self.created_at = created_at
        self.last_modified_by = last_modified_by
        self.last_modified_by_type = last_modified_by_type
        self.last_modified_at = last_modified_at


class ErrorResponse:
    """Common error response structure.
    
    Attributes:
        code: Error code.
        message: Error message.
        target: Error target.
        details: Additional error details.
    """
    
    def __init__(
        self,
        code: Optional[str] = None,
        message: Optional[str] = None,
        target: Optional[str] = None,
        details: Optional[List[Dict[str, Any]]] = None,
        **kwargs: Any
    ):
        """Initialize ErrorResponse."""
        self.code = code
        self.message = message
        self.target = target
        self.details = details or []
    
    def __repr__(self) -> str:
        """Return string representation."""
        return f"<ErrorResponse code={self.code!r} message={self.message!r}>"
