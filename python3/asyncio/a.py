import asyncio
async def greeting(name):
    return 'Hello %s'%name

g = greeting('Guido')
print(g)

# Rule 1: async functions dont' run themselves
loop = asyncio.get_event_loop()
loop.run_until_complete(g)

# Rule 2: async functions can call other asyncs
async def spam():
    names = ['Guido', 'Paula', 'Lewis']
    for name in names:
        print(await greeting(name))

loop.run_until_complete(spam())

#await cannot be done outside async function

# Rule 3: Don't talk about how it works
# Rule 4: asyncio LOVES nonblocking
from thread_q import Queuey
q = Queuey(2)
item, fut = q.get_noblock()
print(fut)

from asyncio import wrap_future, wait_for
async def spam():
    item = await wait_for(wrap_future(fut), None)
    print('Got:', item)

from threading import Thread
from time import sleep
Thread(target=lambda:(sleep(15), q.put_sync(42))).start()
loop.run_until_complete(spam())
