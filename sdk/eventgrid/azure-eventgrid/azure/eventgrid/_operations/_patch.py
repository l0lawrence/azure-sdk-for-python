# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
"""Customize generated code here.

Follow our quickstart for examples: https://aka.ms/azsdk/python/dpcodegen/python/customize
"""
from typing import List, Optional, Any, Union, Dict, cast
import json
from azure.eventgrid._operations import EventGridClientOperationsMixin as InternalOperationsMixin
from azure.core.tracing.decorator import distributed_trace
from azure.core.exceptions import (
    HttpResponseError,
    ClientAuthenticationError,
    ResourceNotFoundError,
    ResourceExistsError,
    map_error,
)
from azure.core.messaging import CloudEvent
from ..models._models import EventGridEvent
from ..models._models import CloudEventEvent as InternalCloudEvent
from .._serialization import Serializer
from azure.core.pipeline.transport import HttpRequest

SendType = Union[
    CloudEvent,
    EventGridEvent,
    Dict,
    List[CloudEvent],
    List[EventGridEvent],
    List[Dict],
]

ListEventType = Union[List[CloudEvent], List[EventGridEvent], List[Dict]]

def _is_cloud_event(event):
    # type: (Any) -> bool
    required = ("id", "source", "specversion", "type")
    try:
        return all((_ in event for _ in required)) and event["specversion"] == "1.0"
    except TypeError:
        return False

def _is_eventgrid_event(event):
    # type: (Any) -> bool
    required = ("subject", "eventType", "data", "dataVersion", "id", "eventTime")
    try:
        return all((prop in event for prop in required))
    except TypeError:
        return False

def _eventgrid_data_typecheck(event):
    try:
        data = event.get("data")
    except AttributeError:
        data = event.data

    if isinstance(data, bytes):
        raise TypeError(
            "Data in EventGridEvent cannot be bytes. Please refer to"
            "https://docs.microsoft.com/en-us/azure/event-grid/event-schema"
        )

def _cloud_event_to_generated(cloud_event, **kwargs):
    if isinstance(cloud_event.data, bytes):
        data_base64 = cloud_event.data
        data = None
    else:
        data = cloud_event.data
        data_base64 = None
    return InternalCloudEvent(
        id=cloud_event.id,
        source=cloud_event.source,
        type=cloud_event.type,
        specversion=cloud_event.specversion,
        data=data,
        data_base64=data_base64,
        time=cloud_event.time,
        dataschema=cloud_event.dataschema,
        datacontenttype=cloud_event.datacontenttype,
        subject=cloud_event.subject,
        additional_properties=cloud_event.extensions,
        **kwargs
    )

def _from_cncf_events(event): # pylint: disable=inconsistent-return-statements
    """This takes in a CNCF cloudevent and returns a dictionary.
    If cloud events library is not installed, the event is returned back.

    :param event: The event to be serialized
    :type event: cloudevents.http.CloudEvent
    :return: The serialized event
    :rtype: any
    """
    try:
        from cloudevents.http import to_json
        return json.loads(to_json(event))
    except (AttributeError, ImportError):
        # means this is not a CNCF event
        return event
    except Exception as err: # pylint: disable=broad-except
        msg = """Failed to serialize the event. Please ensure your
        CloudEvents is correctly formatted (https://pypi.org/project/cloudevents/)"""
        raise ValueError(msg) from err


def _build_request(endpoint, content_type, events, *, channel_name=None):
    serialize = Serializer()
    header_parameters = {}  # type: Dict[str, Any]
    header_parameters['Content-Type'] = serialize.header("content_type", content_type, 'str')

    if channel_name:
        header_parameters['aeg-channel-name'] = channel_name

    query_parameters = {}  # type: Dict[str, Any]
    query_parameters['api-version'] = serialize.query("api_version", "2018-01-01", 'str')

    body = serialize.body(events, '[object]')
    if body is None:
        data = None
    else:
        data = json.dumps(body)
        header_parameters['Content-Length'] = str(len(data))

    request = HttpRequest(
        method="POST",
        url=endpoint,
        headers=header_parameters,
        data=data
    )
    request.format_parameters(query_parameters)
    return request

