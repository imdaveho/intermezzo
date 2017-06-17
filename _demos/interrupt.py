import time
import asyncio
from intermezzo import Intermezzo as mzo


def tbPrint(x, y, fg, bg, msg):
    for c in msg:
        mzo.set_cell(x, y, c, fg, bg)
        x+=1

def draw(i):
    mzo.clear(0, 0)
    w, h = mzo.size()
    s = "count = {}".format(i)
    tbPrint(int((w/2)-(len(s)/2)), int(h/2), 2, 0, s)
    mzo.flush()

def _interrupt():
    time.sleep(5)
    mzo.interrupt()
    time.sleep(1) # <-- this shouldn't run either, but it does...TODO: fix?
    raise(Exception("This should never run."))

async def main():
    err = mzo.init()
    if err:
        raise(Exception(err))
    mzo.set_input_mode(1)
    count = 0
    draw(count)
    while True:
        evt = mzo.poll_event()
        if evt["Type"] == 0:
            if chr(evt["Ch"]) == '+':
                count += 1
            elif chr(evt["Ch"]) == '-':
                count -= 1
        elif evt["Type"] == 3:
            raise(Exception(evt["Err"]))
        elif evt["Type"] == 4:
            break
        draw(count)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, _interrupt)
    try:
        loop.run_until_complete(main())
    finally:
        mzo.close()
        print("Finished")
        loop._default_executor.shutdown()
        loop.close()
