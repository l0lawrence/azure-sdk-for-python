from azure.servicebus import ServiceBusClient, ServiceBusMessage, ServiceBusReceiveMode, AutoLockRenewer
from concurrent.futures import ThreadPoolExecutor
from azure.servicebus.exceptions import ServiceBusError, AutoLockRenewTimeout
import time
import types
from azure.servicebus._common.utils import utc_now
import threading
import logging
import sys
from azure.servicebus._common.utils import utc_now

servicebus_namespace_connection_string = "Endpoint=sb://llawsb.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=9S5Xs8ht3zvIyExL+HOq/8wZeuj8d34NEOf/A08gWds="
queue = "l2"

logger = logging.getLogger("azure")
logger.setLevel(logging.DEBUG)
# handler = logging.StreamHandler(stream=sys.stdout)
# logger.addHandler(handler)


def sleep_until_expired(entity):
    time.sleep(max(0,(entity.locked_until_utc - utc_now()).total_seconds()+1))

with ServiceBusClient.from_connection_string(
    servicebus_namespace_connection_string, logging_enable=False) as sb_client:

    with sb_client.get_queue_sender(queue) as sender:
        for i in range(10):
            message = ServiceBusMessage(f"test {i}".format(i))
            sender.send_messages(message)

    renewer = AutoLockRenewer()
    messages = []
    with sb_client.get_queue_receiver(queue,
                                            max_wait_time=10,
                                            receive_mode=ServiceBusReceiveMode.PEEK_LOCK, 
                                            prefetch_count=10) as receiver:
        for message in receiver:
            if not messages:
                messages.append(message)
                print(message._lock_expired==False)
                renewer.register(receiver, message, max_lock_renewal_duration=10)
                print("Registered lock renew thread", message.locked_until_utc, utc_now())
                time.sleep(10)
                print("Finished first sleep", message.locked_until_utc)
                print(message._lock_expired==False)
                time.sleep(15) #generate autolockrenewtimeout error by going one iteration past.
                sleep_until_expired(message)
                print("Finished second sleep", message.locked_until_utc, utc_now())
                print(message._lock_expired==True)
                try:
                    receiver.complete_message(message)
                    # raise AssertionError("Didn't raise MessageLockLostError")
                except ServiceBusError as e:
                    print("auto lock timeout")
                    print(isinstance(e.inner_exception, AutoLockRenewTimeout))
            else:
                if message._lock_expired:
                    print("Remaining messages", message.locked_until_utc, utc_now())
                    print(message._lock_expired)
                    try:
                        print(message)
                        receiver.complete_message(message)
                    except ServiceBusError:
                        print("ServiceBusError")
                else:
                    print(message)
                    print(message.delivery_count >= 1)
                    print("Remaining messages", message.locked_until_utc, utc_now())
                    messages.append(message)
                    receiver.complete_message(message)
    renewer.close()
    print(len(messages))
    print(len(messages) == 11)

    # renewer = AutoLockRenewer(max_workers=8)
    # with sb_client.get_queue_sender(queue) as sender:
    #     for i in range(10):
    #         message = ServiceBusMessage("{}".format(i))
    #         sender.send_messages(message)

    # with sb_client.get_queue_receiver(queue,
    #                                         max_wait_time=10,
    #                                         receive_mode=ServiceBusReceiveMode.PEEK_LOCK,
    #                                         prefetch_count=10) as receiver:
    #     received_msgs = receiver.receive_messages(max_message_count=10, max_wait_time=5)
    #     for msg in received_msgs:
    #         renewer.register(receiver, msg, max_lock_renewal_duration=30)
    #     time.sleep(10)

    #     for msg in received_msgs:
    #         receiver.complete_message(msg)
    # print(len(received_msgs) == 10)
    # renewer.close()

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
    # print(len(received_msgs) == 2)
    # print(renewer._is_max_workers_greater_than_one==False)
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
    # print(len(received_msgs) == 3)
    # print(renewer._is_max_workers_greater_than_one)
    # renewer.close()
