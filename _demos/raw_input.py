import time
import struct
from intermezzo import Intermezzo as mzo

def tbPrint(x, y, fg, bg, msg):
    for c in msg:
        mzo.set_cell(x, y, c, fg, bg)
        x += 1

current = ""
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
                f"EventKey: k: {curev['Key']}, c: {chr(curev['Ch'])}, mod: {mod_str(curev['Mod'])}")
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

    while True:
        data = bytes(64)
        length = len(struct.unpack(f"{len(data)}p", data)[0])

        if 64 - length < 32:
            newdata = bytes(length+32)
            newdata[:len(data)] = data
            data = newdata

        # in Go, this sub-array is call-by-reference
        # therefore, when PollRawEvent updates d, it
        # in turn, also updates data. This isn't the
        # case here; we need to manually update data:
        d = data[length:length+32]
        evt, d = mzo.poll_raw_event(d)
        data = data[:length] + struct.pack(f"{len(d)}B", *d) + data[length+32:]

        if evt["Type"] == mzo.event("Raw"):
            data = data[:length+evt["N"]]
            current = "\"" + f"{data!s}"[2:][:-1] + "\""
            if current == '"q"':
                break

            while True:
                evt, data = mzo.parse_event(data)
                if evt["N"] == 0:
                    break
                curev = evt
                data = data[:len(data)-evt["N"]]

        if evt["Type"] == mzo.event("Error"):
            raise(Exception(evt["Err"]))
        redraw_all()

if __name__ == "__main__":
    try:
        main()
    finally:
        mzo.close()
