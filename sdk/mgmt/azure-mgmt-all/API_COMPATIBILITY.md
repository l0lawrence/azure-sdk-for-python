# API Compatibility with azure-mgmt-appconfiguration

This document shows how the `azure-mgmt-all` package provides API compatibility with the official `azure-mgmt-appconfiguration` package.

## Method Mapping

Our factory methods now match the official `ConfigurationStoresOperations` class:

| Official Method | azure-mgmt-all Factory Method |
|----------------|------------------------------|
| `list(skip_token=None)` | `list(skip_token=None)` |
| `list_by_resource_group(resource_group_name, skip_token=None)` | `list_by_resource_group(resource_group_name, skip_token=None)` |
| `get(resource_group_name, config_store_name)` | `get(resource_group_name, config_store_name)` |
| `begin_create(resource_group_name, config_store_name, config_store_creation_parameters)` | `begin_create(resource_group_name, config_store_name, config_store_creation_parameters)` |
| `begin_update(resource_group_name, config_store_name, config_store_update_parameters)` | `begin_update(resource_group_name, config_store_name, config_store_update_parameters)` |
| `begin_delete(resource_group_name, config_store_name)` | `begin_delete(resource_group_name, config_store_name)` |
| `list_keys(resource_group_name, config_store_name, skip_token=None)` | `list_keys(resource_group_name, config_store_name, skip_token=None)` |
| `regenerate_key(resource_group_name, config_store_name, regenerate_key_parameters)` | `regenerate_key(resource_group_name, config_store_name, regenerate_key_parameters)` |

## Parameter Standardization

### Parameter Name Changes
- `resource_group` → `resource_group_name` (matches official Azure SDK convention)
- `config_store_data` → `config_store_creation_parameters` (for create operations)
- `config_store_data` → `config_store_update_parameters` (for update operations)  
- `key_to_regenerate` → `regenerate_key_parameters` (for key regeneration)

### Added Features
- **Pagination Support**: Added `skip_token` parameter to list operations
- **LRO Compliance**: All long-running operations use `begin_*` prefix
- **Type Safety**: Full TypedDict models for request/response types

## Usage Examples

### Migration from azure-mgmt-appconfiguration

**Before (official package):**
```python
from azure.mgmt.appconfiguration import AppConfigurationManagementClient

client = AppConfigurationManagementClient(credential, subscription_id)
stores = client.configuration_stores.list()
store = client.configuration_stores.get(resource_group_name="rg", config_store_name="store")
```

**After (azure-mgmt-all factory):**
```python
from azure.mgmt.all import ManagementClient

client = ManagementClient(credential, subscription_id)
app_config = client("Microsoft.AppConfiguration")
stores = app_config.list()
store = app_config.get(resource_group_name="rg", config_store_name="store")
```

### Async Compatibility

Both sync and async versions provide identical API surfaces:

```python
# Sync
from azure.mgmt.all import ManagementClient
client = ManagementClient(credential, subscription_id)
app_config = client("Microsoft.AppConfiguration")
stores = app_config.list()

# Async  
from azure.mgmt.all.aio import AsyncManagementClient
async with AsyncManagementClient(credential, subscription_id) as client:
    app_config = client("Microsoft.AppConfiguration")
    stores = await app_config.list()
```

## Benefits

1. **API Consistency**: Method names and parameters match official Azure SDK packages
2. **Drop-in Replacement**: Easy migration path from service-specific packages  
3. **Enhanced Features**: Built-in pagination, LRO support, and type safety
4. **Unified Interface**: Single factory pattern for all Azure services
5. **Future-proof**: Extensible design for adding new Azure services

## Additional Methods

Beyond the standard operations, we also provide convenience methods:

- `create_configuration_store()`: Direct create without LRO polling
- Additional specialized factories for other Azure services through the same pattern

This ensures both compatibility with existing code and enhanced functionality for new development.