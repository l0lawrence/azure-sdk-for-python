# Azure Mgmt All Package: Service Provider Factory Architecture

This document describes the architecture and flow of how the `azure-mgmt-all` package for the Azure SDK for Python is implemented, focusing on the service provider factory pattern.

## Architecture Diagram

```text
+-----------------------------+
|      ManagementClient       |
+-----------------------------+
             |
             | call with provider name
             V
+-----------------------------+
|     ServiceProviderFactory |
| (e.g. AppConfigurationFactory)|
+-----------------------------+
             |
     +-------+--------+
     | HTTP Operations|
     | (GET, POST,    |
     | PUT, PATCH,    |
     | DELETE)        |
     +-------+--------+
             |
   +---------+--------+
   | Typed Models     |
   | (ConfigurationStore,|
   | ApiKey, etc.)    |
   +------------------+

                    (Factory pattern for all resource providers)
```

## Flow Overview

1. **ManagementClient**  
   The main entry point that acts as a factory dispatcher. You call it with a service provider name to get a specialized factory.

2. **Service Provider Factories**  
   Dynamically created factories for specific resource providers (e.g., `"Microsoft.AppConfiguration"`). Each factory provides:
   - HTTP operations (GET, POST, PUT, PATCH, DELETE) 
    - Specialized methods for common operations
    - Typed models for request/response data
    - Route maps (`operations_by_method`, `operations_by_group`, `routes_by_method`) with dynamic dispatch

3. **HTTP Operations**  
   Low-level HTTP methods that automatically handle:
   - URL construction with subscription ID and provider namespace
   - API version management
   - Authentication and ARM pipeline integration

4. **Typed Models**  
   TypedDict classes that provide type hints for Azure resource data structures.

---

## Usage Example

### Synchronous Usage

```python
from azure.mgmt.all import ManagementClient
from azure.identity import DefaultAzureCredential

# Create the main management client
client = ManagementClient(
    credential=DefaultAzureCredential(),
    subscription_id="your-subscription-id"
)

# Get a factory for App Configuration service
app_config = client("Microsoft.AppConfiguration")

# Use HTTP operations directly
response = app_config.get("configurationStores")  # List all stores
response = app_config.get("configurationStores/mystore", resource_group="mygroup")  # Get specific store

# Create a new configuration store
store_data = {
    "location": "eastus", 
    "sku": {"name": "Standard"}
}
response = app_config.put("configurationStores/mystore", model=store_data, resource_group="mygroup")

# Use specialized methods (where available)
stores = app_config.list()  # List all configuration stores
store = app_config.get(
    resource_group_name="mygroup",
    config_store_name="mystore"
)

# Access by operation group
stores_group = app_config.configuration_stores
stores = stores_group.list()

# Dynamic dispatch via __getattr__ (falls back to routes_by_method)
replica = app_config.get_replica("rg1", "store1", "replicaA")

# Create with polling
poller = app_config.begin_create(
    resource_group_name="mygroup",
    config_store_name="mystore", 
    config_store_creation_parameters=store_data
)
result = poller.result()

# Create without polling
app_config.create_configuration_store(
    resource_group_name="mygroup",
    config_store_name="mystore", 
    config_store_data=store_data
)
```

### Asynchronous Usage

```python
import asyncio
from azure.mgmt.all.aio import AsyncManagementClient
from azure.identity.aio import DefaultAzureCredential

async def main():
    async with DefaultAzureCredential() as credential:
        client = AsyncManagementClient(
            credential=credential,
            subscription_id="your-subscription-id"
        )
        
        async with client:
            # Get a factory for App Configuration service
            app_config = client("Microsoft.AppConfiguration")

            # Use async HTTP operations
            response = await app_config.get("configurationStores")  # List all stores
            response = await app_config.get("configurationStores/mystore", resource_group="mygroup")

            # Create a new configuration store asynchronously
            store_data = {
                "location": "eastus", 
                "sku": {"name": "Standard"}
            }
            response = await app_config.put("configurationStores/mystore", model=store_data, resource_group="mygroup")

            # Use specialized async methods with LRO polling
            stores = await app_config.list()  # List all configuration stores
            store = await app_config.get(
                resource_group_name="mygroup",
                config_store_name="mystore"
            )

            # Create with polling
            poller = await app_config.begin_create(
                resource_group_name="mygroup",
                config_store_name="mystore",
                config_store_creation_parameters=store_data
            )
            result = await poller.result()

asyncio.run(main())
```

