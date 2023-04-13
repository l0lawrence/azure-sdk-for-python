from azure.servicebus import ServiceBusClient, ServiceBusMessage, ServiceBusReceiveMode, AutoLockRenewer
from azure.servicebus.exceptions import ServiceBusError
import time
import types
from azure.servicebus._common.utils import utc_now
import threading
import logging
import sys

servicebus_namespace_connection_string = "Endpoint=sb://llawsb.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=9S5Xs8ht3zvIyExL+HOq/8wZeuj8d34NEOf/A08gWds="
queue = "q14"

# logger = logging.getLogger("azure")
# logger.setLevel(logging.DEBUG)
# handler = logging.StreamHandler(stream=sys.stdout)
# logger.addHandler(handler)



with ServiceBusClient.from_connection_string(
    servicebus_namespace_connection_string, logging_enable=False) as sb_client:

    # def sub_test_releasing_messages():
    #     print("SUB RELEASE")
    #     # test releasing messages when prefetch is 1 and link credits are issue dynamically
    #     receiver = sb_client.get_queue_receiver(queue)
    #     sender = sb_client.get_queue_sender(queue)
    #     with sender, receiver:
    #         # send 10 msgs to queue first
    #         sender.send_messages([ServiceBusMessage('test') for _ in range(5)])

    #         received_msgs = []
    #         # the amount of messages returned by receive call is not stable, especially in live tests
    #         # of different os platforms, this is why a while loop is used here to receive the specific
    #         # amount of message we want to receive
    #         while len(received_msgs) < 5:
    #             # issue link credits more than 5, client should consume 5 msgs from the service in total,
    #             # leaving the extra credits on the wire
    #             for msg in receiver.receive_messages(max_message_count=10, max_wait_time=5):
    #                 receiver.complete_message(msg)
    #                 received_msgs.append(received_msgs)
    #         print(len(received_msgs) == 5)

    #         # send 5 more messages, those messages would arrive at the client while the program is sleeping
    #         sender.send_messages([ServiceBusMessage('test') for _ in range(5)])
    #         time.sleep(15)  # sleep > message expiration time

    #         target_msgs_count = 5
    #         received_msgs = []
    #         while len(received_msgs) < target_msgs_count:
    #             # issue 10 link credits, client should consume 5 msgs from the service, leaving no link credits
    #             for msg in receiver.receive_messages(max_message_count=target_msgs_count - len(received_msgs),
    #                                                     max_wait_time=5):
    #                 print(msg.delivery_count == 0)  # release would not increase delivery count
    #                 receiver.complete_message(msg)
    #                 received_msgs.append(msg)
    #         print("GOT 5")
    #         print(len(received_msgs) == 5)

    # def sub_test_releasing_messages_iterator():
    #     print("SUB RELEASE ITERATOR")
    #     # test nested iterator scenario
    #     receiver = sb_client.get_queue_receiver(queue, max_wait_time=10)
    #     sender = sb_client.get_queue_sender(queue)
    #     with sender, receiver:
    #         # send 5 msgs to queue first
    #         sender.send_messages([ServiceBusMessage('test') for _ in range(5)])
    #         first_time = True
    #         iterator_recv_cnt = 0

    #         # case: iterator + receive batch
    #         for msg in receiver:
    #             print(msg.delivery_count == 0)  # release would not increase delivery count
    #             receiver.complete_message(msg)
    #             iterator_recv_cnt += 1
    #             if first_time:  # for the first time, we call nested receive message call
    #                 received_msgs = []

    #                 while len(received_msgs) < 4:  # there supposed to be 5 msgs in the queue
    #                     # we issue 10 link credits, leaving more credits on the wire
    #                     for sub_msg in receiver.receive_messages(max_message_count=10, max_wait_time=5):
    #                         print(sub_msg.delivery_count == 0)
    #                         receiver.complete_message(sub_msg)
    #                         received_msgs.append(sub_msg)
    #                 print(len(received_msgs) == 4)
    #                 sender.send_messages([ServiceBusMessage('test') for _ in range(10)])
    #                 time.sleep(15)  # sleep > message expiration time

    #                 received_msgs = []
    #                 target_msgs_count = 5  # we want to receive 5 with the receive message call
    #                 while len(received_msgs) < target_msgs_count:
    #                     for sub_msg in receiver.receive_messages(
    #                             max_message_count=target_msgs_count - len(received_msgs), max_wait_time=5):
    #                         print(sub_msg.delivery_count == 0)  # release would not increase delivery count
    #                         receiver.complete_message(sub_msg)
    #                         received_msgs.append(sub_msg)
    #                 print(len(received_msgs) == target_msgs_count)
    #                 first_time = False
    #         print("Iterator recv cnt")
    #         # this is wrong 
    #         print(iterator_recv_cnt == 6)  # 1 before nested receive message call + 5 after nested receive message call

    #         # case: iterator + iterator case
    #         sender.send_messages([ServiceBusMessage('test') for _ in range(10)])
    #         outter_recv_cnt = 0
    #         inner_recv_cnt = 0
    #         for msg in receiver:
    #             print(msg.delivery_count == 0)
    #             outter_recv_cnt += 1
    #             receiver.complete_message(msg)
    #             for sub_msg in receiver:
    #                 print(sub_msg.delivery_count == 0)
    #                 inner_recv_cnt += 1
    #                 receiver.complete_message(sub_msg)
    #                 if inner_recv_cnt == 5:
    #                     time.sleep(15)  # innner finish receiving first 5 messages then sleep until lock expiration
    #                     break
    #         print(outter_recv_cnt == 1)
    #         outter_recv_cnt = 0
    #         for msg in receiver:
    #             print(msg.delivery_count == 0)
    #             outter_recv_cnt += 1
    #             receiver.complete_message(msg)
    #         print("OUTER RECV COUNT")
    #         print(outter_recv_cnt == 4)


    def _hack_disable_receive_context_message_received(self, frame, message):
        print("put messages")
        # pylint: disable=protected-access
        self._handler._received_messages.put((frame, message))

    def sub_test_non_releasing_messages():
        print("NO RELEASE MSG")
        # test not releasing messages when prefetch is not 1
        receiver = sb_client.get_queue_receiver(queue)
        sender = sb_client.get_queue_sender(queue)

        with sender, receiver:
            # send 5 msgs to queue first
            sender.send_messages([ServiceBusMessage('test') for _ in range(5)])
            receiver._handler._link._on_transfer = types.MethodType(
                _hack_disable_receive_context_message_received, receiver)
            received_msgs = []
            while len(received_msgs) < 5:
                # issue 10 link credits, client should consume 5 msgs from the service
                # leaving 5 credits on the wire
                for msg in receiver.receive_messages(max_message_count=10, max_wait_time=5):
                    receiver.complete_message(msg)
                    received_msgs.append(msg)
            print(len(received_msgs) == 5)

            # send 5 more messages, those messages would arrive at the client while the program is sleeping
            sender.send_messages([ServiceBusMessage('test') for _ in range(5)])
            time.sleep(15)  # sleep > message expiration time

            # issue 5 link credits, client should consume 5 msgs from the internal buffer which is already lock expired
            target_msgs_count = 5
            received_msgs = []
            while len(received_msgs) < target_msgs_count:
                received_msgs.extend(receiver.receive_messages(max_message_count=5, max_wait_time=5))
            print(len(received_msgs) == 5)
            for msg in received_msgs:
                # queue ordering I think
                print(msg.delivery_count == 0)
                try:
                    receiver.complete_message(msg)
                except ServiceBusError:
                    print("ERRORED")

            # re-received message with delivery count increased
            target_msgs_count = 5
            received_msgs = []
            while len(received_msgs) < target_msgs_count:
                received_msgs.extend(receiver.receive_messages(max_message_count=5, max_wait_time=5))
            print(len(received_msgs) == 5)
            for msg in received_msgs:
                print(msg.delivery_count > 0)
                receiver.complete_message(msg)

    # sub_test_releasing_messages()
    # sub_test_releasing_messages_iterator()
    sub_test_non_releasing_messages()
