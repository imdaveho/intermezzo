import time
from intermezzo import Intermezzo as mzo


def tbPrint(x, y, fg, bg, msg):
    for c in msg:
        mzo.set_cell(x, y, c, fg, bg)
        x += 1

def update_and_redraw(s):
    mzo.clear(mzo.color("Default"), mzo.color("Default"))
    tbPrint(0, 0, 0, 0, s)
    mzo.flush()

if __name__ == "__main__":
    mx, my = 0, 0
    err = mzo.init()
    if err:
        raise(Exception(err))
    mzo.set_input_mode(mzo.input("Esc") | mzo.input("Mouse"))
    while True:
        evt = mzo.poll_event()
        if evt["Type"] == mzo.event("Key"):
            if evt["Key"] == mzo.key("Esc"):
                break
        elif evt["Type"] == mzo.event("Mouse"):
            if evt["Key"] == mzo.mouse("Left"):
                mx, my = evt["MouseX"], evt["MouseY"]
        s = f"x: {mx}, y: {my}"
        update_and_redraw(s)
    mzo.close()
