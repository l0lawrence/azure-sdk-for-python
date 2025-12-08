from typing import Any, Optional, TYPE_CHECKING, Union, Dict, Callable, cast

from azure.core.polling import AsyncLROPoller, AsyncPollingMethod, AsyncNoPolling
from azure.core.rest import HttpRequest, AsyncHttpResponse
from azure.core.pipeline import PipelineResponse, PipelineContext
from azure.mgmt.core.polling.async_arm_polling import AsyncARMPolling


if TYPE_CHECKING:
    from .._client import AsyncManagementClient


class AsyncServiceProviderFactory:
    """Base async factory class for service providers with HTTP operations."""
    
    def __init__(self, client: "AsyncManagementClient", service_provider: str, subscription_id: Optional[str] = None, api_version: Optional[str] = None):
        self.client = client
        self.service_provider = service_provider
        # Use provided subscription_id or fall back to client's default
        self.subscription_id = subscription_id or client._config.subscription_id
        # Store API version for use in requests - use provided version, class default, or global default
        self.api_version = api_version
        self.base_url = f"/subscriptions/{self.subscription_id}/providers/{service_provider}"
    
    async def get(self, url: str, **kwargs: Any) -> AsyncHttpResponse:
        """Send an async GET request.
        
        :param url: The relative URL to send the request to. Can be absolute or relative to provider.
        :type url: str
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: The response of your network call.
        :rtype: ~azure.core.rest.AsyncHttpResponse
        """
        full_url = url if url.startswith('/') else f"{self.base_url}/{url}"
        # Add required api-version parameter
        api_version = kwargs.pop("api_version", self.api_version)
        separator = "&" if "?" in full_url else "?"
        full_url += f"{separator}api-version={api_version}"
        request = HttpRequest("GET", full_url)
        return await self.client._send_request(request, **kwargs)

    async def post(self, url: str, *, model: Optional[Dict[str, Any]] = None, json: Any = None, data: Any = None, **kwargs: Any) -> AsyncHttpResponse:
        """Send an async POST request.
        
        :param url: The relative URL to send the request to. Can be absolute or relative to provider.
        :type url: str
        :keyword model: Model data to send in the request body (takes precedence over json/data).
        :type model: Optional[Dict[str, Any]]
        :keyword json: JSON data to send in the request body.
        :keyword data: Data to send in the request body.
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: The response of your network call.
        :rtype: ~azure.core.rest.AsyncHttpResponse
        """
        full_url = url if url.startswith('/') else f"{self.base_url}/{url}"
        # Add required api-version parameter
        api_version = kwargs.pop("api_version", self.api_version)
        separator = "&" if "?" in full_url else "?"
        full_url += f"{separator}api-version={api_version}"
        request = HttpRequest("POST", full_url)
        if model is not None:
            request.set_json_body(model)
        elif json is not None:
            request.set_json_body(json)
        elif data is not None:
            request.set_bytes_body(data)
        return await self.client._send_request(request, **kwargs)

    async def put(self, url: str, *, model: Optional[Dict[str, Any]] = None, json: Any = None, data: Any = None, **kwargs: Any) -> AsyncHttpResponse:
        """Send an async PUT request.
        
        :param url: The relative URL to send the request to. Can be absolute or relative to provider.
        :type url: str
        :keyword model: Model data to send in the request body (takes precedence over json/data).
        :type model: Optional[Dict[str, Any]]
        :keyword json: JSON data to send in the request body.
        :keyword data: Data to send in the request body.
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: The response of your network call.
        :rtype: ~azure.core.rest.AsyncHttpResponse
        """
        full_url = url if url.startswith('/') else f"{self.base_url}/{url}"
        # Add required api-version parameter
        api_version = kwargs.pop("api_version", self.api_version)
        separator = "&" if "?" in full_url else "?"
        full_url += f"{separator}api-version={api_version}"
        request = HttpRequest("PUT", full_url)
        if model is not None:
            request.set_json_body(model)
        elif json is not None:
            request.set_json_body(json)
        elif data is not None:
            request.set_bytes_body(data)
        return await self.client._send_request(request, **kwargs)

    async def patch(self, url: str, *, model: Optional[Dict[str, Any]] = None, json: Any = None, data: Any = None, **kwargs: Any) -> AsyncHttpResponse:
        """Send an async PATCH request.
        
        :param url: The relative URL to send the request to. Can be absolute or relative to provider.
        :type url: str
        :keyword model: Model data to send in the request body (takes precedence over json/data).
        :type model: Optional[Dict[str, Any]]
        :keyword json: JSON data to send in the request body.
        :keyword data: Data to send in the request body.
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: The response of your network call.
        :rtype: ~azure.core.rest.AsyncHttpResponse
        """
        full_url = url if url.startswith('/') else f"{self.base_url}/{url}"
        # Add required api-version parameter
        api_version = kwargs.pop("api_version", self.api_version)
        separator = "&" if "?" in full_url else "?"
        full_url += f"{separator}api-version={api_version}"
        request = HttpRequest("PATCH", full_url)
        if model is not None:
            request.set_json_body(model)
        elif json is not None:
            request.set_json_body(json)
        elif data is not None:
            request.set_bytes_body(data)
        return await self.client._send_request(request, **kwargs)

    async def delete(self, url: str, **kwargs: Any) -> AsyncHttpResponse:
        """Send an async DELETE request.
        
        :param url: The relative URL to send the request to. Can be absolute or relative to provider.
        :type url: str
        :keyword bool stream: Whether the response payload will be streamed. Defaults to False.
        :return: The response of your network call.
        :rtype: ~azure.core.rest.AsyncHttpResponse
        """
        full_url = url if url.startswith('/') else f"{self.base_url}/{url}"
        # Add required api-version parameter
        api_version = kwargs.pop("api_version", self.api_version)
        separator = "&" if "?" in full_url else "?"
        full_url += f"{separator}api-version={api_version}"
        request = HttpRequest("DELETE", full_url)
        return await self.client._send_request(request, **kwargs)

    def _create_lro_poller(
        self,
        response: AsyncHttpResponse,
        polling: Union[bool, AsyncPollingMethod] = True,
        lro_options: Optional[Dict[str, Any]] = None,
        **kwargs: Any
    ) -> AsyncLROPoller:
        """Create an async Long Running Operation poller from an initial response.
        
        :param response: The initial response.
        :type response: ~azure.core.rest.AsyncHttpResponse
        :param polling: True for default async ARMPolling, False for no polling, or an async polling method.
        :type polling: Union[bool, AsyncPollingMethod]
        :param lro_options: Options for LRO poller.
        :type lro_options: Optional[Dict[str, Any]]
        :return: An async LRO poller.
        :rtype: ~azure.core.polling.AsyncLROPoller
        """
        lro_options = lro_options or {}
        
        if polling is True:
            polling_method = AsyncARMPolling(
                lro_options.get("lro_delay", 30),
                **lro_options
            )
        elif polling is False:
            polling_method = AsyncNoPolling()
        else:
            polling_method = polling

        return AsyncLROPoller(
            self.client,
            response,
            lambda x: None,  # Deserialization function - keeping simple for now
            polling_method,
            **kwargs
        )

    async def _build_request(
        self, 
        method: str,
        url: str,
        *,
        resource_group: Optional[str] = None,
        model: Optional[Dict[str, Any]] = None,
        json: Any = None,
        data: Any = None,
        api_version: Optional[str] = None,
        **kwargs: Any
    ) -> HttpRequest:
        """Build an HTTP request with common parameter handling.
        
        :param method: HTTP method (GET, POST, PUT, PATCH, DELETE).
        :type method: str
        :param url: The relative URL to send the request to. Can be absolute or relative to provider.
        :type url: str
        :keyword resource_group: Optional resource group name to add to URL path.
        :type resource_group: Optional[str]
        :keyword model: Model data to send in the request body (takes precedence over json/data).
        :type model: Optional[Dict[str, Any]]
        :keyword json: JSON data to send in the request body.
        :keyword data: Data to send in the request body.
        :keyword api_version: Override API version for this request.
        :type api_version: Optional[str]
        :return: The built HTTP request.
        :rtype: ~azure.core.rest.HttpRequest
        """
        # Build the full URL
        if url.startswith('/'):
            full_url = url
        elif resource_group:
            full_url = f"{self.base_url}/resourceGroups/{resource_group}/providers/{self.service_provider}/{url}"
        else:
            full_url = f"{self.base_url}/{url}"
        
        # Add required api-version parameter
        request_api_version = api_version or self.api_version
        separator = "&" if "?" in full_url else "?"
        full_url += f"{separator}api-version={request_api_version}"
        
        # Create request
        request = HttpRequest(method.upper(), full_url)
        
        # Set body if provided
        if model is not None:
            request.set_json_body(model)
        elif json is not None:
            request.set_json_body(json)
        elif data is not None:
            request.set_bytes_body(data)
            
        return request