class EventGridClientOperationsMixin(InternalOperationsMixin):

    @distributed_trace
    def send(
        self,
        events: SendType,
        *,
        channel_name: Optional[str] = None,
        **kwargs: Any
        ) -> None:
        """Sends events to a topic or a domain specified during the client initialization.

        A single instance or a list of dictionaries, CloudEvents or EventGridEvents are accepted.

        .. admonition:: Example:

            .. literalinclude:: ../samples/sync_samples/sample_publish_eg_events_to_a_topic.py
                :start-after: [START publish_eg_event_to_topic]
                :end-before: [END publish_eg_event_to_topic]
                :language: python
                :dedent: 0
                :caption: Publishing an EventGridEvent.

            .. literalinclude:: ../samples/sync_samples/sample_publish_events_using_cloud_events_1.0_schema.py
                :start-after: [START publish_cloud_event_to_topic]
                :end-before: [END publish_cloud_event_to_topic]
                :language: python
                :dedent: 0
                :caption: Publishing a CloudEvent.

        Dict representation of respective serialized models is accepted as CloudEvent(s) or
        EventGridEvent(s) apart from the strongly typed objects.

        .. admonition:: Example:

            .. literalinclude:: ../samples/sync_samples/sample_publish_eg_event_using_dict.py
                :start-after: [START publish_eg_event_dict]
                :end-before: [END publish_eg_event_dict]
                :language: python
                :dedent: 4
                :caption: Publishing a list of EventGridEvents using a dict-like representation.

            .. literalinclude:: ../samples/sync_samples/sample_publish_cloud_event_using_dict.py
                :start-after: [START publish_cloud_event_dict]
                :end-before: [END publish_cloud_event_dict]
                :language: python
                :dedent: 0
                :caption: Publishing a CloudEvent using a dict-like representation.

        When publishing a Custom Schema Event(s), dict-like representation is accepted.
        Either a single dictionary or a list of dictionaries can be passed.

        .. admonition:: Example:

            .. literalinclude:: ../samples/sync_samples/sample_publish_custom_schema_to_a_topic.py
                :start-after: [START publish_custom_schema]
                :end-before: [END publish_custom_schema]
                :language: python
                :dedent: 4
                :caption: Publishing a Custom Schema event.

        **WARNING**: When sending a list of multiple events at one time, iterating over and sending each event
        will not result in optimal performance. For best performance, it is highly recommended to send
        a list of events.

        :param events: A single instance or a list of dictionaries/CloudEvent/EventGridEvent to be sent.
        :type events: ~azure.core.messaging.CloudEvent or ~azure.eventgrid.EventGridEvent or dict or
         List[~azure.core.messaging.CloudEvent] or List[~azure.eventgrid.EventGridEvent] or List[dict]
        :keyword str content_type: The type of content to be used to send the events.
         Has default value "application/json; charset=utf-8" for EventGridEvents,
         with "cloudevents-batch+json" for CloudEvents
        :keyword channel_name: Optional. Used to specify the name of event channel when publishing to partner.
        :paramtype channel_name: str or None
         namespaces with partner topic. For more details, visit
         https://docs.microsoft.com/azure/event-grid/partner-events-overview
        :rtype: None
        """
        if not isinstance(events, list):
            events = cast(ListEventType, [events])
        content_type = kwargs.pop("content_type", "application/json; charset=utf-8")
        if isinstance(events[0], CloudEvent) or _is_cloud_event(events[0]):
            try:
                events = [
                    _cloud_event_to_generated(e, **kwargs)
                    for e in events  # pylint: disable=protected-access
                ]
            except AttributeError:
                ## this is either a dictionary or a CNCF cloud event
                events = [
                    _from_cncf_events(e) for e in events
                ]
            content_type = "application/cloudevents-batch+json; charset=utf-8"
        elif isinstance(events[0], EventGridEvent) or _is_eventgrid_event(events[0]):
            for event in events:
                _eventgrid_data_typecheck(event)
        response = self._client.send_request(  # pylint: disable=protected-access
            _build_request(self._endpoint, content_type, events, channel_name=channel_name), **kwargs
        )
        error_map = {401: ClientAuthenticationError, 404: ResourceNotFoundError, 409: ResourceExistsError}
        if response.status_code != 200:
            map_error(status_code=response.status_code, response=response, error_map=error_map)
            raise HttpResponseError(response=response)



__all__: List[str] = []  # Add all objects you want publicly available to users at this package level


def patch_sdk():
    """Do not remove from this file.

    `patch_sdk` is a last resort escape hatch that allows you to do customizations
    you can't accomplish using the techniques described in
    https://aka.ms/azsdk/python/dpcodegen/python/customize
    """