---

## Key Features

### Both Sync and Async Support
The package provides both synchronous and asynchronous clients:

- **ManagementClient**: Synchronous operations
- **AsyncManagementClient**: Asynchronous operations with `async`/`await` support

Both clients share the same API design and factory pattern.

### Dynamic Factory Registration
Both clients support registering new service provider factories:

```python
# Sync client
from azure.mgmt.all import ManagementClient
supported = ManagementClient.get_supported_providers()
ManagementClient.register_service_factory("Microsoft.Storage", StorageFactory)

# Async client  
from azure.mgmt.all.aio import AsyncManagementClient
supported = AsyncManagementClient.get_supported_providers()
AsyncManagementClient.register_service_factory("Microsoft.Storage", AsyncStorageFactory)
```

### Flexible API Version Support
Each factory call can specify a different API version:

```python
# Sync - use default API version for the service
app_config = client("Microsoft.AppConfiguration")

# Sync - use specific API version
app_config = client("Microsoft.AppConfiguration", api_version="2023-03-01")

# Async - use default API version
async_app_config = async_client("Microsoft.AppConfiguration")

# Async - use specific API version
async_app_config = async_client("Microsoft.AppConfiguration", api_version="2023-03-01")

# Override subscription ID for both
app_config = client("Microsoft.AppConfiguration", subscription_id="different-sub")
async_app_config = async_client("Microsoft.AppConfiguration", subscription_id="different-sub")
```

### Integrated ARM Pipeline
All requests go through the ARM pipeline with:
- Automatic authentication (sync and async)
- Resource provider auto-registration  
- Retry policies
- Logging and tracing
- Distributed tracing support
- Long Running Operation (LRO) support with polling

### Long Running Operations (LRO)
Both sync and async clients expose `begin_*` operations that now wrap HTTP responses with `_create_lro_poller`, so you always receive an `LROPoller` instead of a raw `HttpResponse`.

```python
# Async LRO with polling
poller = await app_config.begin_create_configuration_store(...)
result = await poller.result()  # Wait for completion

# Sync LRO (if implemented)
poller = app_config.begin_create_configuration_store(...)
result = poller.result()  # Wait for completion

# Dynamic begin_* also returns a poller via routes_by_method
poller = app_config.begin_create("rg1", "store1", {"location": "eastus"})
result = poller.result()
```

---

## Summary Table

| Layer                | Examples/Responsibilities                        | Async Support |
|----------------------|--------------------------------------------------|---------------|
| ManagementClient / AsyncManagementClient | Factory dispatcher, ARM pipeline management | ✅ Full async support |
| ServiceProviderFactory / AsyncServiceProviderFactory | HTTP operations, URL construction, API versioning | ✅ Full async support |
| HTTP Operations      | GET, POST, PUT, PATCH, DELETE with ARM integration | ✅ Full async support |
| LRO Operations       | Long running operations with polling | ✅ AsyncLROPoller support |
| Typed Models         | ConfigurationStore, ApiKey, Sku, etc.           | ✅ Shared models |

---

**References:**  
- See [demomgmt branch commits](https://github.com/l0lawrence/azure-sdk-for-python/commits?sha=demomgmt) for latest package updates.
- Design guidelines: [Azure SDK Python Design](https://azure.github.io/azure-sdk/python_design.html)
- Async guidelines: [Azure SDK Python Async Design](https://azure.github.io/azure-sdk/python_design.html#async-support)
