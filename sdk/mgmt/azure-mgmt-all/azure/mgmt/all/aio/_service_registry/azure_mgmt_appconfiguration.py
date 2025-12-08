from typing import TYPE_CHECKING, Any, Optional, List, Dict, Union, cast

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

    # Typed operations for Configuration Stores
    
    async def list(self, skip_token: Optional[str] = None, **kwargs: Any) -> ConfigurationStoreListResult:
        """List all configuration stores in the subscription.
        
        :param skip_token: A skip token for pagination. Default is None.
        :type skip_token: Optional[str]
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: List result containing configuration stores
        :rtype: ConfigurationStoreListResult
        """
        url = "configurationStores"
        if skip_token:
            url += f"?$skipToken={skip_token}"
        response = await self.get(url, **kwargs)
        response.raise_for_status()
        return cast(ConfigurationStoreListResult, response.json())

    async def list_by_resource_group(self, resource_group_name: str, skip_token: Optional[str] = None, **kwargs: Any) -> ConfigurationStoreListResult:
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