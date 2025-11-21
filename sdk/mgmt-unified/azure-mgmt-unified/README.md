# Azure Management Unified Client Library for Python

This package provides a unified interface to Azure Management Plane services, consolidating 100+ azure-mgmt-* packages into a single, consistent API.

## Features

- **Single Client Interface**: Access all Azure management services through one client
- **Service Routing**: Automatic routing to appropriate service based on operation
- **Consistent API**: Common CRUD operations across all services
- **Flexible API Versioning**: Default versions per service with easy overrides
- **Type Safety**: Full type hints and IntelliSense support
- **Lazy Loading**: Services loaded on-demand for optimal performance

## Installation

```bash
# Install core package
pip install azure-mgmt-unified

# Install with specific services
pip install azure-mgmt-unified[storage,compute,network]

# Install with all services
pip install azure-mgmt-unified[all]
```

## Quick Start

### Basic Usage

```python
from azure.identity import DefaultAzureCredential
from azure.mgmt.unified import UnifiedManagementClient, ServiceType

credential = DefaultAzureCredential()
subscription_id = "00000000-0000-0000-0000-000000000000"

# Create unified client
client = UnifiedManagementClient(credential, subscription_id)

# Use operations - automatic service detection
storage_accounts = client.storage_accounts.list()
virtual_machines = client.virtual_machines.list()
```

### Service-Specific Client

```python
# Create service-scoped client
storage_client = UnifiedManagementClient(
    credential, 
    subscription_id, 
    service=ServiceType.STORAGE
)

# All operations route to storage service
accounts = storage_client.storage_accounts.list()
```

### Custom API Versions

```python
# Override default API versions
client = UnifiedManagementClient(
    credential,
    subscription_id,
    api_versions={
        ServiceType.STORAGE: "2024-01-01",
        ServiceType.COMPUTE: "2023-09-01"
    }
)
```

## Architecture

This package uses a service-routing architecture where:

1. **ServiceType Enum** defines all supported Azure services
2. **Service Registry** maps operations to services and API versions
3. **Common Base Models** provide consistent resource properties
4. **Routing Layer** automatically directs operations to correct service
5. **Lazy Loading** loads service packages only when needed

## Design Goals

- Maintain backwards compatibility with existing azure-mgmt-* packages
- Provide intuitive single-client experience
- Support both service-scoped and multi-service usage
- Enable fine-grained API version control
- Minimize installation size through optional dependencies

## Status

⚠️ **Beta**: This package is under active development. APIs may change.

## Contributing

This project welcomes contributions. Please see [CONTRIBUTING.md](https://github.com/Azure/azure-sdk-for-python/blob/main/CONTRIBUTING.md).
