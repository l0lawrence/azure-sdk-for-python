from typing import Any, Dict, List, Optional, TypeVar, Generic, TYPE_CHECKING, Type, Union
from typing_extensions import TypedDict, Unpack, Required, NotRequired
from enum import Enum
import datetime
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
    
    # Default URL template - should be overridden by subclasses
    _url_template = "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/{resourceProvider}/{resourceType}/{resourceName}"

    # ^ these are used by serializer might need to adjsut 

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.id = None
        self.name = None
        self.type = None
        self.api_version = None
        self.properties: Optional[T] = None 
    
    @classmethod
    def get_url_template(cls) -> str:
        """Get the URL template for this resource type."""
        return cls._url_template
    
    def build_instance_path_arguments(self, subscription_id: str) -> Dict[str, str]:
        """Build path arguments from instance attributes."""
        return {
            "subscriptionId": subscription_id,
            "resourceGroupName": self.resource_group_name,
            "resourceName": self.resource_name,
        } 

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

    :param resource_group_name: The name of the resource group. Required.
    :type resource_group_name: str
    :param resource_name: The name of the custom location. Required.
    :type resource_name: str
    :keyword api_version: The API version used to create the resource.
    :paramtype api_version: str
    :keyword properties: Properties of a Custom Location resource.
    :paramtype properties: ~azure.mgmt.crud.models.CustomLocationProperties
    """

    # URL template for this resource type
    _url_template = "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ExtendedLocation/customLocations/{resourceName}"

    def __init__(self, resource_group_name: str, resource_name: str, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.resource_group_name = resource_group_name
        self.resource_name = resource_name
        self.api_version: str = kwargs.get("api_version", "2021-08-15") # use api verison enum?
        self.properties: Optional[CustomLocationProperties] = kwargs.get("properties", None)
    
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

    def __init__(self, resource_group_name: str, storage_account_name: str, container_name: str, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.resource_group_name = resource_group_name
        self.storage_account_name = storage_account_name
        self.container_name = container_name
        self.api_version: str = kwargs.get("api_version", "2025-06-01") # use api verison enum?
        self.properties: Optional[BlobContainerProperties] = kwargs.get("properties", None)