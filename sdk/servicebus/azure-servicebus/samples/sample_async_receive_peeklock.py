from azure.servicebus.aio import ServiceBusClient
from azure.servicebus import ServiceBusMessage, ServiceBusMessageBatch
from azure.servicebus.exceptions import ServiceBusError
from azure.servicebus._common.utils import utc_now
import time
import threading
import asyncio

connection_str = "Endpoint=sb://llawsb.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=9S5Xs8ht3zvIyExL+HOq/8wZeuj8d34NEOf/A08gWds="
queue = "lock7"


async def main():
        async with ServiceBusClient.from_connection_string(
            connection_str, logging_enable=False) as sb_client:

            sender = sb_client.get_queue_sender(queue)
            async with sender:
                for i in range(10):
                    message = ServiceBusMessage("Handler message no. {}".format(i))
                    await sender.send_messages(message, timeout=5)

                # Test that noop empty send works properly.
                await sender.send_messages([])
                await sender.send_messages(ServiceBusMessageBatch())
                print(len(await sender.schedule_messages([], utc_now())) == 0)
                await sender.cancel_scheduled_messages([])

            # Then test expected failure modes.
            # try:
            #     await sender.send_messages(ServiceBusMessage('msg'))
            # except ValueError:
            #     print("Val Er 1")
            # try:
            #     await sender.schedule_messages(ServiceBusMessage('msg'), utc_now())
            # except ValueError:
            #     print("Val Er 2")
            # try:
            #     await sender.cancel_scheduled_messages([1, 2, 3])
            # except ValueError:
            #     print("Val Er 3")

            # try:
            #     await (sb_client.get_queue_receiver(queue, session_id="test", max_wait_time=5))._open_with_retry()
            # except ServiceBusError:
            #     print("Should SB error")

            # try:
            #     sb_client.get_queue_receiver(queue, max_wait_time=0)
            # except:
            #     print("Should value err here")

            receiver = sb_client.get_queue_receiver(queue, max_wait_time=5)
            async with receiver:
                print(len(await receiver.receive_deferred_messages([])) == 0)
                try:
                    await receiver.receive_messages(max_wait_time=0)
                except Exception as e:
                    print(f"Raise {e}")

                try:
                    await receiver._get_streaming_message_iter(max_wait_time=0)
                except ValueError:
                    print("Gives val error")

                count = 0
                async for message in receiver:
                    count += 1
                    await receiver.complete_message(message)

            print(count == 10)
            print(count)

            # with pytest.raises(ValueError):
            #     await receiver.receive_messages()
            # with pytest.raises(ValueError):
            #     async with receiver:
            #         raise AssertionError("Should raise ValueError")
            # with pytest.raises(ValueError):
            #     await receiver.receive_deferred_messages([1, 2, 3])
            # with pytest.raises(ValueError):
            #     await receiver.peek_messages()

asyncio.run(main())