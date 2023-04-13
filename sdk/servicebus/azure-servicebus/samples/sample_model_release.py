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

logger = logging.getLogger("azure")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)

with ServiceBusClient.from_connection_string(
    servicebus_namespace_connection_string, logging_enable=True) as sb_client:
    
        # test not releasing messages when prefetch is not 1
        receiver = sb_client.get_queue_receiver(queue)
        sender = sb_client.get_queue_sender(queue)

        def _hack_disable_receive_context_message_received(self, frame, message):
            # pylint: disable=protected-access
            # self._handler._was_message_received = True
            # print(receiver._prefetch_count)
            # print(self._handler.link_credit)
            print(receiver._handler._link.current_link_credit)
            print(f"Put messages {threading.current_thread().name}")
            self._handler._received_messages.put((frame, message))
    
        def _hack_disable_receive_context_message_received_a(self, message):
            # pylint: disable=protected-access
            # self._handler._was_message_received = True
            # print(self._handler._connection._prefetch)
            # print(self._handler._link_properties.get("_prefetch"))
            print(f"Put messages {threading.current_thread().name}")
            self._handler._received_messages.put(message)

        with sender, receiver:
            # send 5 msgs to queue first
            sender.send_messages([ServiceBusMessage('test') for _ in range(5)])
            # receiver._handler.message_handler.on_message_received = types.MethodType(
            #     _hack_disable_receive_context_message_received_a, receiver)
            receiver._handler._link._on_transfer = types.MethodType(
                _hack_disable_receive_context_message_received, receiver)
            received_msgs = []
            while len(received_msgs) < 5:
                # issue 10 link credits, client should consume 5 msgs from the service
                # leaving 5 credits on the wire
                for msg in receiver.receive_messages(max_message_count=10, max_wait_time=5):
                    print("Complete first 5 messages")
                    receiver.complete_message(msg)
                    received_msgs.append(msg)
                print("Got the 5 messages")
                print(len(received_msgs) == 5)

            # link credit should be 10-5 = 5

            # send 5 more messages, those messages would arrive at the client while the program is sleeping
            # for i in [ServiceBusMessage(f'test {_}') for _ in range(5)]:
            #     sender.send_messages(i)
            sender.send_messages([ServiceBusMessage(f'test {_}') for _ in range(5)])
            # print(receiver._handler.message_handler._link.current_link_credit)

            print("SLEEP")
            time.sleep(15)  # sleep > message expiration time
            print("END SLEEP")
            # print(receiver._handler.message_handler._link.current_link_credit)


            # issue 5 link credits, client should consume 5 msgs from the internal buffer which is already lock expired
            target_msgs_count = 5
            received_msgs = []
            while len(received_msgs) < target_msgs_count:
                print("Receive Messages")
                received_msgs.extend(receiver.receive_messages(max_message_count=5, max_wait_time=5))
         

            for msg in received_msgs:
                # queue ordering I think
                # print(msg.delivery_count == 0)
                print(msg)
                try: 
                    receiver.complete_message(msg)
                    print("Completes")
                except ServiceBusError:
                    print("It should Errored")
     
            # # re-received message with delivery count increased
            # print("Receive Again")
            target_msgs_count = 5
            received_msgs = []
            while len(received_msgs) < target_msgs_count:
                received_msgs.extend(receiver.receive_messages(max_message_count=5, max_wait_time=5))
            print(len(received_msgs) == 5)
            for msg in received_msgs:
                print(msg.delivery_count > 0)
                receiver.complete_message(msg)
        print("Oustide of with")

# Prefetch count being incorrect 
# What frames are you getting from the main thread that the keep alive isn't
# state in the connection, move lock to connection?



# uamqp link credit be reset, pyamqp link credit is not on the keep alive