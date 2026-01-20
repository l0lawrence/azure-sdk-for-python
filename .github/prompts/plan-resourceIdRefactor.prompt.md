# Plan: Add ResourceId class to separate resource identity from resource properties

You'll create a new generic `ResourceId[PathParamsT]` class to encapsulate resource identity and URL building, separate from `ResourceType` which will focus only on resource properties. URL templates move to `ResourceId`, subscription_id stays as a client property, and TypeVar constraints ensure type safety.

## Steps

1. **Create generic `ResourceId[PathParamsT]` base class in [models/models.py](sdk/crud/azure-mgmt-crud/azure/mgmt/crud/models/models.py)** - Add class with TypeVar constraint `PathParamsT` bound to TypedDict, URL template class attributes (`_url_template`, `_list_url_template`), abstract methods `to_dict() -> PathParamsT` and `build_path_arguments(subscription_id: str) -> Dict[str, Any]`, class methods `from_dict(params: PathParamsT)` and `from_resource_id(resource_id: str)`, and URL building methods `get_operation_url(operation: str, subscription_id: str)` and `get_action_url(action: str, subscription_id: str)`

2. **Refactor `ResourceType` in [models/models.py](sdk/crud/azure-mgmt-crud/azure/mgmt/crud/models/models.py)** - Remove identity fields (`resource_group_name`, `resource_name`), remove URL template attributes (`_url_template`, `_list_url_template`), remove all URL-building methods (`get_operation_url`, `get_action_url`, `build_instance_path_arguments_from_params`), keep only property data fields (`id`, `name`, `type`, `properties`) and serialization methods (`from_response`, `to_dict`, `__init__`)

3. **Create `BlobContainerResourceId` in [models/storage_models.py](sdk/crud/azure-mgmt-crud/azure/mgmt/crud/models/storage_models.py)** - Extend `ResourceId[BlobContainerPathParams]`, add fields `resource_group_name: str`, `storage_account_name: str`, `container_name: str`, set URL template class attributes from current `BlobContainer`, implement `to_dict()` returning `BlobContainerPathParams`, implement `from_dict(params: BlobContainerPathParams)`, implement `from_resource_id()` using regex to parse ARM ID pattern, implement `build_path_arguments()` returning dict with all path parameters

4. **Update client operations in [_client.py](sdk/crud/azure-mgmt-crud/azure/mgmt/crud/_client.py)** - Change method signatures to accept `resource_id: ResourceId[PathParamsT]` instead of `resource_type` and `url_params`, for `create` and `update` add `resource_type: ResourceType[PropertiesT, Any]` parameter for properties payload, update URL building calls to use `resource_id.get_operation_url(operation, self._config.subscription_id)` and `resource_id.build_path_arguments(self._config.subscription_id)`, maintain `resource_type.from_response()` for deserializing responses into `ResourceType` instances

5. **Update all six samples** - Modify [sample_read.py](sdk/crud/azure-mgmt-crud/samples/sample_read.py), [sample_create.py](sdk/crud/azure-mgmt-crud/samples/sample_create.py), [sample_delete.py](sdk/crud/azure-mgmt-crud/samples/sample_delete.py), [sample_list.py](sdk/crud/azure-mgmt-crud/samples/sample_list.py), [sample_update.py](sdk/crud/azure-mgmt-crud/samples/sample_update.py), [sample_action.py](sdk/crud/azure-mgmt-crud/samples/sample_action.py) to instantiate `BlobContainerResourceId(resource_group_name=..., storage_account_name=..., container_name=...)`, add example showing `BlobContainerResourceId.from_resource_id(arm_id_string)` pattern, update client method calls to pass `resource_id` parameter

6. **Export new classes and update async client** - Add `ResourceId` and `BlobContainerResourceId` to exports in [models/__init__.py](sdk/crud/azure-mgmt-crud/azure/mgmt/crud/models/__init__.py), apply identical signature changes to [aio/_client.py](sdk/crud/azure-mgmt-crud/azure/mgmt/crud/aio/_client.py) async client methods

## Implementation Notes

- URL templates (`_url_template`, `_list_url_template`) fully migrate from `BlobContainer` class to `BlobContainerResourceId` class
- Client stores `subscription_id` in `self._config.subscription_id` and passes it to `ResourceId` methods as needed
- Use `TypeVar('PathParamsT', bound=TypedDict)` pattern at module level for type safety across `from_dict()` and `to_dict()` operations
- ARM resource ID parsing regex should match pattern: `/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Storage/storageAccounts/{accountName}/blobServices/default/containers/{containerName}`
