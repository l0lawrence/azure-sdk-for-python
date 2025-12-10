from typing import TYPE_CHECKING, Any, Optional, Dict, Union, Protocol, TypedDict, Callable, cast, IO
from azure.core.paging import ItemPaged

from azure.core.polling import LROPoller
from azure.core.rest import HttpResponse
from .service_factory import ServiceProviderFactory
from ..models.azure_mgmt_appconfiguration import (
    ApiKey, ApiKeyListResult, ConfigurationStore, ConfigurationStoreListResult
)

if TYPE_CHECKING:
    from .._client import ManagementClient


class ConfigurationStoresOperations(Protocol):
    def list(self, skip_token: Optional[str] = None, **kwargs: Any) -> ItemPaged[ConfigurationStore]: ...

    def list_by_resource_group(
        self, resource_group_name: str, skip_token: Optional[str] = None, **kwargs: Any
    ) -> ItemPaged[ConfigurationStore]: ...

    def get_configuration_store(self, resource_group_name: str, config_store_name: str, **kwargs: Any) -> ConfigurationStore: ...

    def begin_create(
        self,
        resource_group_name: str,
        config_store_name: str,
        config_store_creation_parameters: Union[ConfigurationStore, IO[bytes]],
        **kwargs: Any,
    ) -> LROPoller[ConfigurationStore]: ...

    def begin_delete(self, resource_group_name: str, config_store_name: str, **kwargs: Any) -> LROPoller[None]: ...

    def begin_update(
        self,
        resource_group_name: str,
        config_store_name: str,
        config_store_update_parameters: Union[Dict[str, Any], IO[bytes]],
        **kwargs: Any,
    ) -> LROPoller[ConfigurationStore]: ...

    def list_keys(
        self, resource_group_name: str, config_store_name: str, skip_token: Optional[str] = None, **kwargs: Any
    ) -> ItemPaged[ApiKey]: ...

    def regenerate_key(
        self,
        resource_group_name: str,
        config_store_name: str,
        regenerate_key_parameters: Union[Dict[str, str], IO[bytes]],
        **kwargs: Any,
    ) -> ApiKey: ...

    def list_deleted(self, **kwargs: Any) -> ItemPaged[Dict[str, Any]]: ...

    def get_deleted(self, location: str, config_store_name: str, **kwargs: Any) -> Dict[str, Any]: ...

    def begin_purge_deleted(self, location: str, config_store_name: str, **kwargs: Any) -> LROPoller[None]: ...


class KeyValuesOperations(Protocol):
    def get_key_value(
        self, resource_group_name: str, config_store_name: str, key_value_name: str, **kwargs: Any
    ) -> Dict[str, Any]: ...

    def create_or_update_key_value(
        self,
        resource_group_name: str,
        config_store_name: str,
        key_value_name: str,
        key_value_parameters: Union[Dict[str, Any], IO[bytes]],
        **kwargs: Any,
    ) -> Dict[str, Any]: ...

    def begin_delete_key_value(
        self, resource_group_name: str, config_store_name: str, key_value_name: str, **kwargs: Any
    ) -> LROPoller[None]: ...


class OperationsOperations(Protocol):
    def check_name_availability(
        self, check_name_availability_parameters: Union[Dict[str, Any], IO[bytes]], **kwargs: Any
    ) -> Dict[str, Any]: ...

    def list_operations(self, skip_token: Optional[str] = None, **kwargs: Any) -> ItemPaged[Dict[str, Any]]: ...

    def regional_check_name_availability(
        self,
        location: str,
        check_name_availability_parameters: Union[Dict[str, Any], IO[bytes]],
        **kwargs: Any,
    ) -> Dict[str, Any]: ...


