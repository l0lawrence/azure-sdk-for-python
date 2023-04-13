from azure.servicebus.aio import ServiceBusClient
from azure.servicebus import ServiceBusMessage, ServiceBusMessageBatch
from azure.servicebus.exceptions import ServiceBusError
from azure.servicebus._common.utils import utc_now
import time
import threading
import asyncio
import logging
import sys

connection_str = "Endpoint=sb://llawsb.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=9S5Xs8ht3zvIyExL+HOq/8wZeuj8d34NEOf/A08gWds="
queue = "lock15"


logger = logging.getLogger("azure")
logger.setLevel(logging.DEBUG)

# Direct logging output to stdout. Without adding a handler,
# no logging output is visible.
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)

async def main():
    async with ServiceBusClient.from_connection_string(
                connection_str,
                logging_enable=False) as sb_client:

            async with sb_client.get_queue_sender(queue) as sender:
                message = ServiceBusMessage("0")
                message_1 = ServiceBusMessage("1")
                await sender.send_messages([message, message_1])

                print("SENT")
                messages = []
                async with sb_client.get_queue_receiver(queue, max_wait_time=10) as receiver:
                    
                    async for message in receiver._get_streaming_message_iter():
                        messages.append(message)
                        break
                    print("Iter 1")

                    async for message in receiver._get_streaming_message_iter():
                        messages.append(message)
                    print("Iter 2")

                    for message in messages:
                        await receiver.complete_message(message)
                    print("Completed")


                    print(len(messages) == 2)
                    print(str(messages[0]) == "0")
                    print(str(messages[1]) == "1")

                    message_2 = ServiceBusMessage("2")
                    message_3 = ServiceBusMessage("3")
                    await sender.send_messages([message_2, message_3])

                    async for message in receiver._get_streaming_message_iter():
                        messages.append(message)
                        async for message in receiver._get_streaming_message_iter():
                            messages.append(message)

                    print(len(messages) == 4)
                    print(str(messages[2]) == "2")
                    print(str(messages[3]) == "3")

                    for message in messages[2:]:
                        await receiver.complete_message(message)

                    messages = await receiver.receive_messages()
                    print(messages)

asyncio.run(main())


# with ServiceBusClient.from_connection_string(
#                 connection_str,
#                 logging_enable=False) as sb_client:

#             with sb_client.get_queue_sender(queue) as sender:
#                 message = ServiceBusMessage("0")
#                 message_1 = ServiceBusMessage("1")
#                 sender.send_messages([message, message_1])

#                 print("SENT")
#                 messages = []
#                 with sb_client.get_queue_receiver(queue, max_wait_time=10) as receiver:
                    
#                     for message in receiver._get_streaming_message_iter():
#                         messages.append(message)
#                         break
#                     print("Iter 1")

#                     for message in receiver._get_streaming_message_iter():
#                         messages.append(message)
#                     print("Iter 2")

#                     for message in messages:
#                         receiver.complete_message(message)
#                     print("Completed")


#                     print(len(messages) == 2)
#                     print(str(messages[0]) == "0")
#                     print(str(messages[1]) == "1")

#                     message_2 = ServiceBusMessage("2")
#                     message_3 = ServiceBusMessage("3")
#                     sender.send_messages([message_2, message_3])

#                     for message in receiver._get_streaming_message_iter():
#                         messages.append(message)
#                         for message in receiver._get_streaming_message_iter():
#                             messages.append(message)

#                     print(len(messages) == 4)
#                     print(str(messages[2]) == "2")
#                     print(str(messages[3]) == "3")

#                     for message in messages[2:]:
#                         receiver.complete_message(message)

#                     messages = receiver.receive_messages()
#                     print(messages)