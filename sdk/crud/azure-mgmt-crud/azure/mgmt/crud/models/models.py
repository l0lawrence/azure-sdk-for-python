from typing import Any, Dict, List, Optional, TypeVar, Generic, TYPE_CHECKING, Type, Union
from typing_extensions import TypedDict, Unpack, Required, NotRequired
from enum import Enum
import datetime
from azure.core import CaseInsensitiveEnumMeta


T = TypeVar("T") # bound by model?
TResourceType = TypeVar('TResourceType', bound='ResourceType')

class ResourceTypeParameters(TypedDict):
    """Base parameters for all resource types."""
    resource_group_name: Required[str]
    api_version: NotRequired[str]
    properties: NotRequired[Optional[Any]]

class ResourceType(Generic[T]):
    """Common ARM resource fields."""
    _validation = {"id": {"readonly": True}, "name": {"readonly": True}, "type": {"readonly": True}, "properties": {"readonly": False}} # properties would not be readonly bc think of put operation

    # Default URL template - should be overridden by subclasses
    _url_template = "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProvider}/{resourceType}/{resourceName}"

    # ^ these are used by serializer might need to adjsut 

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.resource_group_name: str
        self.resource_name: str
        self.id = None
        self.name = None
        self.type = None
        self.properties: Optional[T] = None 
    
    @classmethod
    def get_url_template(cls) -> str:
        """Get the URL template for this resource type."""
        return cls._url_template
    
    @classmethod 
    def from_response(cls: Type[TResourceType], data_dict: Dict[str, Any], **kwargs) -> TResourceType:
        """Create instance from API response data and request parameters."""
        properties = data_dict.get('properties', {})
        
        # Create instance with constructor parameters from kwargs
        instance = cls(**kwargs, properties=properties)
        
        # Set response data attributes
        instance.id = data_dict.get('id')
        instance.name = data_dict.get('name')
        instance.type = data_dict.get('type')
        
        return instance
    
    def build_instance_path_arguments(self, subscription_id: str) -> Dict[str, str]:
        """Build path arguments from instance attributes."""
        return {
            "subscriptionId": subscription_id,
            "resourceGroupName": self.resource_group_name,
            "resourceName": self.resource_name,
        }

class AccountImmutabilityPolicyState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """The ImmutabilityPolicy state defines the mode of the policy. Disabled state disables the
    policy, Unlocked state allows increase and decrease of immutability retention time and also
    allows toggling allowProtectedAppendWrites property, Locked state only allows the increase of
    the immutability retention time. A policy can only be created in a Disabled or Unlocked state
    and can be toggled between the two states. Only a policy in an Unlocked state can transition to
    a Locked state which cannot be reverted.
    """

    UNLOCKED = "Unlocked"
    LOCKED = "Locked"
    DISABLED = "Disabled"

class ImmutabilityPolicyProperties(TypedDict):
    """Properties of an Immutability Policy."""
    immutability_period_since_creation_in_days: Optional[int]
    state: Optional[Union[str,AccountImmutabilityPolicyState]]
    allow_protected_append_writes: Optional[bool]

class TagProperty(TypedDict):
    """Tag property of a Legal Hold."""
    tag: Optional[str]
    timestamp: Optional[datetime.datetime]
    object_identifier: Optional[str]
    tenant_id: Optional[str]
    upn: Optional[str]

class ProtectedAppendWritesHistory(TypedDict):
    """Protected append writes history."""
    allow_protected_append_writes_all: Optional[bool]
    timestamp: Optional[datetime.datetime]

class LegalHoldProperties(TypedDict):
    """Properties of a Legal Hold."""
    has_legal_hold: Optional[bool]
    tags: Optional[List[TagProperty]]
    protected_append_writes_history: Optional[ProtectedAppendWritesHistory]


class MigrationState(str, Enum, metaclass=CaseInsensitiveEnumMeta):
    """This property denotes the container level immutability to object level immutability migration
    state.
    """

    IN_PROGRESS = "InProgress"
    COMPLETED = "Completed"

