# Code Transparency Service client library for Python

The Azure Code Transparency Service provides a secure and verifiable way to record and retrieve code artifacts. This service helps establish trust in software by providing transparency about what code is being executed in your environment.

[Source code][source_code] | [Package (PyPI)][pypi] | [API reference documentation][api_docs] | [Product documentation][product_docs]

## Getting started

### Prerequisites

- Python 3.9 or later is required to use this package.
- You need an [Azure subscription][azure_sub] to use this package.
- An existing Code Transparency Service instance or resource.

### Install the package

```bash
python -m pip install azure-codetransparency
```

### Authenticate the client

To create a client for Code Transparency Service, you'll need to use the Azure Identity library to authenticate. The recommended approach is to use `DefaultAzureCredential`:

```python
from azure.identity import DefaultAzureCredential
from azure.codetransparency import CodeTransparencyClient

# Create an instance of the DefaultAzureCredential
credential = DefaultAzureCredential()
client = CodeTransparencyClient(endpoint="https://your-code-transparency-service.confidentialledger.azure.com", credential=credential)
```

## Key concepts

### Client

The `CodeTransparencyClient` is the primary interface for working with the Code Transparency Service. It provides methods for creating and retrieving entries, statements, and managing operations.

## Examples

### Creating an entry

```python
from azure.identity import DefaultAzureCredential
from azure.codetransparency import CodeTransparencyClient

endpoint = "https://your-code-transparency-service.confidentialledger.azure.com"
credential = DefaultAzureCredential()
client = CodeTransparencyClient(endpoint=endpoint, credential=credential)

# Create a binary entry
binary_data = b"Your binary content here"
response = client.create_entry(body=binary_data)
print(f"Operation ID: {response.operation_id}")
```

### Retrieving an entry

```python
from azure.identity import DefaultAzureCredential
from azure.codetransparency import CodeTransparencyClient

endpoint = "https://your-code-transparency-service.confidentialledger.azure.com"
credential = DefaultAzureCredential()
client = CodeTransparencyClient(endpoint=endpoint, credential=credential)

# Get an entry using its ID
entry_id = "your-entry-id"
entry = client.get_entry(entry_id=entry_id)
print(f"Entry content: {entry.value}")
```

## Contributing

This project welcomes contributions and suggestions. Most contributions require
you to agree to a Contributor License Agreement (CLA) declaring that you have
the right to, and actually do, grant us the rights to use your contribution.
For details, visit https://cla.microsoft.com.

When you submit a pull request, a CLA-bot will automatically determine whether
you need to provide a CLA and decorate the PR appropriately (e.g., label,
comment). Simply follow the instructions provided by the bot. You will only
need to do this once across all repos using our CLA.

This project has adopted the
[Microsoft Open Source Code of Conduct][code_of_conduct]. For more information,
see the Code of Conduct FAQ or contact opencode@microsoft.com with any
additional questions or comments.

<!-- LINKS -->
[source_code]: https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/confidentialledger/azure-codetransparency
[pypi]: https://pypi.org/project/azure-codetransparency
[api_docs]: https://docs.microsoft.com/python/api/azure-codetransparency
[product_docs]: https://docs.microsoft.com/azure/confidential-ledger/
[code_of_conduct]: https://opensource.microsoft.com/codeofconduct/
[azure_identity_credentials]: https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/identity/azure-identity#credentials
[azure_identity_pip]: https://pypi.org/project/azure-identity/
[default_azure_credential]: https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/identity/azure-identity#defaultazurecredential
[pip]: https://pypi.org/project/pip/
[azure_sub]: https://azure.microsoft.com/free/
