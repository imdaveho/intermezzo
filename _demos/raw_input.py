import time
from intermezzo import Intermezzo as mzo

def tbPrint(x, y, fg, bg, msg):
    for c in msg:
        mzo.set_cell(x, y, c, fg, bg)
        x += 1

current = b""
curev = {
    "Type":   None,
    "Mod":    None,
    "Key":    None,
    "Ch":     None,
    "Width":  None,
    "Height": None,
    "Err":    "",
    "MouseX": None,
    "MouseY": None,
    "N":      None
}


def mouse_button_str(k):
    if k == mzo.mouse("Left"):
        return "MouseLeft"
    elif k == mzo.mouse("Middle"):
        return "MouseMiddle"
    elif k == mzo.mouse("Right"):
        return "MouseRight"
    elif k == mzo.mouse("Release"):
        return "MouseRelease"
    elif k == mzo.mouse("WheelUp"):
        return "MouseWheelUp"
    elif k == mzo.mouse("WheelDown"):
        return "MouseWheelDown"
    else:
        return "Key"

def mod_str(m):
    out = []
    if m & mzo.mod("Alt") != 0:
        out.append("ModAlt")
    if m & mzo.mod("Motion") != 0:
        out.append("ModMotion")
    return " | ".join(out)

def redraw_all():
    global current, curev
    coldef = mzo.color("Default")
    mzo.clear(coldef, coldef)
    tbPrint(0, 0, mzo.color("Magenta"), coldef, "Press 'q' to quit")
    tbPrint(0, 1, coldef, coldef, current)
    if curev["Type"] == mzo.event("Key"):
        tbPrint(0, 2, coldef, coldef,
                f"EventKey: k: {curev['Key']}, c: {curev['Ch']}, mod: {mod_str(curev['Mod'])}")
    elif curev["Type"] == mzo.event("Mouse"):
        tbPrint(0, 2, coldef, coldef,
                f"EventMouse: x: {curev['MouseX']}, y: {curev['MouseY']}, b: {mouse_button_str(curev['Key'])}, mod: {mod_str(curev['Mod'])}")
    elif curev["Type"] == mzo.event("None"):
        tbPrint(0, 2, coldef, coldef, "EventNone")
    tbPrint(0, 3, coldef, coldef, f"{curev['N']}")
    mzo.flush()

def main():
    global current, curev
    err = mzo.init()
    if err:
        raise(Exception(err))
    mzo.set_input_mode(mzo.input("Alt")|mzo.input("Mouse"))
    redraw_all()
    data = bytes(64)
    while True:
        beg = sum([1 for i in data if i > 0])
        if 64 - beg < 32:
            data = data[beg:]
        d = data[beg:beg+32]
        evt, data = mzo.poll_raw_event(d)
        print(d)
        if evt["Type"] == mzo.event("Raw"):
            data = data[:beg+evt["N"]]
            current = "%s" % data
            print(current)
            if current == 'q':
                break
            while True:
                _evt, data = mzo.parse_event(data)
                if _evt["N"] == 0:
                    break
                curev = _evt
                data = data[curev["N"]:]
                data = data[:len(data) - curev["N"]]
        if evt["Type"] == mzo.event("Error"):
            raise(Exception(evt["Err"]))
        redraw_all()

if __name__ == "__main__":
    try:
        main()
    finally:
        mzo.close()
