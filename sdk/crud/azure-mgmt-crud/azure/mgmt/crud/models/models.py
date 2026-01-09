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
    migration_state: Optional[str, MigrationState]


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

    :keyword id: Resource ID.
    :paramtype id: str
    :keyword name: Resource name.
    :paramtype name: str
    :keyword type: Resource type.
    :paramtype type: str
    :keyword api_version: The API version used to create the resource.
    :paramtype api_version: str
    :keyword properties: Properties of a Blob Container resource.
    :paramtype properties: ~azure.mgmt.crud.models.BlobContainerProperties
    """

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
    
    _attribute_map = {
        "id": {"key": "id", "type": "str"},
        "name": {"key": "name", "type": "str"},
        "type": {"key": "type", "type": "str"},
        "etag": {"key": "etag", "type": "str"},
        "version": {"key": "properties.version", "type": "str"},
        "deleted": {"key": "properties.deleted", "type": "bool"},
        "deleted_time": {"key": "properties.deletedTime", "type": "iso-8601"},
        "remaining_retention_days": {"key": "properties.remainingRetentionDays", "type": "int"},
        "default_encryption_scope": {"key": "properties.defaultEncryptionScope", "type": "str"},
        "deny_encryption_scope_override": {"key": "properties.denyEncryptionScopeOverride", "type": "bool"},
        "public_access": {"key": "properties.publicAccess", "type": "str"},
        "last_modified_time": {"key": "properties.lastModifiedTime", "type": "iso-8601"},
        "lease_status": {"key": "properties.leaseStatus", "type": "str"},
        "lease_state": {"key": "properties.leaseState", "type": "str"},
        "lease_duration": {"key": "properties.leaseDuration", "type": "str"},
        "metadata": {"key": "properties.metadata", "type": "{str}"},
        "immutability_policy": {"key": "properties.immutabilityPolicy", "type": "ImmutabilityPolicyProperties"},
        "legal_hold": {"key": "properties.legalHold", "type": "LegalHoldProperties"},
        "has_legal_hold": {"key": "properties.hasLegalHold", "type": "bool"},
        "has_immutability_policy": {"key": "properties.hasImmutabilityPolicy", "type": "bool"},
        "immutable_storage_with_versioning": {
            "key": "properties.immutableStorageWithVersioning",
            "type": "ImmutableStorageWithVersioning",
        },
        "enable_nfs_v3_root_squash": {"key": "properties.enableNfsV3RootSquash", "type": "bool"},
        "enable_nfs_v3_all_squash": {"key": "properties.enableNfsV3AllSquash", "type": "bool"},
    }

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.api_version: str = kwargs.get("api_version", "2025-06-01") # use api verison enum?
        self.properties: Optional[BlobContainerProperties] = kwargs.get("properties", None)