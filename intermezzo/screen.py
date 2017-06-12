import time
import asyncio
from libs.intermezzo import Intermezzo

mzo = Intermezzo()

def tbPrint(x, y, fg, bg, msg):
    for c in msg:
        mzo.set_cell(int(x), int(y), ord(c), fg, bg)
        x+=1

def draw(i):
    mzo.clear(0, 0)
    w, h = mzo.size()
    s = "count = {}".format(i)
    tbPrint((w/2)-(len(s)/2), h/2, 2, 0, s)
    mzo.flush()

async def countdown():
    await asyncio.sleep(5)
    mzo.interrupt()

    await asyncio.sleep(1)
    raise(Exception("This shouldn't run."))

if __name__ == "__main__":
    err = mzo.init()
    if err:
        raise(Exception(err))
    mzo.set_input_mode(1)
    # loop = asyncio.get_event_loop()
    count = 0
    draw(count)
    # loop.run_until_complete(countdown())
    while True:
        evt = mzo.poll_event()
        if evt["Type"] == 0:
            if chr(evt["Ch"]) == '+':
                count += 1
            elif chr(evt["Ch"]) == '-':
                count -= 1
            elif chr(evt["Ch"]) == 'q':
                break
        elif evt["Type"] == 3:
            raise(Exception(evt["Err"]))
        elif evt["Type"] == 4:
            break
        draw(count)
    mzo.close()
    # loop.close()

    # ============================== [ Test Begin ]
    # count = 0
    # while True:
    #     evt = mzo.poll_event()
    #     count += 1
    #     if count > 5:
    #         break
    # time.sleep(1)
    # mzo.close()
    # ============================== [ Test Ends  ]
    print("Done.")

# if __name__ == "__main__":
#     mzo = Intermezzo()
#     mzo.init()
#     time.sleep(1)
#     mzo.close()

#     buffer = mzo.cell_buffer()
#     print("(python) buffer lenght: {}".format(len(buffer)))

#     error = mzo.clear(1, 1)
#     error = mzo.flush()
#     w, h = mzo.size()
#     print(w)
#     print(h)

#     evt = mzo.poll_event()
