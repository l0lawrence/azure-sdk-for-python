from azure.servicebus import ServiceBusMessage, ServiceBusClient
from azure.servicebus.exceptions import ServiceBusError
import time
import threading

connection_str = "Endpoint=sb://llawsb.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=9S5Xs8ht3zvIyExL+HOq/8wZeuj8d34NEOf/A08gWds="
queue = "lock5"




with ServiceBusClient.from_connection_string(connection_str, logging_enable=False) as sb_client:
    import types
    # test nested iterator scenario
    receiver = sb_client.get_queue_receiver(queue, max_wait_time=10)
    sender = sb_client.get_queue_sender(queue)

    def _hack_disable_receive_context_message_received(self, message):
        # pylint: disable=protected-access
        print("Callback should be here instead")
        # self._handler._was_message_received = True
        self._handler._received_messages.put(message)

    with sender, receiver:
        # send 5 msgs to queue first
        sender.send_messages([ServiceBusMessage(f'testONE {_}') for _ in range(5)])
        receiver._handler._message_received = types.MethodType(
            _hack_disable_receive_context_message_received, receiver)
        received_msgs = []
        while len(received_msgs) < 5:
            # issue 10 link credits, client should consume 5 msgs from the service
            # leaving 5 credits on the wire
            for msg in receiver.receive_messages(max_message_count=10, max_wait_time=5):
                receiver.complete_message(msg)
                received_msgs.append(msg)
        print(len(received_msgs) == 5)
        print(len(received_msgs))
        print("DONE WITH THIS")

       # send 5 more messages, those messages would arrive at the client while the program is sleeping
        sender.send_messages([ServiceBusMessage(f'test {_}') for _ in range(5)])
        print("SLEEP")
        time.sleep(15)  # sleep > message expiration time
        print("DONE SLEEP")

        # issue 5 link credits, client should consume 5 msgs from the internal buffer which is already lock expired
        target_msgs_count = 5
        received_msgs = []
        while len(received_msgs) < target_msgs_count:
            received_msgs.extend(receiver.receive_messages(max_message_count=5, max_wait_time=5))
        print(f"Got the first 5 expired messages now {len(received_msgs) == 5}")
        for msg in received_msgs:
            print(f"Delivery count doesnt increment {msg.delivery_count == 0}")
            # try:
            print("Try to complete messages")
            receiver.complete_message(msg)
        #     except ServiceBusError:
        #         print("They should Fail")


        # # this section of the test is expecting that the 
        # target_msgs_count = 5
        # received_msgs = []
        # while len(received_msgs) < target_msgs_count:
        #     received_msgs.extend(receiver.receive_messages(max_message_count=5, max_wait_time=5))
        # print(f"Get the next 5 messages which are not lock expired {len(received_msgs) == 5}")
        # for msg in received_msgs:

        #     print("next")
        #     print(f"Delivery count is incrementing {msg.delivery_count > 0}")
        #     receiver.complete_message(msg)