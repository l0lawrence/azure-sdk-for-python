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
queue = "lock9"



logger = logging.getLogger("azure")
logger.setLevel(logging.DEBUG)

# Direct logging output to stdout. Without adding a handler,
# no logging output is visible.
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)



async def main():

    async with ServiceBusClient.from_connection_string(connection_str, logging_enable=True) as sb_client:

        # async def sub_test_releasing_messages():
            # test releasing messages when prefetch is 1 and link credits are issue dynamically
            receiver = sb_client.get_queue_receiver(queue)
            sender = sb_client.get_queue_sender(queue)
            async with sender, receiver:
                # send 10 msgs to queue first
                await sender.send_messages([ServiceBusMessage('test') for _ in range(5)])

                received_msgs = []
                # the amount of messages returned by receive call is not stable, especially in live tests
                # of different os platforms, this is why a while loop is used here to receive the specific
                # amount of message we want to receive
                while len(received_msgs) < 5:
                    # issue link credits more than 5, client should consume 5 msgs from the service in total,
                    # leaving the extra credits on the wire
                    for msg in (await receiver.receive_messages(max_message_count=10, max_wait_time=10)):
                        await receiver.complete_message(msg)
                        received_msgs.append(received_msgs)
                print(len(received_msgs) == 5)

                # send 5 more messages, those messages would arrive at the client while the program is sleeping
                await sender.send_messages([ServiceBusMessage('test') for _ in range(5)])
                print("SLEEP")
                await asyncio.sleep(15)  # sleep > message expiration time
                print("DONE SLEEP")

                target_msgs_count = 5
                received_msgs = []
                while len(received_msgs) < target_msgs_count:
                    # issue 10 link credits, client should consume 5 msgs from the service, leaving no link credits
                    for msg in (await receiver.receive_messages(max_message_count=target_msgs_count - len(received_msgs),max_wait_time=10)):
                        print("Get a message")
                        print(msg.delivery_count == 0)  # release would not increase delivery count
                        await receiver.complete_message(msg)
                        received_msgs.append(msg)
                print("Got messg")
                print(len(received_msgs) == 5)

asyncio.run(main())