from typing_extensions import TypedDict, NotRequired
from typing import List, Dict

# Shared TypedDict models for azure-mgmt-appconfiguration
# These models can be used by both sync and async implementations

class ApiKey(TypedDict, total=False):
    """An API key used for authenticating with a configuration store endpoint."""
    id: NotRequired[str]  # readonly
    name: NotRequired[str]  # readonly
    value: NotRequired[str]  # readonly
    connection_string: NotRequired[str]  # readonly
    last_modified: NotRequired[str]  # readonly, ISO-8601 datetime
    read_only: NotRequired[bool]  # readonly

class ApiKeyListResult(TypedDict, total=False):
    """The result of a request to list API keys."""
    value: NotRequired[List[ApiKey]]
    next_link: NotRequired[str]

class Sku(TypedDict):
    """The SKU of the configuration store."""
    name: str  # Required. Known values: "Free", "Standard", "Premium"

class UserIdentity(TypedDict, total=False):
    """User assigned identity properties."""
    principal_id: NotRequired[str]  # readonly
    client_id: NotRequired[str]  # readonly

class ResourceIdentity(TypedDict, total=False):
    """The managed identity information for the configuration store."""
    type: NotRequired[str]  # Known values: "None", "SystemAssigned", "UserAssigned", "SystemAssigned, UserAssigned"
    user_assigned_identities: NotRequired[Dict[str, UserIdentity]]
    principal_id: NotRequired[str]  # readonly
    tenant_id: NotRequired[str]  # readonly

class KeyVaultProperties(TypedDict, total=False):
    """Settings concerning key vault encryption for a configuration store."""
    key_identifier: NotRequired[str]
    identity_client_id: NotRequired[str]

class EncryptionProperties(TypedDict, total=False):
    """The encryption settings of the configuration store."""
    key_vault_properties: NotRequired[KeyVaultProperties]

class SystemData(TypedDict, total=False):
    """Resource system metadata."""
    created_by: NotRequired[str]
    created_by_type: NotRequired[str]
    created_at: NotRequired[str]  # ISO-8601 datetime
    last_modified_by: NotRequired[str]
    last_modified_by_type: NotRequired[str]
    last_modified_at: NotRequired[str]  # ISO-8601 datetime

class PrivateEndpointConnectionReference(TypedDict, total=False):
    """A reference to a related private endpoint connection."""
    id: NotRequired[str]  # readonly
    name: NotRequired[str]  # readonly
    type: NotRequired[str]  # readonly
    provisioning_state: NotRequired[str]  # readonly

class DataPlaneProxyProperties(TypedDict, total=False):
    """Property specifying the configuration of data plane proxy for Azure Resource Manager (ARM)."""
    authentication_mode: NotRequired[str]  # Known values: "Pass", "Local"
    private_link_resource_id: NotRequired[str]

class ConfigurationStore(TypedDict):
    """The configuration store along with all resource properties."""
    # Required fields
    location: str
    sku: Sku
    
    # Optional fields
    tags: NotRequired[Dict[str, str]]
    identity: NotRequired[ResourceIdentity]
    
    # Properties (optional)
    encryption: NotRequired[EncryptionProperties]
    public_network_access: NotRequired[str]  # Known values: "Enabled", "Disabled"
    disable_local_auth: NotRequired[bool]
    soft_delete_retention_in_days: NotRequired[int]
    default_key_value_revision_retention_period_in_seconds: NotRequired[int]
    enable_purge_protection: NotRequired[bool]
    data_plane_proxy: NotRequired[DataPlaneProxyProperties]
    create_mode: NotRequired[str]  # Known values: "Recover", "Default"
    
    # Readonly fields
    id: NotRequired[str]  # readonly
    name: NotRequired[str]  # readonly
    type: NotRequired[str]  # readonly
    system_data: NotRequired[SystemData]  # readonly
    provisioning_state: NotRequired[str]  # readonly
    creation_date: NotRequired[str]  # readonly, ISO-8601 datetime
    endpoint: NotRequired[str]  # readonly

class ConfigurationStoreListResult(TypedDict, total=False):
    """The result of a request to list configuration stores."""
    value: NotRequired[List[ConfigurationStore]]
    next_link: NotRequired[str]