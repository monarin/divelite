from time import sleep

async def aproducer(q, n):
    for i in range(n):
        await q.put(i)
    await q.put(None)

async def aconsumer(q):
    while True:
        item = await q.get()
        if item is None:
            break
        
        print("Async Got:", item)

from asyncio import Queue, get_event_loop
q = Queue()
loop = get_event_loop()
loop.create_task(aproducer(q, 10))
loop.run_until_complete(aconsumer(q))
