from azure.servicebus import ServiceBusClient, ServiceBusMessage, ServiceBusReceiveMode, ServiceBusReceivedMessage
from azure.servicebus.exceptions import ServiceBusError
import time
import types
from azure.servicebus._common.utils import utc_now
import threading
import logging
import sys
from datetime import timedelta

servicebus_namespace_connection_string = "Endpoint=sb://llawsb.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=9S5Xs8ht3zvIyExL+HOq/8wZeuj8d34NEOf/A08gWds="
queue = "q14"

logger = logging.getLogger("uamqp")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)





with ServiceBusClient.from_connection_string(
    servicebus_namespace_connection_string, logging_enable=True) as sb_client:

    receiver = sb_client.get_queue_receiver(queue,
                                    max_wait_time=5,
                                    receive_mode=ServiceBusReceiveMode.PEEK_LOCK)
    sender = sb_client.get_queue_sender(queue)
    with receiver, sender:
        for i in range(1):
            message = ServiceBusMessage(
                body=b"Test message",
                application_properties={'key': b'value'},
                subject='label',
                content_type='application/text',
                correlation_id='cid',
                message_id='mid',
                to='to',
                reply_to='reply_to',
                time_to_live=timedelta(seconds=60)
            )
            print("FIRST MSG")
            sender.send_messages(message)

            # encode application properties-- debug here 
            # print out encoded bytes at transport level of the message 
        # messages = receiver.receive_messages(5)
        # print(len(messages) > 0)
        # print(all(isinstance(m, ServiceBusReceivedMessage) for m in messages))
        # for message in messages:
        #     # print_message(_logger, message)
        #     assert b''.join(message.body) == b'Test message'
        #     assert message.application_properties[b'key'] == b'value'
        #     assert message.subject == 'label'
        #     assert message.content_type == 'application/text'
        #     assert message.correlation_id == 'cid'
        #     assert message.message_id == 'mid'
        #     assert message.to == 'to'
        #     assert message.reply_to == 'reply_to'
        #     assert message.time_to_live == timedelta(seconds=60)
        #     try:
        #         receiver.complete_message(message)
        #     except ValueError as e:
        #         print("VALUE ERROR")
        #         print(e)

        #     print("TRY TO RESEND MESSAGE")
        #     sender.send_messages(message)

        # cnt = 0
        # for message in receiver:
        #     assert b''.join(message.body) == b'Test message'
        #     assert message.application_properties[b'key'] == b'value'
        #     assert message.subject == 'label'
        #     assert message.content_type == 'application/text'
        #     assert message.correlation_id == 'cid'
        #     assert message.message_id == 'mid'
        #     assert message.to == 'to'
        #     assert message.reply_to == 'reply_to'
        #     assert message.time_to_live == timedelta(seconds=60)
        #     receiver.complete_message(message)
        #     cnt += 1
        # assert cnt == 10