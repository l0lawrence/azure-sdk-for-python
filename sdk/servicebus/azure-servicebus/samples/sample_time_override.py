
from azure.servicebus import ServiceBusClient, ServiceBusMessage, ServiceBusReceiveMode, AutoLockRenewer
from azure.servicebus.exceptions import ServiceBusError
import time
import types
from azure.servicebus._common.utils import utc_now
import threading
import logging
import sys
from datetime import datetime, timedelta

servicebus_namespace_connection_string = "Endpoint=sb://llawsb.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=9S5Xs8ht3zvIyExL+HOq/8wZeuj8d34NEOf/A08gWds="
queue = "q11"

with ServiceBusClient.from_connection_string(
        servicebus_namespace_connection_string,
        logging_enable=False) as sb_client:

    with sb_client.get_queue_sender(queue) as sender:
        message = ServiceBusMessage("0")
        sender.send_messages(message)

        messages = []
        receiver2= sb_client.get_queue_receiver(queue, max_wait_time=1)
        with sb_client.get_queue_receiver(queue, max_wait_time=10) as receiver:
            

            time_1 = time.time()
            time_3 = time_1 # In case inner loop isn't hit, fail sanely.
            # for message in receiver._get_streaming_message_iter(max_wait_time=10):
            for message in receiver: # time is 5
                print('Got Message sent ')
                messages.append(message)
                receiver.complete_message(message)

                time_2 = time.time()
                print("Set time 2")
                # for message in receiver._get_streaming_message_iter(max_wait_time=1):
                for message in receiver2:
                    print("Got msg")
                    messages.append(message)
                print("Set time 3")
                time_3 = time.time()

                
                print(f"Time 2 time 3 compare {timedelta(seconds=(time_3 - time_2))}")
                print(timedelta(seconds=.5) < timedelta(seconds=(time_3 - time_2)) <= timedelta(seconds=2))


            time_4 = time.time()
            print(f"Time 4 time 3 compare {timedelta(seconds=(time_4 - time_3))}")
            print(timedelta(seconds=8) < timedelta(seconds=(time_4 - time_3)) <= timedelta(seconds=11))


            # for message in receiver._get_streaming_message_iter(max_wait_time=3):
            #     print("Got messages 1")
            #     messages.append(message)
            # time_5 = time.time()
            # print(f"Time 5 time 4 compare {timedelta(seconds=(time_5 - time_4))}")
            # print(timedelta(seconds=1) < timedelta(seconds=(time_5 - time_4)) <= timedelta(seconds=4))

            # for message in receiver:
            #     print("Got messages 2")
            #     messages.append(message)
            # time_6 = time.time()
            # print(f"Time 6 time 5 compare {timedelta(seconds=(time_6 - time_5))}")
            # print(timedelta(seconds=3) < timedelta(seconds=(time_6 - time_5)) <= timedelta(seconds=6))

            # for message in receiver._get_streaming_message_iter():
            #     print("Got messages 3")
            #     messages.append(message)
            # time_7 = time.time()
            # print(f"Time 7 time 6 compare {timedelta(seconds=(time_7 - time_6))}")
            # print(timedelta(seconds=3) < timedelta(seconds=(time_7 - time_6)) <= timedelta(seconds=6))
            # print(len(messages) == 1)