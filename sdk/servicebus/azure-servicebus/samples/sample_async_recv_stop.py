from azure.servicebus.aio import ServiceBusClient
from azure.servicebus import ServiceBusMessage, ServiceBusMessageBatch
from azure.servicebus.exceptions import ServiceBusError
from azure.servicebus._common.utils import utc_now
import time
import threading
import asyncio

connection_str = "Endpoint=sb://llawsb.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=9S5Xs8ht3zvIyExL+HOq/8wZeuj8d34NEOf/A08gWds="
queue = "lock9"

async def main():

    async with ServiceBusClient.from_connection_string(
        connection_str, logging_enable=False) as sb_client:

        async with sb_client.get_queue_sender(queue) as sender:
            for i in range(10):
                message = ServiceBusMessage("Stop message no. {}".format(i))
                await sender.send_messages(message)

        messages = []
        receiver = sb_client.get_queue_receiver(queue, max_wait_time=5, prefetch_count=0) 
        async with receiver:
            async for message in receiver:
                messages.append(message)
                await receiver.complete_message(message)
                if len(messages) >= 5:
                    break

            print(receiver._running)
            print(len(messages) == 5)

            async for message in receiver:
                print("Add another message")
                messages.append(message)
                await receiver.complete_message(message)
                if len(messages) >= 5:
                    break

        print(receiver._running==False)
        print(len(messages) == 6)

asyncio.run(main())