from typing import TYPE_CHECKING, Any, Optional, List, Dict, Union, cast, IO
from azure.core.paging import ItemPaged

from azure.core.polling import LROPoller
from azure.core.rest import HttpResponse
from .service_factory import ServiceProviderFactory
from ..models.azure_mgmt_appconfiguration import (
    ApiKey, ApiKeyListResult, ConfigurationStore, ConfigurationStoreListResult
)

if TYPE_CHECKING:
    from .._client import ManagementClient


class AppConfigurationFactory(ServiceProviderFactory):
    """Specialized factory for Microsoft.AppConfiguration resource provider.
    
    Provides typed operations and models for App Configuration service management.
    """
    
    def __init__(self, client: "ManagementClient", service_provider: str, subscription_id: Optional[str] = None, api_version: Optional[str] = None):
        # Set default API version if none provided
        if api_version is None:
            api_version = "2023-03-01"
        super().__init__(client, service_provider, subscription_id, api_version)

    # Configuration Stores Operations
    
    def list(self, skip_token: Optional[str] = None, **kwargs: Any) -> ItemPaged[ConfigurationStore]:
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
        response = super().get(url, **kwargs)
        response.raise_for_status()
        # For now, return a simple cast - in a full implementation this would be proper ItemPaged
        result = response.json()
        return cast(ItemPaged[ConfigurationStore], result.get('value', []))

    def list_by_resource_group(self, resource_group_name: str, skip_token: Optional[str] = None, **kwargs: Any) -> ItemPaged[ConfigurationStore]:
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
        response = super().get(url, **kwargs)
        response.raise_for_status()
        result = response.json()
        return cast(ItemPaged[ConfigurationStore], result.get('value', []))

    # would be get but overload wont work here 
    def get_configuration_store(self, resource_group_name: str, config_store_name: str, **kwargs: Any) -> ConfigurationStore:
        """Get properties of a configuration store.
        
        :param resource_group_name: The name of the resource group.
        :type resource_group_name: str
        :param config_store_name: The name of the configuration store.
        :type config_store_name: str
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: The configuration store properties
        :rtype: ConfigurationStore
        """
        response = super().get(f"resourceGroups/{resource_group_name}/providers/Microsoft.AppConfiguration/configurationStores/{config_store_name}", **kwargs)
        response.raise_for_status()
        return cast(ConfigurationStore, response.json())

    def begin_create(self, resource_group_name: str, config_store_name: str, config_store_creation_parameters: Union[ConfigurationStore, IO[bytes]], **kwargs: Any) -> LROPoller[ConfigurationStore]:
        """Create a configuration store with the specified parameters.
        
        :param resource_group_name: The name of the resource group.
        :type resource_group_name: str
        :param config_store_name: The name of the configuration store.
        :type config_store_name: str
        :param config_store_creation_parameters: The parameters for creating a configuration store.
        :type config_store_creation_parameters: Union[ConfigurationStore, IO[bytes]]
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: An LRO poller for the create operation
        :rtype: LROPoller[ConfigurationStore]
        """
        response = self.put(f"resourceGroups/{resource_group_name}/providers/Microsoft.AppConfiguration/configurationStores/{config_store_name}", model=config_store_creation_parameters, **kwargs)
        return self._create_lro_poller(response, **kwargs)

    def begin_delete(self, resource_group_name: str, config_store_name: str, **kwargs: Any) -> LROPoller[None]:
        """Delete a configuration store.
        
        :param resource_group_name: The name of the resource group.
        :type resource_group_name: str
        :param config_store_name: The name of the configuration store.
        :type config_store_name: str
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: An LRO poller for the delete operation
        :rtype: LROPoller[None]
        """
        response = self.delete(f"resourceGroups/{resource_group_name}/providers/Microsoft.AppConfiguration/configurationStores/{config_store_name}", **kwargs)
        return self._create_lro_poller(response, **kwargs)

    def begin_update(self, resource_group_name: str, config_store_name: str, config_store_update_parameters: Union[Dict[str, Any], IO[bytes]], **kwargs: Any) -> LROPoller[ConfigurationStore]:
        """Update a configuration store with the specified parameters.
        
        :param resource_group_name: The name of the resource group.
        :type resource_group_name: str
        :param config_store_name: The name of the configuration store.
        :type config_store_name: str
        :param config_store_update_parameters: The parameters for updating a configuration store.
        :type config_store_update_parameters: Union[Dict[str, Any], IO[bytes]]
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: An LRO poller for the update operation
        :rtype: LROPoller[ConfigurationStore]
        """
        response = self.patch(f"resourceGroups/{resource_group_name}/providers/Microsoft.AppConfiguration/configurationStores/{config_store_name}", model=config_store_update_parameters, **kwargs)
        return self._create_lro_poller(response, **kwargs)

    def list_keys(self, resource_group_name: str, config_store_name: str, skip_token: Optional[str] = None, **kwargs: Any) -> ItemPaged[ApiKey]:
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
        response = self.post(url, **kwargs)
        response.raise_for_status()
        result = response.json()
        return cast(ItemPaged[ApiKey], result.get('value', []))

    def regenerate_key(self, resource_group_name: str, config_store_name: str, regenerate_key_parameters: Union[Dict[str, str], IO[bytes]], **kwargs: Any) -> ApiKey:
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
        response = self.post(f"resourceGroups/{resource_group_name}/providers/Microsoft.AppConfiguration/configurationStores/{config_store_name}/RegenerateKey", model=regenerate_key_parameters, **kwargs)
        response.raise_for_status()
        return cast(ApiKey, response.json())

    def list_deleted(self, **kwargs: Any) -> ItemPaged[Dict[str, Any]]:
        """List deleted configuration stores.
        
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: An iterator like instance of deleted configuration stores
        :rtype: ItemPaged[Dict[str, Any]]
        """
        response = super().get("deletedConfigurationStores", **kwargs)
        response.raise_for_status()
        result = response.json()
        return cast(ItemPaged[Dict[str, Any]], result.get('value', []))

    def get_deleted(self, location: str, config_store_name: str, **kwargs: Any) -> Dict[str, Any]:
        """Get properties of a deleted configuration store.
        
        :param location: The location of the deleted store.
        :type location: str
        :param config_store_name: The name of the configuration store.
        :type config_store_name: str
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: The deleted configuration store properties
        :rtype: Dict[str, Any]
        """
        response = super().get(f"locations/{location}/deletedConfigurationStores/{config_store_name}", **kwargs)
        response.raise_for_status()
        return cast(Dict[str, Any], response.json())

    def begin_purge_deleted(self, location: str, config_store_name: str, **kwargs: Any) -> LROPoller[None]:
        """Purge a deleted configuration store.
        
        :param location: The location of the deleted store.
        :type location: str
        :param config_store_name: The name of the configuration store.
        :type config_store_name: str
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: An LRO poller for the purge operation
        :rtype: LROPoller[None]
        """
        response = self.delete(f"locations/{location}/deletedConfigurationStores/{config_store_name}/purge", **kwargs)
        return self._create_lro_poller(response, **kwargs)

    # KeyValues Operations
    
    def get_key_value(self, resource_group_name: str, config_store_name: str, key_value_name: str, **kwargs: Any) -> Dict[str, Any]:
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
        response = super().get(f"resourceGroups/{resource_group_name}/providers/Microsoft.AppConfiguration/configurationStores/{config_store_name}/keyValues/{key_value_name}", **kwargs)
        response.raise_for_status()
        return cast(Dict[str, Any], response.json())

    def create_or_update_key_value(self, resource_group_name: str, config_store_name: str, key_value_name: str, key_value_parameters: Union[Dict[str, Any], IO[bytes]], **kwargs: Any) -> Dict[str, Any]:
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
        response = self.put(f"resourceGroups/{resource_group_name}/providers/Microsoft.AppConfiguration/configurationStores/{config_store_name}/keyValues/{key_value_name}", model=key_value_parameters, **kwargs)
        response.raise_for_status()
        return cast(Dict[str, Any], response.json())

    def begin_delete_key_value(self, resource_group_name: str, config_store_name: str, key_value_name: str, **kwargs: Any) -> LROPoller[None]:
        """Delete a key-value.
        
        :param resource_group_name: The name of the resource group.
        :type resource_group_name: str
        :param config_store_name: The name of the configuration store.
        :type config_store_name: str
        :param key_value_name: The name of the key-value.
        :type key_value_name: str
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: An LRO poller for the delete operation
        :rtype: LROPoller[None]
        """
        response = self.delete(f"resourceGroups/{resource_group_name}/providers/Microsoft.AppConfiguration/configurationStores/{config_store_name}/keyValues/{key_value_name}", **kwargs)
        return self._create_lro_poller(response, **kwargs)

    # Operations
    
    def check_name_availability(self, check_name_availability_parameters: Union[Dict[str, Any], IO[bytes]], **kwargs: Any) -> Dict[str, Any]:
        """Check name availability.
        
        :param check_name_availability_parameters: The parameters for checking name availability.
        :type check_name_availability_parameters: Union[Dict[str, Any], IO[bytes]]
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: The name availability status
        :rtype: Dict[str, Any]
        """
        response = self.post("checkNameAvailability", model=check_name_availability_parameters, **kwargs)
        response.raise_for_status()
        return cast(Dict[str, Any], response.json())

    def list_operations(self, skip_token: Optional[str] = None, **kwargs: Any) -> ItemPaged[Dict[str, Any]]:
        """List operations available for App Configuration.
        
        :param skip_token: A skip token for pagination. Default is None.
        :type skip_token: Optional[str]
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: An iterator like instance of operation definitions
        :rtype: ItemPaged[Dict[str, Any]]
        """
        url = "/providers/Microsoft.AppConfiguration/operations"
        if skip_token:
            url += f"?$skipToken={skip_token}"
        response = super().get(url, **kwargs)
        response.raise_for_status()
        result = response.json()
        return cast(ItemPaged[Dict[str, Any]], result.get('value', []))

    def regional_check_name_availability(self, location: str, check_name_availability_parameters: Union[Dict[str, Any], IO[bytes]], **kwargs: Any) -> Dict[str, Any]:
        """Check name availability in a specific region.
        
        :param location: The location/region.
        :type location: str
        :param check_name_availability_parameters: The parameters for checking name availability.
        :type check_name_availability_parameters: Union[Dict[str, Any], IO[bytes]]
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: The name availability status
        :rtype: Dict[str, Any]
        """
        response = self.post(f"locations/{location}/checkNameAvailability", model=check_name_availability_parameters, **kwargs)
        response.raise_for_status()
        return cast(Dict[str, Any], response.json())

    # Private Endpoint Connections
    
    def list_private_endpoint_connections(self, resource_group_name: str, config_store_name: str, **kwargs: Any) -> ItemPaged[Dict[str, Any]]:
        """List private endpoint connections for a configuration store.
        
        :param resource_group_name: The name of the resource group.
        :type resource_group_name: str
        :param config_store_name: The name of the configuration store.
        :type config_store_name: str
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: An iterator like instance of private endpoint connections
        :rtype: ItemPaged[Dict[str, Any]]
        """
        response = super().get(f"resourceGroups/{resource_group_name}/providers/Microsoft.AppConfiguration/configurationStores/{config_store_name}/privateEndpointConnections", **kwargs)
        response.raise_for_status()
        result = response.json()
        return cast(ItemPaged[Dict[str, Any]], result.get('value', []))

    def get_private_endpoint_connection(self, resource_group_name: str, config_store_name: str, private_endpoint_connection_name: str, **kwargs: Any) -> Dict[str, Any]:
        """Get properties of a private endpoint connection.
        
        :param resource_group_name: The name of the resource group.
        :type resource_group_name: str
        :param config_store_name: The name of the configuration store.
        :type config_store_name: str
        :param private_endpoint_connection_name: The name of the private endpoint connection.
        :type private_endpoint_connection_name: str
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: The private endpoint connection properties
        :rtype: Dict[str, Any]
        """
        response = super().get(f"resourceGroups/{resource_group_name}/providers/Microsoft.AppConfiguration/configurationStores/{config_store_name}/privateEndpointConnections/{private_endpoint_connection_name}", **kwargs)
        response.raise_for_status()
        return cast(Dict[str, Any], response.json())

    def begin_create_or_update_private_endpoint_connection(self, resource_group_name: str, config_store_name: str, private_endpoint_connection_name: str, private_endpoint_connection: Union[Dict[str, Any], IO[bytes]], **kwargs: Any) -> LROPoller[Dict[str, Any]]:
        """Create or update a private endpoint connection.
        
        :param resource_group_name: The name of the resource group.
        :type resource_group_name: str
        :param config_store_name: The name of the configuration store.
        :type config_store_name: str
        :param private_endpoint_connection_name: The name of the private endpoint connection.
        :type private_endpoint_connection_name: str
        :param private_endpoint_connection: The private endpoint connection parameters.
        :type private_endpoint_connection: Union[Dict[str, Any], IO[bytes]]
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: An LRO poller for the create/update operation
        :rtype: LROPoller[Dict[str, Any]]
        """
        response = self.put(f"resourceGroups/{resource_group_name}/providers/Microsoft.AppConfiguration/configurationStores/{config_store_name}/privateEndpointConnections/{private_endpoint_connection_name}", model=private_endpoint_connection, **kwargs)
        return self._create_lro_poller(response, **kwargs)

    def begin_delete_private_endpoint_connection(self, resource_group_name: str, config_store_name: str, private_endpoint_connection_name: str, **kwargs: Any) -> LROPoller[None]:
        """Delete a private endpoint connection.
        
        :param resource_group_name: The name of the resource group.
        :type resource_group_name: str
        :param config_store_name: The name of the configuration store.
        :type config_store_name: str
        :param private_endpoint_connection_name: The name of the private endpoint connection.
        :type private_endpoint_connection_name: str
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: An LRO poller for the delete operation
        :rtype: LROPoller[None]
        """
        response = self.delete(f"resourceGroups/{resource_group_name}/providers/Microsoft.AppConfiguration/configurationStores/{config_store_name}/privateEndpointConnections/{private_endpoint_connection_name}", **kwargs)
        return self._create_lro_poller(response, **kwargs)

    # Private Link Resources
    
    def list_private_link_resources(self, resource_group_name: str, config_store_name: str, **kwargs: Any) -> ItemPaged[Dict[str, Any]]:
        """List private link resources for a configuration store.
        
        :param resource_group_name: The name of the resource group.
        :type resource_group_name: str
        :param config_store_name: The name of the configuration store.
        :type config_store_name: str
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: An iterator like instance of private link resources
        :rtype: ItemPaged[Dict[str, Any]]
        """
        response = super().get(f"resourceGroups/{resource_group_name}/providers/Microsoft.AppConfiguration/configurationStores/{config_store_name}/privateLinkResources", **kwargs)
        response.raise_for_status()
        result = response.json()
        return cast(ItemPaged[Dict[str, Any]], result.get('value', []))

    def get_private_link_resource(self, resource_group_name: str, config_store_name: str, group_name: str, **kwargs: Any) -> Dict[str, Any]:
        """Get properties of a private link resource.
        
        :param resource_group_name: The name of the resource group.
        :type resource_group_name: str
        :param config_store_name: The name of the configuration store.
        :type config_store_name: str
        :param group_name: The name of the private link resource group.
        :type group_name: str
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: The private link resource properties
        :rtype: Dict[str, Any]
        """
        response = super().get(f"resourceGroups/{resource_group_name}/providers/Microsoft.AppConfiguration/configurationStores/{config_store_name}/privateLinkResources/{group_name}", **kwargs)
        response.raise_for_status()
        return cast(Dict[str, Any], response.json())

    # Replicas Operations
    
    def list_replicas(self, resource_group_name: str, config_store_name: str, skip_token: Optional[str] = None, **kwargs: Any) -> ItemPaged[Dict[str, Any]]:
        """List replicas for a configuration store.
        
        :param resource_group_name: The name of the resource group.
        :type resource_group_name: str
        :param config_store_name: The name of the configuration store.
        :type config_store_name: str
        :param skip_token: A skip token for pagination. Default is None.
        :type skip_token: Optional[str]
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: An iterator like instance of replicas
        :rtype: ItemPaged[Dict[str, Any]]
        """
        url = f"resourceGroups/{resource_group_name}/providers/Microsoft.AppConfiguration/configurationStores/{config_store_name}/replicas"
        if skip_token:
            url += f"?$skipToken={skip_token}"
        response = super().get(url, **kwargs)
        response.raise_for_status()
        result = response.json()
        return cast(ItemPaged[Dict[str, Any]], result.get('value', []))

    def get_replica(self, resource_group_name: str, config_store_name: str, replica_name: str, **kwargs: Any) -> Dict[str, Any]:
        """Get properties of a replica.
        
        :param resource_group_name: The name of the resource group.
        :type resource_group_name: str
        :param config_store_name: The name of the configuration store.
        :type config_store_name: str
        :param replica_name: The name of the replica.
        :type replica_name: str
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: The replica properties
        :rtype: Dict[str, Any]
        """
        response = super().get(f"resourceGroups/{resource_group_name}/providers/Microsoft.AppConfiguration/configurationStores/{config_store_name}/replicas/{replica_name}", **kwargs)
        response.raise_for_status()
        return cast(Dict[str, Any], response.json())

    def begin_create_replica(self, resource_group_name: str, config_store_name: str, replica_name: str, replica_creation_parameters: Union[Dict[str, Any], IO[bytes]], **kwargs: Any) -> LROPoller[Dict[str, Any]]:
        """Create a replica.
        
        :param resource_group_name: The name of the resource group.
        :type resource_group_name: str
        :param config_store_name: The name of the configuration store.
        :type config_store_name: str
        :param replica_name: The name of the replica.
        :type replica_name: str
        :param replica_creation_parameters: The parameters for creating a replica.
        :type replica_creation_parameters: Union[Dict[str, Any], IO[bytes]]
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: An LRO poller for the create operation
        :rtype: LROPoller[Dict[str, Any]]
        """
        response = self.put(f"resourceGroups/{resource_group_name}/providers/Microsoft.AppConfiguration/configurationStores/{config_store_name}/replicas/{replica_name}", model=replica_creation_parameters, **kwargs)
        return self._create_lro_poller(response, **kwargs)

    def begin_delete_replica(self, resource_group_name: str, config_store_name: str, replica_name: str, **kwargs: Any) -> LROPoller[None]:
        """Delete a replica.
        
        :param resource_group_name: The name of the resource group.
        :type resource_group_name: str
        :param config_store_name: The name of the configuration store.
        :type config_store_name: str
        :param replica_name: The name of the replica.
        :type replica_name: str
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: An LRO poller for the delete operation
        :rtype: LROPoller[None]
        """
        response = self.delete(f"resourceGroups/{resource_group_name}/providers/Microsoft.AppConfiguration/configurationStores/{config_store_name}/replicas/{replica_name}", **kwargs)
        return self._create_lro_poller(response, **kwargs)

    # Snapshots Operations
    
    def get_snapshot(self, resource_group_name: str, config_store_name: str, snapshot_name: str, **kwargs: Any) -> Dict[str, Any]:
        """Get properties of a snapshot.
        
        :param resource_group_name: The name of the resource group.
        :type resource_group_name: str
        :param config_store_name: The name of the configuration store.
        :type config_store_name: str
        :param snapshot_name: The name of the snapshot.
        :type snapshot_name: str
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: The snapshot properties
        :rtype: Dict[str, Any]
        """
        response = super().get(f"resourceGroups/{resource_group_name}/providers/Microsoft.AppConfiguration/configurationStores/{config_store_name}/snapshots/{snapshot_name}", **kwargs)
        response.raise_for_status()
        return cast(Dict[str, Any], response.json())

    def begin_create_snapshot(self, resource_group_name: str, config_store_name: str, snapshot_name: str, body: Union[Dict[str, Any], IO[bytes]], **kwargs: Any) -> LROPoller[Dict[str, Any]]:
        """Create a snapshot.
        
        :param resource_group_name: The name of the resource group.
        :type resource_group_name: str
        :param config_store_name: The name of the configuration store.
        :type config_store_name: str
        :param snapshot_name: The name of the snapshot.
        :type snapshot_name: str
        :param body: The parameters for creating a snapshot.
        :type body: Union[Dict[str, Any], IO[bytes]]
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: An LRO poller for the create operation
        :rtype: LROPoller[Dict[str, Any]]
        """
        response = self.put(f"resourceGroups/{resource_group_name}/providers/Microsoft.AppConfiguration/configurationStores/{config_store_name}/snapshots/{snapshot_name}", model=body, **kwargs)
        return self._create_lro_poller(response, **kwargs)
