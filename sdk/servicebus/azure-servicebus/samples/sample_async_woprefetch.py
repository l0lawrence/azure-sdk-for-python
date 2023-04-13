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


        def message_content():
            for i in range(20):
                yield ServiceBusMessage(
                    body="ServiceBusMessage no. {}".format(i),
                    subject='1st'
                )

        sender = sb_client.get_queue_sender(queue)
        receiver = sb_client.get_queue_receiver(queue)

        async with sender, receiver:
            message = ServiceBusMessageBatch()
            for each in message_content():
                message.add_message(each)
            await sender.send_messages(message)

            receive_counter = 0
            message_1st_received_cnt = 0
            message_2nd_received_cnt = 0
            while message_1st_received_cnt < 20 or message_2nd_received_cnt < 20:
                messages = []
                batch = await receiver.receive_messages(max_message_count=20, max_wait_time=5)
                while batch:
                    messages += batch
                    batch = await receiver.receive_messages(max_message_count=20, max_wait_time=5)
                if not messages:
                    break
                receive_counter += 1
                for message in messages:
                    if message.subject == '1st':
                        message_1st_received_cnt += 1
                        print(f"First message {message}")
                        print(message.subject)
                        await receiver.complete_message(message)
                        message.subject = '2nd'
                        await sender.send_messages(message)  # resending received message
                    elif message.subject == '2nd':
                        message_2nd_received_cnt += 1
                        print(f"Second message {message}")
                        print(message.subject)
                        await receiver.complete_message(message)

            print(message_1st_received_cnt == 20 and message_2nd_received_cnt == 20)
            # Network/server might be unstable making flow control ineffective in the leading rounds of connection iteration
            print(receive_counter < 10)  # Dynamic link credit issuing come info effect

asyncio.run(main())