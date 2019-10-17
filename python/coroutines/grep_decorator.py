# This ex wraps grep generator with coroutine def that
# activates the incoming generator with next statement.
# Coroutine is usually a consumer - the "line = (yield)"
# get unblocked when it receives something via g.send - see below:
#
# g = grep("python") # will start running right away (with coroutine wrapper below)
# g.send("python hello") # unblock yield line
# g.close() # throw GeneratorExit

def coroutine(func):
    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        next(cr)
        return cr
    return start

@coroutine
def grep(pattern):
    print("looking for %s"%pattern)
    try:
        while True:
            line = (yield)
            if pattern in line:
                print(line)
    except GeneratorExit:
        print("Going away.")

from IPython import embed
embed()