class ImmutableStorageWithVersioning(TypedDict):
    """Immutable storage with versioning properties."""
    enabled: Optional[bool]
    time_stamp: Optional[datetime.datetime]
    migration_state: Optional[Union[str, MigrationState]]


class BlobContainerProperties(TypedDict):
    """Properties of a Blob Container resource."""
    public_access: Optional[str]
    last_modified_time: Optional[str]
    etag: Optional[str]
    version: Optional[str]
    deleted: Optional[bool]
    deleted_time: Optional[str]
    remaining_retention_days: Optional[int]
    default_encryption_scope: Optional[str]
    deny_encryption_scope_override: Optional[bool]
    lease_status: Optional[str]
    lease_state: Optional[str]
    lease_duration: Optional[str]
    metadata: Optional[Dict[str, str]]
    immutability_policy: Optional[ImmutabilityPolicyProperties]
    legal_hold: Optional[LegalHoldProperties]
    has_legal_hold: Optional[bool]
    has_immutability_policy: Optional[bool]
    immutable_storage_with_versioning: Optional[ImmutableStorageWithVersioning]
    enable_nfs_v3_root_squash: Optional[bool]
    enable_nfs_v3_all_squash: Optional[bool]

class BlobContainerParameters(ResourceTypeParameters):
    """Parameters for BlobContainer resource."""
    storage_account_name: Required[str]
    container_name: Required[str]

class BlobContainer(ResourceType[BlobContainerProperties]):
    """A Blob Container resource.

    Variables are only populated by the server, and will be ignored when sending a request.

    :param resource_group_name: The name of the resource group. Required.
    :type resource_group_name: str
    :param storage_account_name: The name of the storage account. Required.
    :type storage_account_name: str
    :param container_name: The name of the blob container. Required.
    :type container_name: str
    :keyword api_version: The API version used to create the resource.
    :paramtype api_version: str
    :keyword properties: Properties of a Blob Container resource.
    :paramtype properties: ~azure.mgmt.crud.models.BlobContainerProperties
    """

    # URL template for this resource type
    _url_template = "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Storage/storageAccounts/{storageAccountName}/blobServices/default/containers/{containerName}"

    def build_instance_path_arguments(self, subscription_id: str) -> Dict[str, str]:
        """Build path arguments from instance attributes."""
        return {
            "subscriptionId": subscription_id,
            "resourceGroupName": self.resource_group_name,
            "storageAccountName": self.storage_account_name,
            "containerName": self.container_name,
        }

    _validation = {
        "id": {"readonly": True},
        "name": {"readonly": True},
        "type": {"readonly": True},
        "etag": {"readonly": True},
        "last_modified_time": {"readonly": True},
        "deleted": {"readonly": True},
        "deleted_time": {"readonly": True},
        "remaining_retention_days": {"readonly": True},
        "lease_status": {"readonly": True},
        "lease_state": {"readonly": True},
        "has_legal_hold": {"readonly": True},
        "has_immutability_policy": {"readonly": True},
    }

    @classmethod
    def from_response(cls, data_dict: Dict[str, Any], **kwargs) -> 'BlobContainer':
        """Create BlobContainer instance from API response data and request parameters."""
        properties = data_dict.get('properties', {})
        
        # Create instance with BlobContainer-specific constructor parameters
        instance = cls(
            resource_group_name=kwargs.get('resource_group_name', 'unknown'),
            storage_account_name=kwargs.get('storage_account_name', 'unknown'),  
            container_name=kwargs.get('container_name', 'unknown'),
            api_version=kwargs.get('api_version'),
            properties=properties
        )
        
        # Set response data attributes
        instance.id = data_dict.get('id')
        instance.name = data_dict.get('name')
        instance.type = data_dict.get('type')
        
        return instance

    def __init__(self, resource_group_name:str, storage_account_name:str, container_name:str, **kwargs) -> None:
        super().__init__()
        self.resource_group_name = resource_group_name
        self.storage_account_name = storage_account_name
        self.container_name = container_name
        self.api_version: str = kwargs.get("api_version", "2025-06-01")
        self.properties: Optional[BlobContainerProperties] = kwargs.get("properties", None)