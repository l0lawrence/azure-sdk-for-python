# Stress Test Breakdown

Summary of ServiceBus stress tests --

```md
    -- test_stress_queues
        -- stress_test_base
            -- StressTestRunner
``````

## Coverage

### The Tests

- **queue**
    - Send/Iterator Receive
- **aqueue**:
    - Async Send/Iterator Receive
- **queuepull**:
    - Send/Receive
- **aqueuepull**:
    - Async Send/Receive
- **batch**:
    - Send Batch of size 5/Iterator Receive
- **abatch**:
    - Async Send Batch of size 5/Iterator Receive
- **queuew**:
    - Send/Iterator Receive with Websockets
- **aqueuew**:
    - Async Send/Iterator Receive with Websockets
- **queuepullw**:
    - Send/Receive with Websockets
- **aqueuepullw**:
    - Async Send/Receive with Websockets
- **batchw**:
    - Batch of 5 Send/Iterator Receive with Websockets
- **abatchw**:
    - Async Batch of 5 Send/Iterator Receive with Websockets
- **memray**:
    - Send/Receive with MemRay
- **amemray**:
    - Async Send/Receive with MemRay
    ```azurepowershell
    mkdir -p $DEBUG_SHARE && memray run --output $DEBUG_SHARE/sb_memray_output.bin test_stress_queues.py --method send_receive --duration 300000 --logging-enable
    ``````

### Customizable Arguments

- **conn-str**
- **queue_name**
- **method** -- name of the test you want to run
- **duration** -- duration of the test
- **logging-enable** -- enable logging
- **send-batch-size** -- size of batch to send (not used currently - default 100)
- **message-size** --
- **receive-type** -- pull/push receive
- **max_wait_time** -- max_wait_time of the receiver
- **max_message_count**-- Receive max_message_count
- **uamqp_mode** -- choose uamqp or pyamqp
- **transport** -- websockets or socket
- **debug_level** -- level of logging you want
