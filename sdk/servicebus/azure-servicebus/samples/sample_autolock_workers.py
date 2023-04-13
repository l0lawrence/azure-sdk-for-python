from azure.servicebus import ServiceBusClient, AutoLockRenewer, ServiceBusReceiveMode, ServiceBusMessage
from azure.servicebus.exceptions import AutoLockRenewTimeout, ServiceBusError
import time
from concurrent.futures import ThreadPoolExecutor
from azure.servicebus._common.utils import utc_now

connection_str = "Endpoint=sb://llawsb.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=9S5Xs8ht3zvIyExL+HOq/8wZeuj8d34NEOf/A08gWds="
queue = "q2"


with ServiceBusClient.from_connection_string(
        connection_str, logging_enable=False) as sb_client:

        renewer = AutoLockRenewer(max_workers=8)
        print("AutoLock Renewer Workers is 8")
        with sb_client.get_queue_sender(queue) as sender:
            for i in range(10):
                message = ServiceBusMessage("{}".format(i))
                sender.send_messages(message)

        with sb_client.get_queue_receiver(queue,
                                                max_wait_time=10,
                                                receive_mode=ServiceBusReceiveMode.PEEK_LOCK,
                                                prefetch_count=10) as receiver:
            received_msgs = receiver.receive_messages(max_message_count=10, max_wait_time=5)
            for msg in received_msgs:
                renewer.register(receiver, msg, max_lock_renewal_duration=30)
            time.sleep(10)

            for msg in received_msgs:
                receiver.complete_message(msg)
        print(f" We have received 10 messages {len(received_msgs) == 10}")
        renewer.close()

        # executor = ThreadPoolExecutor(max_workers=1)
        # renewer = AutoLockRenewer(executor=executor)
        # with sb_client.get_queue_sender(queue) as sender:
        #     for i in range(2):
        #         message = ServiceBusMessage("{}".format(i))
        #         sender.send_messages(message)

        # with sb_client.get_queue_receiver(queue,
        #                                         max_wait_time=10,
        #                                         receive_mode=ServiceBusReceiveMode.PEEK_LOCK,
        #                                         prefetch_count=3) as receiver:
        #     received_msgs = receiver.receive_messages(max_message_count=3, max_wait_time=10)
        #     for msg in received_msgs:
        #         renewer.register(receiver, msg, max_lock_renewal_duration=30)
        #     time.sleep(10)

        #     for msg in received_msgs:
        #         receiver.complete_message(msg)
        # assert len(received_msgs) == 2
        # assert not renewer._is_max_workers_greater_than_one
        # renewer.close()

        # executor = ThreadPoolExecutor(max_workers=2)
        # renewer = AutoLockRenewer(executor=executor)
        # with sb_client.get_queue_sender(queue) as sender:
        #     for i in range(3):
        #         message = ServiceBusMessage("{}".format(i))
        #         sender.send_messages(message)

        # with sb_client.get_queue_receiver(queue,
        #                                         max_wait_time=10,
        #                                         receive_mode=ServiceBusReceiveMode.PEEK_LOCK,
        #                                         prefetch_count=3) as receiver:
        #     received_msgs = receiver.receive_messages(max_message_count=3, max_wait_time=10)
        #     for msg in received_msgs:
        #         renewer.register(receiver, msg, max_lock_renewal_duration=30)
        #     time.sleep(10)

        #     for msg in received_msgs:
        #         receiver.complete_message(msg)
        # assert len(received_msgs) == 3
        # assert renewer._is_max_workers_greater_than_one
        # renewer.close()
