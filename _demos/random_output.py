import time
import random
import asyncio
from collections import deque
from intermezzo import Intermezzo as mzo

def draw():
    w, h = mzo.size()
    mzo.clear(mzo.color("Default"), mzo.color("Default"))
    for y in range(0, h):
        for x in range(0, w):
            # rand.Int() in Go: returns a non-neg. pseudo-random int from default Source
            # default Source represents source of uniformly-distributed pseudo-random
            # int64 values in the range [0, 1<<63]
            mzo.set_cell(x, y, ' ', mzo.color("Default"), (random.randint(0, 1<<63)%8)+1)
    mzo.flush()

evt_queue = deque()
def _polling():
    while True:
        evt = mzo.poll_event()
        evt_queue.append(evt)
        if evt["Type"] == mzo.event("Key") and evt["Key"] == mzo.key("Esc"):
            break

async def main():
    err = mzo.init()
    if err:
        raise(Exception(err))
    draw()
    while True:
        try:
            evt = evt_queue.popleft()
        except:
            evt = {"Type": None, "Key": 0}
        if evt["Type"] == mzo.event("Key") and evt["Key"] == mzo.key("Esc"):
            is_running = False
            break
        draw()
        time.sleep(0.01)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, _polling)
    try:
        loop.run_until_complete(main())
    finally:
        mzo.close()
        loop._default_executor.shutdown()
        loop.close()
