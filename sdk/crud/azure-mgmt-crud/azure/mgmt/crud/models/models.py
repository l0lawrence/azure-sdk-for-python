from typing import Any, Dict, List, Optional, TypeVar, Generic, TYPE_CHECKING, Type, Union
from typing_extensions import TypedDict, Unpack, Required, NotRequired
from enum import Enum
from azure.core import CaseInsensitiveEnumMeta


T = TypeVar("T") # bound by model?

class ResourceType(Generic[T]):
    """Common ARM resource fields."""
    _validation = {"id": {"readonly": True}, "name": {"readonly": True}, "type": {"readonly": True}, "properties": {"readonly": False}} # properties would not be readonly bc think of put operation
    _attribute_map = {
        "id": {"key": "id", "type": "str"},
        "name": {"key": "name", "type": "str"},
        "type": {"key": "type", "type": "str"},
        "properties": {"key": "properties", "type": T},
    }

    # ^ these are used by serializer might need to adjsut 

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.id = None
        self.name = None
        self.type = None
        self.api_version = None
        self.properties: Optional[T] = None 

class ResourceIdentityType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The identity type."""

    SYSTEM_ASSIGNED = "SystemAssigned"
    NONE = "None"

class HostType(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """Type of host the Custom Locations is referencing (Kubernetes, etc...)."""

    KUBERNETES = "Kubernetes"

class CustomLocationPropertiesAuthentication(TypedDict):
        """This is optional input that contains the authentication that should be used to generate the namespace."""
        type: Optional[str]
        value: Optional[str]


class Identity(TypedDict):
        """Identity for the resource."""
        principal_id: NotRequired[Optional[str]]
        tenant_id: NotRequired[Optional[str]]
        type: NotRequired[Optional[Union[str, ResourceIdentityType]]]
     
class CustomLocationProperties(TypedDict):
        """Properties of a Custom Location resource."""
        location: str
        tags: Dict[str, str] # properties of a tracked resource, do we want to inherit that not within properties?
        identity: Optional[Identity]
        authentication: Optional[CustomLocationPropertiesAuthentication]
        cluster_extension_ids: Optional[List[str]]
        display_name: Optional[str]
        host_resource_id: Optional[str]
        host_type: Union[str, HostType]
        namespace: Optional[str]
        provisioning_state: Optional[str]


## If someone wants to pass in additional kwargs, do we need to use Unpack here?

class CustomLocation(ResourceType[CustomLocationProperties]):
    """A Custom Location resource.

    Variables are only populated by the server, and will be ignored when sending a request.

    :keyword id: Resource ID.
    :paramtype id: str
    :keyword name: Resource name.
    :paramtype name: str
    :keyword type: Resource type.
    :paramtype type: str
    :keyword api_version: The API version used to create the resource.
    :paramtype api_version: str
    :keyword properties: Properties of a Custom Location resource.
    :paramtype properties: ~azure.mgmt.crud.models.CustomLocationProperties
    """


    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.api_version: str = kwargs.get("api_version", "2021-08-15") # use api verison enum?
        self.properties: Optional[CustomLocationProperties] = kwargs.get("properties", None)