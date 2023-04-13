from azure.servicebus import ServiceBusMessage, ServiceBusClient
from azure.servicebus.exceptions import ServiceBusError
import time
import threading

connection_str = "Endpoint=sb://llawsb.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=9S5Xs8ht3zvIyExL+HOq/8wZeuj8d34NEOf/A08gWds="
queue = "lock5"



with ServiceBusClient.from_connection_string(connection_str, logging_enable=False) as sb_client:

# test releasing messages when prefetch is 1 and link credits are issue dynamically
        receiver = sb_client.get_queue_receiver(queue, max_wait_time=10)
        sender = sb_client.get_queue_sender(queue)
        with sender, receiver:
                # send 5 msgs to queue first
            sender.send_messages([ServiceBusMessage('test') for _ in range(5)])
            first_time = True
            iterator_recv_cnt = 0

            # case: iterator + receive batch
            for msg in receiver:
                print(msg.delivery_count == 0)  # release would not increase delivery count
                receiver.complete_message(msg)
                iterator_recv_cnt += 1
                if first_time:  # for the first time, we call nested receive message call
                    received_msgs = []

                    while len(received_msgs) < 4:  # there supposed to be 5 msgs in the queue
                        # we issue 10 link credits, leaving more credits on the wire
                        for sub_msg in receiver.receive_messages(max_message_count=10, max_wait_time=5):
                            print(sub_msg.delivery_count == 0)
                            receiver.complete_message(sub_msg)
                            received_msgs.append(sub_msg)
                    print(len(received_msgs) == 4)
                    sender.send_messages([ServiceBusMessage('test') for _ in range(10)])
                    time.sleep(15)  # sleep > message expiration time

                    received_msgs = []
                    target_msgs_count = 5  # we want to receive 5 with the receive message call
                    while len(received_msgs) < target_msgs_count:
                        for sub_msg in receiver.receive_messages(
                                max_message_count=target_msgs_count - len(received_msgs), max_wait_time=5):
                            print(sub_msg.delivery_count == 0)  # release would not increase delivery count
                            receiver.complete_message(sub_msg)
                            received_msgs.append(sub_msg)
                    print(len(received_msgs) == target_msgs_count)
                    first_time = False
                    print("LOOP BACK TO TOP")
            assert iterator_recv_cnt == 6  # 1 before nested receive message call + 5 after nested receive message call

            # case: iterator + iterator case
            sender.send_messages([ServiceBusMessage('test') for _ in range(10)])
            outter_recv_cnt = 0
            inner_recv_cnt = 0
            for msg in receiver:
                assert msg.delivery_count == 0
                outter_recv_cnt += 1
                receiver.complete_message(msg)
                for sub_msg in receiver:
                    assert sub_msg.delivery_count == 0
                    inner_recv_cnt += 1
                    receiver.complete_message(sub_msg)
                    if inner_recv_cnt == 5:
                        time.sleep(15)  # innner finish receiving first 5 messages then sleep until lock expiration
                        break
            assert outter_recv_cnt == 1
            outter_recv_cnt = 0
            for msg in receiver:
                assert msg.delivery_count == 0
                outter_recv_cnt += 1
                receiver.complete_message(msg)
            assert outter_recv_cnt == 4
