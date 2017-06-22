import time
import asyncio
from intermezzo import Intermezzo as mzo


def tbPrint(x, y, fg, bg, msg):
    for c in msg:
        mzo.set_cell(x, y, c, fg, bg)
        x += 1

def draw(i):
    mzo.clear(mzo.color("Default"), mzo.color("Default"))
    w, h = mzo.size()
    s = "count = {}".format(i)
    tbPrint(int((w/2)-(len(s)/2)), int(h/2), mzo.color("Red"), mzo.color("Default"), s)
    mzo.flush()

is_running = True

def _interrupt():
    global is_running
    time.sleep(5)
    mzo.interrupt()
    # global state is bad but Python waits until
    # the thread finishes running before closing
    # the event loop so without something to skip
    # time.sleep(1) and raise(...), the thread will
    # wait 1 second before exiting the main loop...
    if not is_running:
        time.sleep(1) # <-- will sleep w/o is_running check
        raise(Exception("This should never run."))

async def main():
    err = mzo.init()
    if err:
        raise(Exception(err))
    mzo.set_input_mode(mzo.input("Esc"))
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
            global is_running
            is_running = False
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
