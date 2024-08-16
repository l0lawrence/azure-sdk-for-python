import json
import os
from github import Github

from azure.eventgrid.system.events.models import *
from azure.eventgrid import SystemEventNames

GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')

class TestEventGridModelsDeserialization():

    def helper_pull_request_event(self):
        g= Github(GITHUB_TOKEN)

        repo = g.get_repo("Azure/azure-rest-api-specs")

        contents = repo.get_contents("specification/eventgrid/data-plane")

        examples = []

        while contents:

            file_content = contents.pop(0)

            if file_content.type == "dir":

                contents.extend(repo.get_contents(file_content.path))

            else:
                if "examples" in file_content.path and "cloud-events-schema" in file_content.path:
                    data = file_content.decoded_content.decode('utf-8')
                    examples.append(json.loads(data))
        return examples

    def deserialize_models(self):
        output = self.helper_pull_request_event()
        for i in output:
            try:
                if i["type"] == "Microsoft.Devices.DeviceConnected":
                    model = "IotHubDeviceConnectedEventData"
                elif i["type"] == "Microsoft.Devices.DeviceCreated":
                    model = "IotHubDeviceCreatedEventData"
                elif i["type"] == "Microsoft.Communication.AdvancedMessageDeliveryStatusUpdated":
                    model = "AcsMessageDeliveryStatusUpdatedEventData"
                elif i["type"] == "Microsoft.Communication.AdvancedMessageReceived":
                    model = "AcsMessageReceivedEventData"
                elif i["type"] == "Microsoft.Communication.ChatThreadParticipantAdded":
                    model = "AcsChatParticipantAddedToThreadEventData"
                elif i["type"] == "Microsoft.Communication.ChatThreadParticipantRemoved":
                    model = "AcsChatParticipantRemovedFromThreadEventData"
                else:
                    model = (SystemEventNames(i["type"]).name).replace("EventName", "EventData")
                mod = __import__('azure.eventgrid.system.events.models', fromlist=[model])
                my_class = getattr(mod, model)
                my_class._deserialize(i["data"], exist_discriminators=[])
            except Exception:
                assert False