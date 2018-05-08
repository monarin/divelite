from asyncio import wait_for, wrap_future, get_event_loop

# coroutine checking ex.
import sys
def from_coroutine():
    return sys._getframe(2).f_code.co_flags & 0x380

def which_pill():
    if from_coroutine():
        print("Red")
    else:
        print("Blue")

def spam():
    which_pill()
    
async def aspam():
    which_pill()
    
spam()
loop = get_event_loop()
loop.run_until_complete(aspam())
