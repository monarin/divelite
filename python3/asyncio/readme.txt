q.py, q_and_threads.py
    A queue object that is used by producer and consumer.
    There is no wait for free-up space when try to put.
    There is no wait for item for get.

noblock_q.py
    With Future, the queue object can wait for get and put.

thread_q.py
    Use Future in get_sync and put_sync to wait for an empty 
    space or item.

asyncio_q.py

