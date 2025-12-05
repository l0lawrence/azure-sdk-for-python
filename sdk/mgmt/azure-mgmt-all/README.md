# Azure Mgmt All Package: Resource Provider Architecture

This document describes the architecture and flow of how the `azure-mgmt-all` package for the Azure SDK for Python is implemented, focusing on resource providers.

## Architecture Diagram

```text
+-----------------------------+
|     azure-mgmt-all Client   |
+-----------------------------+
             |
             V
+----------------------+      +----------------------+      +----------------------+
| ComputeManagement    |      | StorageManagement    |  ... | <Other RP>Management |
| (e.g. compute_mgmt)  |      | (e.g. storage_mgmt)  |      | (e.g. network_mgmt)  |
+----------------------+      +----------------------+      +----------------------+
             |                        |                             |
     +-------+--------+        +------+-------+             +-------+------+
     | Operations     |        | Operations  |             | Operations   |
     | (methods for   |        | (methods    |             | (methods     |
     | VMs, etc.)     |        | for Storage)|             | for provider)|
     +-------+--------+        +------+-------+             +-------+------+
             |                        |                             |
   +---------+--------+       +-------+---------+          +--------+-------+
   | Models (e.g. VM, |       | Models (Blob,  |          | Models (Custom) |
   | Disk, Image)     |       | Container)     |          |                |
   +------------------+       +----------------+          +----------------+

                               (shared flow for all resource providers)
```

## Flow Overview

1. **azure-mgmt-all Client**  
   The main entry point. This aggregates all Azure management clients into a unified surface.

2. **Resource Provider (RP) Management Clients**  
   Examples include:
   - `ComputeManagement` (`compute_mgmt`)
   - `StorageManagement` (`storage_mgmt`)
   - `NetworkManagement` (`network_mgmt`)
   Each manages its respective resource types.

3. **Operations Classes**  
   Each RP exposes a set of operations (methods) that allow management of Azure resources—such as Create, Update, Delete, and List operations.

4. **Models**  
   Typed classes that represent Azure resources. Used as input/output for the RP operations.

---

## Usage Example

```python
from azure_mgmt_all import AzureMgmtAllClient

client = AzureMgmtAllClient(credentials)

# Compute RP Example
vm_ops = client.compute_mgmt.virtual_machines
vm = vm_ops.get(resource_group="rg", vm_name="foo")
vm_ops.create_or_update(resource_group="rg", vm_name="newvm", parameters=...)

# Storage RP Example
storage_ops = client.storage_mgmt.storage_accounts
accounts = storage_ops.list(resource_group="rg")
storage_ops.create(resource_group="rg", account_name="bar", parameters=...)
```

---

## Summary Table

| Layer                | Examples/Responsibilities                        |
|----------------------|--------------------------------------------------|
| azure-mgmt-all Client| Aggregates all RP clients                        |
| RP Management Client | compute_mgmt, storage_mgmt, network_mgmt, etc.   |
| Operations           | create, get, update, delete per RP resource      |
| Models               | VirtualMachine, StorageAccount, Network, etc.    |

---

**References:**  
- See [demomgmt branch commits](https://github.com/l0lawrence/azure-sdk-for-python/commits?sha=demomgmt) for latest package updates.
- Design guidelines: [Azure SDK Python Design](https://azure.github.io/azure-sdk/python_design.html)
