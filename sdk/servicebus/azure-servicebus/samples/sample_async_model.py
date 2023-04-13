from azure.servicebus.aio import ServiceBusClient
from azure.servicebus import ServiceBusMessage, ServiceBusMessageBatch
from azure.servicebus.exceptions import ServiceBusError
from azure.servicebus._common.utils import utc_now
import time
import threading
import asyncio
import logging
import sys
import types

connection_str = "Endpoint=sb://llawsb.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=9S5Xs8ht3zvIyExL+HOq/8wZeuj8d34NEOf/A08gWds="
queue = "q111"

logger = logging.getLogger("azure")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)

async def _hack_disable_receive_context_message_received(self, frame, message):
    # pylint: disable=protected-access
    print("Put message")
    self._handler._received_messages.put((frame, message))

async def main():


    async with ServiceBusClient.from_connection_string(
        connection_str, logging_enable=True) as sb_client:


        receiver = sb_client.get_queue_receiver(queue)
        sender = sb_client.get_queue_sender(queue)


        async with sender, receiver:
            # send 5 msgs to queue first
            await sender.send_messages([ServiceBusMessage('test') for _ in range(5)])
            receiver._handler._link._on_transfer = types.MethodType(
                _hack_disable_receive_context_message_received, receiver)
            received_msgs = []
            while len(received_msgs) < 5:
                # issue 10 link credits, client should consume 5 msgs from the service
                # leaving 5 credits on the wire
                for msg in (await receiver.receive_messages(max_message_count=10, max_wait_time=10)):
                    await receiver.complete_message(msg)
                    received_msgs.append(msg)
            print(len(received_msgs) == 5)

            # send 5 more messages, those messages would arrive at the client while the program is sleeping
            await sender.send_messages([ServiceBusMessage('test') for _ in range(5)])
            print("SLEEP STARTED")
            print(receiver._handler._link.current_link_credit)
            await asyncio.sleep(15)  # sleep > message expiration time
            print("SLEEP DONE")

            # issue 5 link credits, client should consume 5 msgs from the internal buffer which is already lock expired
            target_msgs_count = 5
            received_msgs = []
            while len(received_msgs) < target_msgs_count:
                received_msgs.extend((await receiver.receive_messages(max_message_count=5, max_wait_time=10)))
            print(f"RECEIVED 5 {len(received_msgs) == 5}")
            for msg in received_msgs:
                print(msg.delivery_count == 0)
                try:
                    print("TRY TO COMPLETE")
                    await receiver.complete_message(msg)
                except ServiceBusError as e:
                    print("ERROR")
                    print(e)

            # re-received message with delivery count increased
            target_msgs_count = 5
            received_msgs = []
            while len(received_msgs) < target_msgs_count:
                received_msgs.extend((await receiver.receive_messages(max_message_count=5, max_wait_time=10)))
            print(f"RECEIVED 5 {len(received_msgs) == 5}")
            for msg in received_msgs:
                # assert msg.delivery_count > 0
                await receiver.complete_message(msg)


asyncio.run(main())