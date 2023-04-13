from azure.servicebus import ServiceBusClient, ServiceBusMessage, ServiceBusReceiveMode, AutoLockRenewer
from azure.servicebus.exceptions import ServiceBusError
import time
import types
from azure.servicebus._common.utils import utc_now
import threading
import logging
import sys

servicebus_namespace_connection_string = "Endpoint=sb://llawsb.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=9S5Xs8ht3zvIyExL+HOq/8wZeuj8d34NEOf/A08gWds="
queue = "q10"


def _hack_disable_receive_context_message_received(self, frame, message):
        # pylint: disable=protected-access
        print("HERE")
        print(receiver._handler._link.current_link_credit)
        self._handler._received_messages.put((frame, message))

with ServiceBusClient.from_connection_string(
    servicebus_namespace_connection_string, logging_enable=False) as sb_client:


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
        print(receiver._handler._link.current_link_credit)
        print("START")
        time.sleep(15)  # sleep > message expiration time
        print("END SLEEP")
        print(receiver._handler._link.current_link_credit)

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
                print("ERR")

        # re-received message with delivery count increased
        target_msgs_count = 5
        received_msgs = []
        while len(received_msgs) < target_msgs_count:
            received_msgs.extend(receiver.receive_messages(max_message_count=5, max_wait_time=5))
        print(len(received_msgs) == 5)
        for msg in received_msgs:
            print(msg.delivery_count > 0)
            receiver.complete_message(msg)