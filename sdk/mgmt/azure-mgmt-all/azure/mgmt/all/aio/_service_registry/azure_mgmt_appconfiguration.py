from typing import TYPE_CHECKING, Any, Optional, List, Dict, Union, cast, IO
from azure.core.paging import ItemPaged

from azure.core.polling import AsyncLROPoller
from azure.core.rest import AsyncHttpResponse
from .service_factory import AsyncServiceProviderFactory
from ..._models import (
    ApiKey, ApiKeyListResult, ConfigurationStore, ConfigurationStoreListResult
)

if TYPE_CHECKING:
    from .._client import AsyncManagementClient


class AsyncAppConfigurationFactory(AsyncServiceProviderFactory):
    """Async specialized factory for Microsoft.AppConfiguration resource provider.
    
    Provides typed operations and models for App Configuration service management.
    """
    
    def __init__(self, client: "AsyncManagementClient", service_provider: str, subscription_id: Optional[str] = None, api_version: Optional[str] = None):
        # Set default API version if none provided
        if api_version is None:
            api_version = "2023-03-01"
        super().__init__(client, service_provider, subscription_id, api_version)

    # Configuration Stores Operations
    
    async def list(self, skip_token: Optional[str] = None, **kwargs: Any) -> ItemPaged[ConfigurationStore]:
        """List all configuration stores in the subscription.
        
        :param skip_token: A skip token for pagination. Default is None.
        :type skip_token: Optional[str]
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: An iterator like instance of ConfigurationStore
        :rtype: ItemPaged[ConfigurationStore]
        """
        url = "configurationStores"
        if skip_token:
            url += f"?$skipToken={skip_token}"
        response = await super().get(url, **kwargs)
        response.raise_for_status()
        result = response.json()
        return cast(ItemPaged[ConfigurationStore], result.get('value', []))

    async def list_by_resource_group(self, resource_group_name: str, skip_token: Optional[str] = None, **kwargs: Any) -> ItemPaged[ConfigurationStore]:
        """List configuration stores in a resource group.
        
        :param resource_group_name: The name of the resource group.
        :type resource_group_name: str
        :param skip_token: A skip token for pagination. Default is None.
        :type skip_token: Optional[str]
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: An iterator like instance of ConfigurationStore
        :rtype: ItemPaged[ConfigurationStore]
        """
        url = f"resourceGroups/{resource_group_name}/providers/Microsoft.AppConfiguration/configurationStores"
        if skip_token:
            url += f"?$skipToken={skip_token}"
        response = await super().get(url, **kwargs)
        response.raise_for_status()
        result = response.json()
        return cast(ItemPaged[ConfigurationStore], result.get('value', []))

    async def get(self, resource_group_name: str, config_store_name: str, **kwargs: Any) -> ConfigurationStore:
        """Get properties of a configuration store.
        
        :param resource_group_name: The name of the resource group.
        :type resource_group_name: str
        :param config_store_name: The name of the configuration store.
        :type config_store_name: str
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: The configuration store properties
        :rtype: ConfigurationStore
        """
        response = await super().get(f"resourceGroups/{resource_group_name}/providers/Microsoft.AppConfiguration/configurationStores/{config_store_name}", **kwargs)
        response.raise_for_status()
        return cast(ConfigurationStore, response.json())

    async def begin_create(self, resource_group_name: str, config_store_name: str, config_store_creation_parameters: Union[ConfigurationStore, IO[bytes]], **kwargs: Any) -> AsyncLROPoller[ConfigurationStore]:
        """Create a configuration store with the specified parameters.
        
        :param resource_group_name: The name of the resource group.
        :type resource_group_name: str
        :param config_store_name: The name of the configuration store.
        :type config_store_name: str
        :param config_store_creation_parameters: The parameters for creating a configuration store.
        :type config_store_creation_parameters: Union[ConfigurationStore, IO[bytes]]
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: An async LRO poller for the create operation
        :rtype: AsyncLROPoller[ConfigurationStore]
        """
        response = await self.put(f"resourceGroups/{resource_group_name}/providers/Microsoft.AppConfiguration/configurationStores/{config_store_name}", model=config_store_creation_parameters, **kwargs)
        return self._create_lro_poller(response, **kwargs)

    async def begin_delete(self, resource_group_name: str, config_store_name: str, **kwargs: Any) -> AsyncLROPoller[None]:
        """Delete a configuration store.
        
        :param resource_group_name: The name of the resource group.
        :type resource_group_name: str
        :param config_store_name: The name of the configuration store.
        :type config_store_name: str
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: An async LRO poller for the delete operation
        :rtype: AsyncLROPoller[None]
        """
        response = await self.delete(f"resourceGroups/{resource_group_name}/providers/Microsoft.AppConfiguration/configurationStores/{config_store_name}", **kwargs)
        return await self._create_lro_poller(response, **kwargs)

    async def begin_update(self, resource_group_name: str, config_store_name: str, config_store_update_parameters: Union[Dict[str, Any], IO[bytes]], **kwargs: Any) -> AsyncLROPoller[ConfigurationStore]:
        """Update a configuration store with the specified parameters.
        
        :param resource_group_name: The name of the resource group.
        :type resource_group_name: str
        :param config_store_name: The name of the configuration store.
        :type config_store_name: str
        :param config_store_update_parameters: The parameters for updating a configuration store.
        :type config_store_update_parameters: Union[Dict[str, Any], IO[bytes]]
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: An async LRO poller for the update operation
        :rtype: AsyncLROPoller[ConfigurationStore]
        """
        response = await self.patch(f"resourceGroups/{resource_group_name}/providers/Microsoft.AppConfiguration/configurationStores/{config_store_name}", model=config_store_update_parameters, **kwargs)
        return self._create_lro_poller(response, **kwargs)

    async def list_keys(self, resource_group_name: str, config_store_name: str, skip_token: Optional[str] = None, **kwargs: Any) -> ItemPaged[ApiKey]:
        """List the access keys for the specified configuration store.
        
        :param resource_group_name: The name of the resource group.
        :type resource_group_name: str
        :param config_store_name: The name of the configuration store.
        :type config_store_name: str
        :param skip_token: A skip token for pagination. Default is None.
        :type skip_token: Optional[str]
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: An iterator like instance of ApiKey
        :rtype: ItemPaged[ApiKey]
        """
        url = f"resourceGroups/{resource_group_name}/providers/Microsoft.AppConfiguration/configurationStores/{config_store_name}/ListKeys"
        if skip_token:
            url += f"?$skipToken={skip_token}"
        response = await self.post(url, **kwargs)
        response.raise_for_status()
        result = response.json()
        return cast(ItemPaged[ApiKey], result.get('value', []))

    async def regenerate_key(self, resource_group_name: str, config_store_name: str, regenerate_key_parameters: Union[Dict[str, str], IO[bytes]], **kwargs: Any) -> ApiKey:
        """Regenerate an access key for the specified configuration store.
        
        :param resource_group_name: The name of the resource group.
        :type resource_group_name: str
        :param config_store_name: The name of the configuration store.
        :type config_store_name: str
        :param regenerate_key_parameters: The parameters for regenerating an access key.
        :type regenerate_key_parameters: Union[Dict[str, str], IO[bytes]]
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: The regenerated API key
        :rtype: ApiKey
        """
        response = await self.post(f"resourceGroups/{resource_group_name}/providers/Microsoft.AppConfiguration/configurationStores/{config_store_name}/RegenerateKey", model=regenerate_key_parameters, **kwargs)
        response.raise_for_status()
        return cast(ApiKey, response.json())

    async def list_deleted(self, **kwargs: Any) -> ItemPaged[Dict[str, Any]]:
        """List deleted configuration stores.
        
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: An iterator like instance of deleted configuration stores
        :rtype: ItemPaged[Dict[str, Any]]
        """
        response = await super().get("deletedConfigurationStores", **kwargs)
        response.raise_for_status()
        result = response.json()
        return cast(ItemPaged[Dict[str, Any]], result.get('value', []))

    async def get_deleted(self, location: str, config_store_name: str, **kwargs: Any) -> Dict[str, Any]:
        """Get properties of a deleted configuration store.
        
        :param location: The location of the deleted store.
        :type location: str
        :param config_store_name: The name of the configuration store.
        :type config_store_name: str
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: The deleted configuration store properties
        :rtype: Dict[str, Any]
        """
        response = await super().get(f"locations/{location}/deletedConfigurationStores/{config_store_name}", **kwargs)
        response.raise_for_status()
        return cast(Dict[str, Any], response.json())

    async def begin_purge_deleted(self, location: str, config_store_name: str, **kwargs: Any) -> AsyncLROPoller[None]:
        """Purge a deleted configuration store.
        
        :param location: The location of the deleted store.
        :type location: str
        :param config_store_name: The name of the configuration store.
        :type config_store_name: str
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: An async LRO poller for the purge operation
        :rtype: AsyncLROPoller[None]
        """
        response = await self.delete(f"locations/{location}/deletedConfigurationStores/{config_store_name}/purge", **kwargs)
        return await self._create_lro_poller(response, **kwargs)

    # KeyValues Operations
    
    async def get_key_value(self, resource_group_name: str, config_store_name: str, key_value_name: str, **kwargs: Any) -> Dict[str, Any]:
        """Get properties of a key-value.
        
        :param resource_group_name: The name of the resource group.
        :type resource_group_name: str
        :param config_store_name: The name of the configuration store.
        :type config_store_name: str
        :param key_value_name: The name of the key-value.
        :type key_value_name: str
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: The key-value properties
        :rtype: Dict[str, Any]
        """
        response = await super().get(f"resourceGroups/{resource_group_name}/providers/Microsoft.AppConfiguration/configurationStores/{config_store_name}/keyValues/{key_value_name}", **kwargs)
        response.raise_for_status()
        return cast(Dict[str, Any], response.json())

    async def create_or_update_key_value(self, resource_group_name: str, config_store_name: str, key_value_name: str, key_value_parameters: Union[Dict[str, Any], IO[bytes]], **kwargs: Any) -> Dict[str, Any]:
        """Create or update a key-value.
        
        :param resource_group_name: The name of the resource group.
        :type resource_group_name: str
        :param config_store_name: The name of the configuration store.
        :type config_store_name: str
        :param key_value_name: The name of the key-value.
        :type key_value_name: str
        :param key_value_parameters: The parameters for creating/updating a key-value.
        :type key_value_parameters: Union[Dict[str, Any], IO[bytes]]
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: The created/updated key-value
        :rtype: Dict[str, Any]
        """
        response = await self.put(f"resourceGroups/{resource_group_name}/providers/Microsoft.AppConfiguration/configurationStores/{config_store_name}/keyValues/{key_value_name}", model=key_value_parameters, **kwargs)
        response.raise_for_status()
        return cast(Dict[str, Any], response.json())

    async def begin_delete_key_value(self, resource_group_name: str, config_store_name: str, key_value_name: str, **kwargs: Any) -> AsyncLROPoller[None]:
        """Delete a key-value.
        
        :param resource_group_name: The name of the resource group.
        :type resource_group_name: str
        :param config_store_name: The name of the configuration store.
        :type config_store_name: str
        :param key_value_name: The name of the key-value.
        :type key_value_name: str
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: An async LRO poller for the delete operation
        :rtype: AsyncLROPoller[None]
        """
        response = await self.delete(f"resourceGroups/{resource_group_name}/providers/Microsoft.AppConfiguration/configurationStores/{config_store_name}/keyValues/{key_value_name}", **kwargs)
        return await self._create_lro_poller(response, **kwargs)

    # Additional async methods for Operations, Private Endpoint Connections, Private Link Resources, Replicas, and Snapshots
    # would follow the same pattern as above with async/await keywords
        """List configuration stores in a resource group.
        
        :param resource_group_name: The name of the resource group.
        :type resource_group_name: str
        :param skip_token: A skip token for pagination. Default is None.
        :type skip_token: Optional[str]
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: List result containing configuration stores
        :rtype: ConfigurationStoreListResult
        """
        url = f"resourceGroups/{resource_group_name}/providers/Microsoft.AppConfiguration/configurationStores"
        if skip_token:
            url += f"?$skipToken={skip_token}"
        response = await self.get(url, **kwargs)
        response.raise_for_status()
        return cast(ConfigurationStoreListResult, response.json())

    async def get(self, resource_group_name: str, config_store_name: str, **kwargs: Any) -> ConfigurationStore:
        """Get properties of a configuration store.
        
        :param resource_group_name: The name of the resource group.
        :type resource_group_name: str
        :param config_store_name: The name of the configuration store.
        :type config_store_name: str
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: The configuration store properties
        :rtype: ConfigurationStore
        """
        response = await super().get(f"resourceGroups/{resource_group_name}/providers/Microsoft.AppConfiguration/configurationStores/{config_store_name}", **kwargs)
        response.raise_for_status()
        return cast(ConfigurationStore, response.json())

    async def begin_create(self, resource_group_name: str, config_store_name: str, config_store_creation_parameters: ConfigurationStore, **kwargs: Any) -> AsyncLROPoller[ConfigurationStore]:
        """Create a configuration store with the specified parameters.
        
        :param resource_group_name: The name of the resource group.
        :type resource_group_name: str
        :param config_store_name: The name of the configuration store.
        :type config_store_name: str
        :param config_store_creation_parameters: The parameters for creating a configuration store.
        :type config_store_creation_parameters: ConfigurationStore
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: An async LRO poller for the create operation
        :rtype: AsyncLROPoller[ConfigurationStore]
        """
        response = await self.put(f"resourceGroups/{resource_group_name}/providers/Microsoft.AppConfiguration/configurationStores/{config_store_name}", model=config_store_creation_parameters, **kwargs)
        return self._create_lro_poller(response, **kwargs)

    async def create_configuration_store(self, resource_group_name: str, config_store_name: str, config_store_data: ConfigurationStore, **kwargs: Any) -> ConfigurationStore:
        """Create or update a configuration store (direct response, not polling).
        
        :param resource_group_name: The name of the resource group.
        :type resource_group_name: str
        :param config_store_name: The name of the configuration store.
        :type config_store_name: str
        :param config_store_data: The configuration store properties.
        :type config_store_data: ConfigurationStore
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: The created/updated configuration store
        :rtype: ConfigurationStore
        """
        response = await self.put(f"resourceGroups/{resource_group_name}/providers/Microsoft.AppConfiguration/configurationStores/{config_store_name}", model=config_store_data, **kwargs)
        response.raise_for_status()
        return cast(ConfigurationStore, response.json())

    async def begin_update(self, resource_group_name: str, config_store_name: str, config_store_update_parameters: Dict[str, Any], **kwargs: Any) -> AsyncLROPoller[ConfigurationStore]:
        """Update a configuration store with the specified parameters.
        
        :param resource_group_name: The name of the resource group.
        :type resource_group_name: str
        :param config_store_name: The name of the configuration store.
        :type config_store_name: str
        :param config_store_update_parameters: The parameters for updating a configuration store.
        :type config_store_update_parameters: Dict[str, Any]
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: An async LRO poller for the update operation
        :rtype: AsyncLROPoller[ConfigurationStore]
        """
        response = await self.patch(f"resourceGroups/{resource_group_name}/providers/Microsoft.AppConfiguration/configurationStores/{config_store_name}", model=config_store_update_parameters, **kwargs)
        return self._create_lro_poller(response, **kwargs)

    async def begin_delete(self, resource_group_name: str, config_store_name: str, **kwargs: Any) -> AsyncLROPoller[None]:
        """Delete a configuration store.
        
        :param resource_group_name: The name of the resource group.
        :type resource_group_name: str
        :param config_store_name: The name of the configuration store.
        :type config_store_name: str
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: An LRO poller for the delete operation
        :rtype: AsyncLROPoller[None]
        """
        response = await self.delete(f"resourceGroups/{resource_group_name}/providers/Microsoft.AppConfiguration/configurationStores/{config_store_name}", **kwargs)
        return await self._create_lro_poller(response, **kwargs)

    # API Keys operations

    async def list_keys(self, resource_group_name: str, config_store_name: str, skip_token: Optional[str] = None, **kwargs: Any) -> ApiKeyListResult:
        """List the access key for the specified configuration store.
        
        :param resource_group_name: The name of the resource group.
        :type resource_group_name: str
        :param config_store_name: The name of the configuration store.
        :type config_store_name: str
        :param skip_token: A skip token for pagination. Default is None.
        :type skip_token: Optional[str]
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: List of API keys
        :rtype: ApiKeyListResult
        """
        url = f"resourceGroups/{resource_group_name}/providers/Microsoft.AppConfiguration/configurationStores/{config_store_name}/ListKeys"
        if skip_token:
            url += f"?$skipToken={skip_token}"
        response = await self.post(url, **kwargs)
        response.raise_for_status()
        return cast(ApiKeyListResult, response.json())

    async def regenerate_key(self, resource_group_name: str, config_store_name: str, regenerate_key_parameters: Dict[str, str], **kwargs: Any) -> ApiKey:
        """Regenerate an access key for the specified configuration store.
        
        :param resource_group_name: The name of the resource group.
        :type resource_group_name: str
        :param config_store_name: The name of the configuration store.
        :type config_store_name: str
        :param regenerate_key_parameters: The parameters for regenerating an access key (e.g., {"id": "key_id"}).
        :type regenerate_key_parameters: Dict[str, str]
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: The regenerated API key
        :rtype: ApiKey
        """
        response = await self.post(f"resourceGroups/{resource_group_name}/providers/Microsoft.AppConfiguration/configurationStores/{config_store_name}/RegenerateKey", model=regenerate_key_parameters, **kwargs)
        response.raise_for_status()
        return cast(ApiKey, response.json())