# Lightweight Unified Azure Management SDK Design

A TypedDict-driven approach for easy maintenance and extensibility of Azure resource managers in Python.

## Overview

This document describes a lightweight, unified design for Azure management SDKs using Python's `TypedDict` for meta-definitions. This approach enables automated CRUD (Create, Read, Update, Delete), paging, and LRO (Long-Running Operations) mapping, significantly reducing boilerplate code and improving maintainability.

## Table of Contents

1. [Architectural Explanation](#architectural-explanation)
2. [TypedDict Meta-Definitions](#typeddict-meta-definitions)
3. [Example Resource Specifications](#example-resource-specifications)
4. [Automated Resource Manager Code](#automated-resource-manager-code)
5. [Benefits](#benefits)
6. [Practical Usage Example](#practical-usage-example)

---

## Architectural Explanation

The unified Azure management SDK design centers on declarative resource specifications. Instead of writing repetitive operation classes for each Azure resource, we define resources using TypedDict-based metadata that automatically generates the necessary operations.

### Core Principles

1. **Declarative Resource Definitions**: Resources are defined using TypedDict structures that specify their properties, operations, and behaviors.

2. **Automated Operation Mapping**: CRUD, paging, and LRO operations are automatically generated based on resource metadata.

3. **Consistent API Surface**: All resources expose a predictable, consistent interface regardless of their underlying complexity.

4. **Type Safety**: Full static type checking support through TypedDict definitions.

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     ResourceManager                              │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │ ResourceSpec    │  │ OperationSpec   │  │ LROSpec         │  │
│  │ (TypedDict)     │  │ (TypedDict)     │  │ (TypedDict)     │  │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘  │
│           │                    │                    │           │
│           v                    v                    v           │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                  AutoOperationBuilder                       ││
│  │  - Generates CRUD operations from ResourceSpec              ││
│  │  - Generates paging from OperationSpec                      ││
│  │  - Generates LRO polling from LROSpec                       ││
│  └─────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              v                                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                   Generated Operations                       ││
│  │  - get(), create_or_update(), delete()                      ││
│  │  - list(), list_by_resource_group()                         ││
│  │  - begin_create_or_update(), begin_delete()                 ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

---

## TypedDict Meta-Definitions

### Core TypedDict Definitions

```python
from __future__ import annotations

from typing import Any, Callable, Literal, Optional, Sequence, Type, TypedDict


class ParameterSpec(TypedDict, total=False):
    """Specification for an operation parameter."""
    
    name: str
    """The parameter name used in the method signature."""
    
    location: Literal["path", "query", "header", "body"]
    """Where the parameter appears in the HTTP request."""
    
    required: bool
    """Whether the parameter is required."""
    
    type: str
    """The Python type annotation as a string."""
    
    default: Any
    """Default value if the parameter is optional."""
    
    description: str
    """Documentation for the parameter."""


class OperationSpec(TypedDict, total=False):
    """Specification for a single API operation."""
    
    name: str
    """The operation method name."""
    
    http_method: Literal["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD"]
    """HTTP method for the operation."""
    
    url_template: str
    """URL template with path parameters in braces, e.g., '/subscriptions/{subscriptionId}/...'."""
    
    parameters: Sequence[ParameterSpec]
    """Parameters for the operation."""
    
    response_model: str
    """The response model type name."""
    
    description: str
    """Documentation for the operation."""


class PagingSpec(TypedDict, total=False):
    """Specification for paged operations."""
    
    item_name: str
    """The property name containing items in the response (e.g., 'value')."""
    
    next_link_name: str
    """The property name for the next page link (e.g., 'nextLink')."""
    
    continuation_token_name: str
    """Name of the continuation token parameter."""


class LROSpec(TypedDict, total=False):
    """Specification for Long-Running Operations."""
    
    polling_method: Literal["azure-async-operation", "location", "operation-location"]
    """The polling strategy to use."""
    
    final_state_via: Literal["azure-async-operation", "location", "original-uri"]
    """How to retrieve the final result."""
    
    polling_interval: int
    """Default polling interval in seconds."""
    
    timeout: int
    """Maximum operation timeout in seconds."""


class CRUDSpec(TypedDict, total=False):
    """Specification for CRUD operation generation."""
    
    get: OperationSpec | bool
    """GET operation specification or True to auto-generate."""
    
    create_or_update: OperationSpec | bool
    """PUT operation specification or True to auto-generate."""
    
    update: OperationSpec | bool
    """PATCH operation specification or True to auto-generate."""
    
    delete: OperationSpec | bool
    """DELETE operation specification or True to auto-generate."""
    
    list: OperationSpec | bool
    """List operation specification or True to auto-generate."""
    
    list_by_resource_group: OperationSpec | bool
    """List by resource group operation or True to auto-generate."""


class ResourceSpec(TypedDict, total=False):
    """Complete specification for an Azure resource type."""
    
    name: str
    """The resource type name (e.g., 'VirtualMachine', 'StorageAccount')."""
    
    provider_namespace: str
    """Azure resource provider namespace (e.g., 'Microsoft.Compute')."""
    
    resource_type: str
    """The ARM resource type (e.g., 'virtualMachines')."""
    
    api_version: str
    """API version for operations."""
    
    model_type: str
    """The Python model class name for this resource."""
    
    crud: CRUDSpec
    """CRUD operations configuration."""
    
    paging: PagingSpec
    """Paging configuration for list operations."""
    
    lro: LROSpec
    """Long-running operation configuration."""
    
    custom_operations: Sequence[OperationSpec]
    """Additional custom operations beyond CRUD."""
    
    scope: Literal["subscription", "resource_group", "resource", "tenant"]
    """The scope level at which this resource operates."""
```

---

## Example Resource Specifications

### Virtual Machine Resource Specification

```python
VIRTUAL_MACHINE_SPEC: ResourceSpec = {
    "name": "VirtualMachine",
    "provider_namespace": "Microsoft.Compute",
    "resource_type": "virtualMachines",
    "api_version": "2024-07-01",
    "model_type": "VirtualMachine",
    "scope": "resource_group",
    "crud": {
        "get": True,
        "create_or_update": True,
        "update": True,
        "delete": True,
        "list": True,
        "list_by_resource_group": True,
    },
    "paging": {
        "item_name": "value",
        "next_link_name": "nextLink",
    },
    "lro": {
        "polling_method": "azure-async-operation",
        "final_state_via": "azure-async-operation",
        "polling_interval": 30,
        "timeout": 3600,
    },
    "custom_operations": [
        {
            "name": "power_off",
            "http_method": "POST",
            "url_template": (
                "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}"
                "/providers/Microsoft.Compute/virtualMachines/{vmName}/powerOff"
            ),
            "parameters": [
                {"name": "resource_group_name", "location": "path", "required": True, "type": "str"},
                {"name": "vm_name", "location": "path", "required": True, "type": "str"},
                {"name": "skip_shutdown", "location": "query", "required": False, "type": "bool", "default": False},
            ],
            "description": "Power off (stop) a virtual machine.",
        },
        {
            "name": "start",
            "http_method": "POST",
            "url_template": (
                "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}"
                "/providers/Microsoft.Compute/virtualMachines/{vmName}/start"
            ),
            "parameters": [
                {"name": "resource_group_name", "location": "path", "required": True, "type": "str"},
                {"name": "vm_name", "location": "path", "required": True, "type": "str"},
            ],
            "description": "Start a virtual machine.",
        },
    ],
}
```

### Storage Account Resource Specification

```python
STORAGE_ACCOUNT_SPEC: ResourceSpec = {
    "name": "StorageAccount",
    "provider_namespace": "Microsoft.Storage",
    "resource_type": "storageAccounts",
    "api_version": "2023-05-01",
    "model_type": "StorageAccount",
    "scope": "resource_group",
    "crud": {
        "get": True,
        "create_or_update": {
            "name": "create",
            "http_method": "PUT",
            "url_template": (
                "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}"
                "/providers/Microsoft.Storage/storageAccounts/{accountName}"
            ),
            "parameters": [
                {"name": "resource_group_name", "location": "path", "required": True, "type": "str"},
                {"name": "account_name", "location": "path", "required": True, "type": "str"},
                {
                    "name": "parameters",
                    "location": "body",
                    "required": True,
                    "type": "StorageAccountCreateParameters",
                },
            ],
            "response_model": "StorageAccount",
            "description": "Creates or updates a storage account.",
        },
        "delete": True,
        "list": True,
        "list_by_resource_group": True,
    },
    "paging": {
        "item_name": "value",
        "next_link_name": "nextLink",
    },
    "lro": {
        "polling_method": "location",
        "final_state_via": "location",
        "polling_interval": 10,
        "timeout": 1800,
    },
    "custom_operations": [
        {
            "name": "list_keys",
            "http_method": "POST",
            "url_template": (
                "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}"
                "/providers/Microsoft.Storage/storageAccounts/{accountName}/listKeys"
            ),
            "parameters": [
                {"name": "resource_group_name", "location": "path", "required": True, "type": "str"},
                {"name": "account_name", "location": "path", "required": True, "type": "str"},
            ],
            "response_model": "StorageAccountListKeysResult",
            "description": "Lists the access keys for the storage account.",
        },
    ],
}
```

---

## Automated Resource Manager Code

### Base Resource Manager

```python
from __future__ import annotations

from typing import Any, Callable, Generic, Iterator, TypeVar

from azure.core.paging import ItemPaged
from azure.core.pipeline import PipelineClient
from azure.core.polling import LROPoller
from azure.core.rest import HttpRequest, HttpResponse
from azure.core.tracing.decorator import distributed_trace
from azure.mgmt.core.polling.arm_polling import ARMPolling


T = TypeVar("T")
ModelType = TypeVar("ModelType")


class AutoResourceManager(Generic[ModelType]):
    """Base class for auto-generated resource managers.
    
    This class uses the ResourceSpec TypedDict to automatically generate
    CRUD, paging, and LRO operations for Azure resources.
    """

    def __init__(
        self,
        client: PipelineClient,
        config: Any,
        serializer: Any,
        deserializer: Any,
        resource_spec: ResourceSpec,
    ) -> None:
        self._client = client
        self._config = config
        self._serialize = serializer
        self._deserialize = deserializer
        self._spec = resource_spec
        self._api_version = resource_spec.get("api_version", "")
        
    def _build_url(self, template: str, **kwargs: Any) -> str:
        """Build URL from template and parameters."""
        url = template
        url = url.replace("{subscriptionId}", self._config.subscription_id)
        for key, value in kwargs.items():
            # Convert snake_case to the URL parameter format
            url_key = self._to_camel_case(key)
            url = url.replace(f"{{{url_key}}}", str(value))
        return url
    
    @staticmethod
    def _to_camel_case(name: str) -> str:
        """Convert snake_case to camelCase."""
        components = name.split("_")
        return components[0] + "".join(x.title() for x in components[1:])

    def _get_base_url(self, resource_group_name: str, resource_name: str) -> str:
        """Generate the base URL for a specific resource."""
        provider = self._spec.get("provider_namespace", "")
        resource_type = self._spec.get("resource_type", "")
        return (
            f"/subscriptions/{{subscriptionId}}/resourceGroups/{resource_group_name}"
            f"/providers/{provider}/{resource_type}/{resource_name}"
        )

    @distributed_trace
    def get(self, resource_group_name: str, resource_name: str, **kwargs: Any) -> ModelType:
        """Get a resource by name.
        
        :param resource_group_name: The name of the resource group.
        :type resource_group_name: str
        :param resource_name: The name of the resource.
        :type resource_name: str
        :return: The resource instance.
        :rtype: ModelType
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        crud = self._spec.get("crud", {})
        if not crud.get("get"):
            raise NotImplementedError("GET operation not supported for this resource")
            
        url = self._get_base_url(resource_group_name, resource_name)
        request = self._build_request("GET", url, **kwargs)
        response = self._send_request(request)
        return self._deserialize(self._spec.get("model_type", ""), response)

    @distributed_trace
    def create_or_update(
        self,
        resource_group_name: str,
        resource_name: str,
        parameters: ModelType,
        **kwargs: Any,
    ) -> ModelType:
        """Create or update a resource.
        
        :param resource_group_name: The name of the resource group.
        :type resource_group_name: str
        :param resource_name: The name of the resource.
        :type resource_name: str
        :param parameters: The resource parameters.
        :type parameters: ModelType
        :return: The created or updated resource.
        :rtype: ModelType
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        crud = self._spec.get("crud", {})
        if not crud.get("create_or_update"):
            raise NotImplementedError("CREATE_OR_UPDATE operation not supported")
            
        url = self._get_base_url(resource_group_name, resource_name)
        body = self._serialize.body(parameters, self._spec.get("model_type", ""))
        request = self._build_request("PUT", url, json=body, **kwargs)
        response = self._send_request(request)
        return self._deserialize(self._spec.get("model_type", ""), response)

    @distributed_trace
    def begin_create_or_update(
        self,
        resource_group_name: str,
        resource_name: str,
        parameters: ModelType,
        **kwargs: Any,
    ) -> LROPoller[ModelType]:
        """Begin creating or updating a resource (LRO).
        
        :param resource_group_name: The name of the resource group.
        :type resource_group_name: str
        :param resource_name: The name of the resource.
        :type resource_name: str
        :param parameters: The resource parameters.
        :type parameters: ModelType
        :return: An LROPoller for the operation.
        :rtype: ~azure.core.polling.LROPoller[ModelType]
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        lro_spec = self._spec.get("lro", {})
        polling_interval = lro_spec.get("polling_interval", 30)
        
        def get_long_running_output(response: HttpResponse) -> ModelType:
            return self._deserialize(self._spec.get("model_type", ""), response)
        
        url = self._get_base_url(resource_group_name, resource_name)
        body = self._serialize.body(parameters, self._spec.get("model_type", ""))
        request = self._build_request("PUT", url, json=body, **kwargs)
        
        return LROPoller(
            self._client,
            request,
            get_long_running_output,
            ARMPolling(polling_interval),
        )

    @distributed_trace
    def delete(self, resource_group_name: str, resource_name: str, **kwargs: Any) -> None:
        """Delete a resource.
        
        :param resource_group_name: The name of the resource group.
        :type resource_group_name: str
        :param resource_name: The name of the resource.
        :type resource_name: str
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        crud = self._spec.get("crud", {})
        if not crud.get("delete"):
            raise NotImplementedError("DELETE operation not supported for this resource")
            
        url = self._get_base_url(resource_group_name, resource_name)
        request = self._build_request("DELETE", url, **kwargs)
        self._send_request(request)

    @distributed_trace
    def begin_delete(
        self,
        resource_group_name: str,
        resource_name: str,
        **kwargs: Any,
    ) -> LROPoller[None]:
        """Begin deleting a resource (LRO).
        
        :param resource_group_name: The name of the resource group.
        :type resource_group_name: str
        :param resource_name: The name of the resource.
        :type resource_name: str
        :return: An LROPoller for the operation.
        :rtype: ~azure.core.polling.LROPoller[None]
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        lro_spec = self._spec.get("lro", {})
        polling_interval = lro_spec.get("polling_interval", 30)
        
        url = self._get_base_url(resource_group_name, resource_name)
        request = self._build_request("DELETE", url, **kwargs)
        
        return LROPoller(
            self._client,
            request,
            lambda _: None,
            ARMPolling(polling_interval),
        )

    @distributed_trace
    def list(self, **kwargs: Any) -> ItemPaged[ModelType]:
        """List all resources in the subscription.
        
        :return: An iterator of resources.
        :rtype: ~azure.core.paging.ItemPaged[ModelType]
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        crud = self._spec.get("crud", {})
        if not crud.get("list"):
            raise NotImplementedError("LIST operation not supported for this resource")
        
        paging_spec = self._spec.get("paging", {})
        item_name = paging_spec.get("item_name", "value")
        next_link_name = paging_spec.get("next_link_name", "nextLink")
        
        provider = self._spec.get("provider_namespace", "")
        resource_type = self._spec.get("resource_type", "")
        url = f"/subscriptions/{{subscriptionId}}/providers/{provider}/{resource_type}"
        
        return self._create_paged_result(url, item_name, next_link_name, **kwargs)

    @distributed_trace
    def list_by_resource_group(
        self, 
        resource_group_name: str, 
        **kwargs: Any,
    ) -> ItemPaged[ModelType]:
        """List all resources in a resource group.
        
        :param resource_group_name: The name of the resource group.
        :type resource_group_name: str
        :return: An iterator of resources.
        :rtype: ~azure.core.paging.ItemPaged[ModelType]
        :raises ~azure.core.exceptions.HttpResponseError:
        """
        crud = self._spec.get("crud", {})
        if not crud.get("list_by_resource_group"):
            raise NotImplementedError("LIST_BY_RESOURCE_GROUP not supported")
        
        paging_spec = self._spec.get("paging", {})
        item_name = paging_spec.get("item_name", "value")
        next_link_name = paging_spec.get("next_link_name", "nextLink")
        
        provider = self._spec.get("provider_namespace", "")
        resource_type = self._spec.get("resource_type", "")
        url = (
            f"/subscriptions/{{subscriptionId}}/resourceGroups/{resource_group_name}"
            f"/providers/{provider}/{resource_type}"
        )
        
        return self._create_paged_result(url, item_name, next_link_name, **kwargs)

    def _build_request(
        self,
        method: str,
        url: str,
        **kwargs: Any,
    ) -> HttpRequest:
        """Build an HTTP request."""
        full_url = self._build_url(url)
        params = {"api-version": self._api_version}
        params.update(kwargs.pop("params", {}))
        return HttpRequest(method=method, url=full_url, params=params, **kwargs)

    def _send_request(self, request: HttpRequest) -> HttpResponse:
        """Send an HTTP request and handle the response."""
        pipeline_response = self._client._pipeline.run(request, stream=False)
        response = pipeline_response.http_response
        if response.status_code >= 400:
            from azure.core.exceptions import HttpResponseError
            raise HttpResponseError(response=response)
        return response

    def _create_paged_result(
        self,
        url: str,
        item_name: str,
        next_link_name: str,
        **kwargs: Any,
    ) -> ItemPaged[ModelType]:
        """Create a paged result iterator."""
        
        def get_next(next_link: str | None = None) -> dict[str, Any]:
            request_url = next_link or url
            request = self._build_request("GET", request_url, **kwargs)
            response = self._send_request(request)
            return response.json()

        def extract_data(response_data: dict[str, Any]) -> tuple[str | None, Iterator[ModelType]]:
            items = response_data.get(item_name, [])
            next_link = response_data.get(next_link_name)
            deserialized = [
                self._deserialize(self._spec.get("model_type", ""), item)
                for item in items
            ]
            return next_link, iter(deserialized)

        return ItemPaged(get_next, extract_data)
```

### Resource Manager Factory

```python
from __future__ import annotations

from typing import Any, Type


class ResourceManagerFactory:
    """Factory for creating resource managers from specifications."""

    def __init__(
        self,
        client: Any,
        config: Any,
        serializer: Any,
        deserializer: Any,
    ) -> None:
        self._client = client
        self._config = config
        self._serializer = serializer
        self._deserializer = deserializer
        self._managers: dict[str, AutoResourceManager[Any]] = {}

    def register(self, spec: ResourceSpec) -> None:
        """Register a resource specification.
        
        :param spec: The resource specification to register.
        :type spec: ResourceSpec
        """
        name = spec.get("name", "")
        self._managers[name] = AutoResourceManager(
            self._client,
            self._config,
            self._serializer,
            self._deserializer,
            spec,
        )

    def get_manager(self, resource_name: str) -> AutoResourceManager[Any]:
        """Get a resource manager by name.
        
        :param resource_name: The resource type name.
        :type resource_name: str
        :return: The resource manager.
        :rtype: AutoResourceManager
        :raises KeyError: If the resource is not registered.
        """
        if resource_name not in self._managers:
            raise KeyError(f"Resource '{resource_name}' is not registered")
        return self._managers[resource_name]

    def __getattr__(self, name: str) -> AutoResourceManager[Any]:
        """Allow attribute-style access to resource managers."""
        try:
            return self.get_manager(name)
        except KeyError:
            raise AttributeError(f"'{type(self).__name__}' has no resource '{name}'")
```

---

## Benefits

### 1. Reduced Boilerplate Code

Traditional approach requires hundreds of lines per resource for CRUD operations. With TypedDict specifications, a complete resource definition is ~50 lines that automatically generates all operations.

### 2. Consistency Across Resources

All resources follow the same patterns for:
- Error handling
- Paging behavior
- LRO polling
- Parameter validation

### 3. Type Safety

Full static type checking support:
- IDE autocompletion for specifications
- Compile-time validation of resource definitions
- Clear documentation of expected types

### 4. Easy Maintenance

Updating API versions or adding new operations requires only modifying the specification:
```python
# Example: Change API version
VIRTUAL_MACHINE_SPEC["api_version"] = "2024-07-01"

# Example: Add new custom operation
VIRTUAL_MACHINE_SPEC["custom_operations"].append({
    "name": "restart",
    "http_method": "POST",
    "url_template": ".../{vmName}/restart",
    # ...
})
```

### 5. Extensibility

New resource types can be added by:
1. Defining a `ResourceSpec` TypedDict
2. Registering with the factory
3. All operations are automatically available

### 6. Centralized Configuration

All resource metadata in one place:
- API versions
- URL templates
- Polling configurations
- Paging settings

---

## Practical Usage Example

### Setting Up the Client

```python
from azure.identity import DefaultAzureCredential
from azure.mgmt.core import ARMPipelineClient

# Initialize credentials and client
credential = DefaultAzureCredential()
subscription_id = "your-subscription-id"

# Create the pipeline client
client = ARMPipelineClient(
    base_url="https://management.azure.com",
    credential=credential,
)

# Create the resource manager factory
factory = ResourceManagerFactory(
    client=client,
    config={"subscription_id": subscription_id},
    serializer=Serializer(),
    deserializer=Deserializer(),
)

# Register resource specifications
factory.register(VIRTUAL_MACHINE_SPEC)
factory.register(STORAGE_ACCOUNT_SPEC)
```

### Working with Virtual Machines

```python
# Get the Virtual Machine manager
vm_manager = factory.VirtualMachine

# List all VMs in a resource group
for vm in vm_manager.list_by_resource_group("my-resource-group"):
    print(f"VM: {vm.name}, Location: {vm.location}")

# Get a specific VM
my_vm = vm_manager.get("my-resource-group", "my-vm-name")
print(f"VM ID: {my_vm.id}")

# Create a new VM (with LRO)
new_vm_params = VirtualMachine(
    location="eastus",
    hardware_profile={"vm_size": "Standard_DS2_v2"},
    # ... other parameters
)

poller = vm_manager.begin_create_or_update(
    "my-resource-group",
    "new-vm-name",
    new_vm_params,
)
result = poller.result()
print(f"Created VM: {result.name}")

# Delete a VM (with LRO)
delete_poller = vm_manager.begin_delete("my-resource-group", "old-vm-name")
delete_poller.wait()
print("VM deleted successfully")
```

### Working with Storage Accounts

```python
# Get the Storage Account manager
storage_manager = factory.StorageAccount

# Create a storage account
storage_params = StorageAccountCreateParameters(
    location="eastus",
    kind="StorageV2",
    sku={"name": "Standard_LRS"},
)

poller = storage_manager.begin_create_or_update(
    "my-resource-group",
    "mystorageaccount",
    storage_params,
)
account = poller.result()
print(f"Storage account created: {account.name}")

# List storage accounts
for account in storage_manager.list():
    print(f"Account: {account.name}, Location: {account.location}")
```

### Error Handling

```python
from azure.core.exceptions import HttpResponseError, ResourceNotFoundError

try:
    vm = vm_manager.get("my-resource-group", "non-existent-vm")
except ResourceNotFoundError:
    print("VM not found")
except HttpResponseError as e:
    print(f"HTTP error: {e.status_code} - {e.message}")
```

---

## Conclusion

The TypedDict-driven approach for Azure management SDKs provides:

- **Simplicity**: Declarative resource definitions replace boilerplate code
- **Safety**: Full type checking and IDE support
- **Consistency**: Uniform behavior across all resources
- **Maintainability**: Centralized configuration and easy updates
- **Extensibility**: New resources added through simple specifications

This design pattern significantly reduces the effort required to maintain and extend Azure management SDKs while improving code quality and developer experience.
