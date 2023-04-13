from azure.servicebus import ServiceBusClient, ServiceBusMessage, ServiceBusReceiveMode, AutoLockRenewer
from azure.servicebus.exceptions import ServiceBusError
import time
from azure.servicebus._common.utils import utc_now



servicebus_namespace_connection_string = "Endpoint=sb://llawsb.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=9S5Xs8ht3zvIyExL+HOq/8wZeuj8d34NEOf/A08gWds="
queue = "lock5"

def sleep_until_expired(entity):
    time.sleep(max(0,(entity.locked_until_utc - utc_now()).total_seconds()+1))

with ServiceBusClient.from_connection_string(
        servicebus_namespace_connection_string, logging_enable=False) as sb_client:

        with sb_client.get_queue_sender(queue) as sender:
            # The 10 iterations is "important" because it gives time for the timed out message to be received again.
            for i in range(10):
                message = ServiceBusMessage("{}".format(i))
                sender.send_messages(message)
        print("Sent messages")
        # renewer = AutoLockRenewer(max_lock_renewal_duration=10)
        renewer = AutoLockRenewer()
        messages = []
        with sb_client.get_queue_receiver(queue,
                                                max_wait_time=10,
                                                receive_mode=ServiceBusReceiveMode.PEEK_LOCK, 
                                                prefetch_count=10,
                                                auto_lock_renewer=renewer) as receiver:
            for message in receiver:
                print("Running receive")
                if not messages:
                    messages.append(message)
                    print(message._lock_expired)
                    renewer.register(receiver, message, max_lock_renewal_duration=10)

                    time.sleep(10)
                    
                    print("Finished first sleep", message.locked_until_utc)
                    print(message._lock_expired)
                    print("SLEEP")
                    time.sleep(15) #generate autolockrenewtimeout error by going one iteration past.
                    sleep_until_expired(message)
                    print("DONE SLEEP")
                    # If this sleeps for 25 seconds, our receiver is going to time out 
                    print(message._lock_expired)
                    try:
                        receiver.complete_message(message)
                    except ServiceBusError as e:
                        print(e)
                else:
                    if message._lock_expired:
                        print(message._lock_expired)
                        try:
                             receiver.complete_message(message)
                        except:
                            print("This should error here")
                    else:
                        print(message.delivery_count >= 1)
                        messages.append(message)
                        receiver.complete_message(message)
        renewer.close()
        print(len(messages) == 11)
        print(len(messages))
