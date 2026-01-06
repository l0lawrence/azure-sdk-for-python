from typing import Any, Dict, Optional, Protocol, TypedDict, Callable, Union, cast, IO

from azure.core.paging import ItemPaged
from azure.core.polling import LROPoller

from .service_factory import ServiceProviderFactory


class WidgetsOperations(Protocol):
    def list_widgets(self, resource_group_name: Optional[str] = None, **kwargs: Any) -> ItemPaged[Dict[str, Any]]: ...

    def get_widget(self, resource_group_name: str, widget_name: str, **kwargs: Any) -> Dict[str, Any]: ...

    def begin_create_widget(
        self,
        resource_group_name: str,
        widget_name: str,
        widget_parameters: Union[Dict[str, Any], IO[bytes]],
        **kwargs: Any,
    ) -> LROPoller[Dict[str, Any]]: ...

    def begin_delete_widget(self, resource_group_name: str, widget_name: str, **kwargs: Any) -> None: ...

class WidgetKeyOperations(Protocol):
    def list_widget_keys(self, resource_group_name: str, widget_name: str, **kwargs: Any) -> ItemPaged[Dict[str, Any]]: ...

    def get_widget_key(self, resource_group_name: str, widget_name: str, key_name: str, **kwargs: Any) -> Dict[str, Any]: ...

    def begin_create_widget_key(
        self,
        resource_group_name: str,
        widget_name: str,
        key_name: str,
        key_parameters: Union[Dict[str, Any], IO[bytes]],
        **kwargs: Any,
    ) -> LROPoller[Dict[str, Any]]: ...

    def begin_delete_widget_key(self, resource_group_name: str, widget_name: str, key_name: str, **kwargs: Any) -> None: ...

class OperationsByGroup(TypedDict):
    widgets: WidgetsOperations
    widget_keys: WidgetKeyOperations


class SampleMgmtFactory(ServiceProviderFactory):
    """Example factory using the service-registry pattern for future providers."""

    def __init__(
        self,
        client: "ManagementClient",
        service_provider: str = "Microsoft.Sample",
        subscription_id: Optional[str] = None,
        api_version: Optional[str] = None,
    ):
        if api_version is None:
            api_version = "2024-01-01-preview"
        super().__init__(client, service_provider, subscription_id, api_version)
        self.operations_by_group: OperationsByGroup = {
            "widgets": cast(WidgetsOperations, self),
            "widget_keys": cast(WidgetKeyOperations, self),
        }
        self.routes_by_method: Dict[str, Dict[str, Callable[..., Any]]] = {
            "GET": {
                # List widgets optionally scoped to a resource group
                "list_widgets": lambda rg=None, **kw: self.get(
                    f"resourceGroups/{rg}/providers/{self.service_provider}/widgets" if rg else "widgets",
                    **kw,
                ),
                "get_widget": lambda rg, name, **kw: self.get(
                    f"resourceGroups/{rg}/providers/{self.service_provider}/widgets/{name}",
                    **kw,
                ),
                "list_widget_keys": lambda rg, name, **kw: self.get(
                    f"resourceGroups/{rg}/providers/{self.service_provider}/widgets/{name}/keys",
                    **kw,
                ),
                "get_widget_key": lambda rg, name, key_name, **kw: self.get(
                    f"resourceGroups/{rg}/providers/{self.service_provider}/widgets/{name}/keys/{key_name}",
                    **kw,
                ),
            },
            "PUT": {
                "begin_create_widget": lambda rg, name, body, **kw: self._create_lro_poller(
                    self.put(
                        f"resourceGroups/{rg}/providers/{self.service_provider}/widgets/{name}",
                        model=body,
                        **kw,
                    ),
                    **kw,
                ),
                "begin_create_widget_key": lambda rg, name, key_name, body, **kw: self._create_lro_poller(
                    self.put(
                        f"resourceGroups/{rg}/providers/{self.service_provider}/widgets/{name}/keys/{key_name}",
                        model=body,
                        **kw,
                    ),
                    **kw,
                ),
            },
            "DELETE": {
                "begin_delete_widget": lambda rg, name, **kw: self._create_lro_poller(
                    self.delete(
                        f"resourceGroups/{rg}/providers/{self.service_provider}/widgets/{name}",
                        **kw,
                    ),
                    **kw,
                ),
                "begin_delete_widget_key": lambda rg, name, key_name, **kw: self._create_lro_poller(
                    self.delete(
                        f"resourceGroups/{rg}/providers/{self.service_provider}/widgets/{name}/keys/{key_name}",
                        **kw,
                    ),
                    **kw,
                ),
            },
        }
        # Flat index for fast dynamic lookup: name -> (verb, handler)
        self._route_index: Dict[str, Callable[..., Any]] = {
            name: handler for _, routes in self.routes_by_method.items() for name, handler in routes.items()
        }

    def _call_route(self, verb: str, operation: str, *args: Any, **kwargs: Any) -> Any:
        try:
            handler = self.routes_by_method[verb][operation]
        except KeyError as exc:
            raise AttributeError(f"Operation '{operation}' not registered for verb '{verb}'") from exc
        return handler(*args, **kwargs)

    def __getattr__(self, name: str) -> Any:
        handler = self._route_index.get(name)
        if handler is None:
            raise AttributeError(f"{type(self).__name__} has no attribute '{name}'")

        def _bound(*args: Any, **kwargs: Any) -> Any:
            return handler(*args, **kwargs)

        return _bound

    @property
    def widgets(self) -> WidgetsOperations:
        return cast(WidgetsOperations, self)
    
    @property
    def widget_keys(self) -> WidgetKeyOperations:
        return cast(WidgetKeyOperations, self)