class PrivateEndpointConnectionsOperations(Protocol):
    def list_private_endpoint_connections(
        self, resource_group_name: str, config_store_name: str, **kwargs: Any
    ) -> ItemPaged[Dict[str, Any]]: ...

    def get_private_endpoint_connection(
        self, resource_group_name: str, config_store_name: str, private_endpoint_connection_name: str, **kwargs: Any
    ) -> Dict[str, Any]: ...

    def begin_create_or_update_private_endpoint_connection(
        self,
        resource_group_name: str,
        config_store_name: str,
        private_endpoint_connection_name: str,
        private_endpoint_connection: Union[Dict[str, Any], IO[bytes]],
        **kwargs: Any,
    ) -> LROPoller[Dict[str, Any]]: ...

    def begin_delete_private_endpoint_connection(
        self, resource_group_name: str, config_store_name: str, private_endpoint_connection_name: str, **kwargs: Any
    ) -> LROPoller[None]: ...


class PrivateLinkResourcesOperations(Protocol):
    def list_private_link_resources(
        self, resource_group_name: str, config_store_name: str, **kwargs: Any
    ) -> ItemPaged[Dict[str, Any]]: ...

    def get_private_link_resource(
        self, resource_group_name: str, config_store_name: str, group_name: str, **kwargs: Any
    ) -> Dict[str, Any]: ...


class ReplicasOperations(Protocol):
    def list_replicas(
        self, resource_group_name: str, config_store_name: str, skip_token: Optional[str] = None, **kwargs: Any
    ) -> ItemPaged[Dict[str, Any]]: ...

    def get_replica(
        self, resource_group_name: str, config_store_name: str, replica_name: str, **kwargs: Any
    ) -> Dict[str, Any]: ...

    def begin_create_replica(
        self,
        resource_group_name: str,
        config_store_name: str,
        replica_name: str,
        replica_creation_parameters: Union[Dict[str, Any], IO[bytes]],
        **kwargs: Any,
    ) -> LROPoller[Dict[str, Any]]: ...

    def begin_delete_replica(
        self, resource_group_name: str, config_store_name: str, replica_name: str, **kwargs: Any
    ) -> LROPoller[None]: ...


class SnapshotsOperations(Protocol):
    def get_snapshot(
        self, resource_group_name: str, config_store_name: str, snapshot_name: str, **kwargs: Any
    ) -> Dict[str, Any]: ...

    def begin_create_snapshot(
        self,
        resource_group_name: str,
        config_store_name: str,
        snapshot_name: str,
        body: Union[Dict[str, Any], IO[bytes]],
        **kwargs: Any,
    ) -> LROPoller[Dict[str, Any]]: ...

class AppConfigurationFactory(ServiceProviderFactory):
    """Specialized factory for Microsoft.AppConfiguration resource provider.

    Provides typed operations and models for App Configuration service management.

    Example:
        ops_get = client.appconfiguration.operations_by_method["GET"]
        stores = ops_get.list()
    """
    
    def __init__(self, client: "ManagementClient", service_provider: str, subscription_id: Optional[str] = None, api_version: Optional[str] = None):
        # Set default API version if none provided
        if api_version is None:
            api_version = "2023-03-01"
        super().__init__(client, service_provider, subscription_id, api_version)

        self.routes_by_method: Dict[str, Dict[str, Callable[..., Any]]] = {
            "GET": {
                "list": lambda skip_token=None, **kw: self.get(
                    f"configurationStores{f'?$skipToken={skip_token}' if skip_token else ''}", **kw
                ),
                "list_by_resource_group": lambda rg, skip_token=None, **kw: self.get(
                    f"resourceGroups/{rg}/providers/Microsoft.AppConfiguration/configurationStores{f'?$skipToken={skip_token}' if skip_token else ''}",
                    **kw,
                ),
                "get_configuration_store": lambda rg, name, **kw: self.get(
                    f"resourceGroups/{rg}/providers/Microsoft.AppConfiguration/configurationStores/{name}", **kw
                ),
                "list_operations": lambda skip_token=None, **kw: self.get(
                    f"/providers/Microsoft.AppConfiguration/operations{f'?$skipToken={skip_token}' if skip_token else ''}",
                    **kw,
                ),
                "list_deleted": lambda **kw: self.get("deletedConfigurationStores", **kw),
                "get_deleted": lambda location, name, **kw: self.get(
                    f"locations/{location}/deletedConfigurationStores/{name}", **kw
                ),
                "get_key_value": lambda rg, name, key, **kw: self.get(
                    f"resourceGroups/{rg}/providers/Microsoft.AppConfiguration/configurationStores/{name}/keyValues/{key}",
                    **kw,
                ),
                "list_private_endpoint_connections": lambda rg, name, **kw: self.get(
                    f"resourceGroups/{rg}/providers/Microsoft.AppConfiguration/configurationStores/{name}/privateEndpointConnections",
                    **kw,
                ),
                "get_private_endpoint_connection": lambda rg, name, pec, **kw: self.get(
                    f"resourceGroups/{rg}/providers/Microsoft.AppConfiguration/configurationStores/{name}/privateEndpointConnections/{pec}",
                    **kw,
                ),
                "list_private_link_resources": lambda rg, name, **kw: self.get(
                    f"resourceGroups/{rg}/providers/Microsoft.AppConfiguration/configurationStores/{name}/privateLinkResources",
                    **kw,
                ),
                "get_private_link_resource": lambda rg, name, group_name, **kw: self.get(
                    f"resourceGroups/{rg}/providers/Microsoft.AppConfiguration/configurationStores/{name}/privateLinkResources/{group_name}",
                    **kw,
                ),
                "list_replicas": lambda rg, name, skip_token=None, **kw: self.get(
                    f"resourceGroups/{rg}/providers/Microsoft.AppConfiguration/configurationStores/{name}/replicas{f'?$skipToken={skip_token}' if skip_token else ''}",
                    **kw,
                ),
                "get_replica": lambda rg, name, replica, **kw: self.get(
                    f"resourceGroups/{rg}/providers/Microsoft.AppConfiguration/configurationStores/{name}/replicas/{replica}",
                    **kw,
                ),
                "get_snapshot": lambda rg, name, snapshot, **kw: self.get(
                    f"resourceGroups/{rg}/providers/Microsoft.AppConfiguration/configurationStores/{name}/snapshots/{snapshot}",
                    **kw,
                ),
            },
            "POST": {
                "list_keys": lambda rg, name, skip_token=None, **kw: self.post(
                    f"resourceGroups/{rg}/providers/Microsoft.AppConfiguration/configurationStores/{name}/ListKeys{f'?$skipToken={skip_token}' if skip_token else ''}",
                    **kw,
                ),
                "regenerate_key": lambda rg, name, body, **kw: self.post(
                    f"resourceGroups/{rg}/providers/Microsoft.AppConfiguration/configurationStores/{name}/RegenerateKey",
                    model=body,
                    **kw,
                ),
                "check_name_availability": lambda body, **kw: self.post(
                    "checkNameAvailability", model=body, **kw
                ),
                "regional_check_name_availability": lambda location, body, **kw: self.post(
                    f"locations/{location}/checkNameAvailability", model=body, **kw
                ),
            },
            "PUT": {
                "begin_create": lambda rg, name, body, **kw: self._create_lro_poller(
                    self.put(
                        f"resourceGroups/{rg}/providers/Microsoft.AppConfiguration/configurationStores/{name}",
                        model=body,
                        **kw,
                    ),
                    **kw,
                ),
                "create_or_update_key_value": lambda rg, name, key, body, **kw: self.put(
                    f"resourceGroups/{rg}/providers/Microsoft.AppConfiguration/configurationStores/{name}/keyValues/{key}",
                    model=body,
                    **kw,
                ),
                "begin_create_or_update_private_endpoint_connection": lambda rg, name, pec, body, **kw: self._create_lro_poller(
                    self.put(
                        f"resourceGroups/{rg}/providers/Microsoft.AppConfiguration/configurationStores/{name}/privateEndpointConnections/{pec}",
                        model=body,
                        **kw,
                    ),
                    **kw,
                ),
                "begin_create_replica": lambda rg, name, replica, body, **kw: self._create_lro_poller(
                    self.put(
                        f"resourceGroups/{rg}/providers/Microsoft.AppConfiguration/configurationStores/{name}/replicas/{replica}",
                        model=body,
                        **kw,
                    ),
                    **kw,
                ),
                "begin_create_snapshot": lambda rg, name, snapshot, body, **kw: self._create_lro_poller(
                    self.put(
                        f"resourceGroups/{rg}/providers/Microsoft.AppConfiguration/configurationStores/{name}/snapshots/{snapshot}",
                        model=body,
                        **kw,
                    ),
                    **kw,
                ),
            },
            "PATCH": {
                "begin_update": lambda rg, name, body, **kw: self._create_lro_poller(
                    self.patch(
                        f"resourceGroups/{rg}/providers/Microsoft.AppConfiguration/configurationStores/{name}",
                        model=body,
                        **kw,
                    ),
                    **kw,
                ),
            },
            "DELETE": {
                "begin_delete": lambda rg, name, **kw: self._create_lro_poller(
                    self.delete(
                        f"resourceGroups/{rg}/providers/Microsoft.AppConfiguration/configurationStores/{name}", **kw
                    ),
                    **kw,
                ),
                "begin_delete_key_value": lambda rg, name, key, **kw: self._create_lro_poller(
                    self.delete(
                        f"resourceGroups/{rg}/providers/Microsoft.AppConfiguration/configurationStores/{name}/keyValues/{key}",
                        **kw,
                    ),
                    **kw,
                ),
                "begin_delete_private_endpoint_connection": lambda rg, name, pec, **kw: self._create_lro_poller(
                    self.delete(
                        f"resourceGroups/{rg}/providers/Microsoft.AppConfiguration/configurationStores/{name}/privateEndpointConnections/{pec}",
                        **kw,
                    ),
                    **kw,
                ),
                "begin_delete_replica": lambda rg, name, replica, **kw: self._create_lro_poller(
                    self.delete(
                        f"resourceGroups/{rg}/providers/Microsoft.AppConfiguration/configurationStores/{name}/replicas/{replica}",
                        **kw,
                    ),
                    **kw,
                ),
                "begin_purge_deleted": lambda location, name, **kw: self._create_lro_poller(
                    self.delete(
                        f"locations/{location}/deletedConfigurationStores/{name}/purge", **kw
                    ),
                    **kw,
                ),
            },
        }

    def _call_route(self, verb: str, operation: str, *args: Any, **kwargs: Any) -> Any:
        try:
            print(f"Calling route: {verb} {operation}")
            handler = self.routes_by_method[verb][operation]
            print(f"Handler: {handler}")
        except KeyError as exc:
            raise AttributeError(f"Operation '{operation}' not registered for verb '{verb}'") from exc
        return handler(*args, **kwargs)

    def __getattr__(self, name: str) -> Any:
        for verb, routes in self.routes_by_method.items():
            if name in routes:
                def _bound(*args: Any, **kwargs: Any) -> Any:
                    return self._call_route(verb, name, *args, **kwargs)

                return _bound
        raise AttributeError(f"{type(self).__name__} has no attribute '{name}'")

    @property
    def configuration_stores(self) -> ConfigurationStoresOperations:
        return cast(ConfigurationStoresOperations, self)

    @property
    def key_values(self) -> KeyValuesOperations:
        return cast(KeyValuesOperations, self)

    @property
    def operations_group(self) -> OperationsOperations:
        return cast(OperationsOperations, self)

    @property
    def private_endpoint_connections(self) -> PrivateEndpointConnectionsOperations:
        return cast(PrivateEndpointConnectionsOperations, self)

    @property
    def private_link_resources(self) -> PrivateLinkResourcesOperations:
        return cast(PrivateLinkResourcesOperations, self)

    @property
    def replicas(self) -> ReplicasOperations:
        return cast(ReplicasOperations, self)

    @property
    def snapshots(self) -> SnapshotsOperations:
        return cast(SnapshotsOperations, self)
