from intermezzo import Intermezzo as mzo

curCol = [0]
curRune = [0]
backbuf = []
bbw, bbh = 0, 0

runes = [' ', '░', '▒', '▓', '█']
colors = [
    mzo.color("Black"),
    mzo.color("Red"),
    mzo.color("Green"),
    mzo.color("Yellow"),
    mzo.color("Blue"),
    mzo.color("Magenta"),
    mzo.color("Cyan"),
    mzo.color("White"),
]

def updateAndDrawButtons(current, x, y, mx, my, n, attrf):
    lx, ly = x, y
    for i in range(0, n):
        if lx <= mx and mx <= lx+3 and ly <= my and my <= ly+1:
            current[0] = i

        r, fg, bg = attrf(i)
        mzo.set_cell(lx+0, ly+0, r, fg, bg)
        mzo.set_cell(lx+1, ly+0, r, fg, bg)
        mzo.set_cell(lx+2, ly+0, r, fg, bg)
        mzo.set_cell(lx+3, ly+0, r, fg, bg)
        mzo.set_cell(lx+0, ly+1, r, fg, bg)
        mzo.set_cell(lx+1, ly+1, r, fg, bg)
        mzo.set_cell(lx+2, ly+1, r, fg, bg)
        mzo.set_cell(lx+3, ly+1, r, fg, bg)
        lx += 4

    lx, ly = x, y
    for i in range(0, n):
        if current[0] == i:
            fg = mzo.color("Red") | mzo.attr("Bold")
            bg = mzo.color("Default")
            mzo.set_cell(lx+0, ly+2, '^', fg, bg)
            mzo.set_cell(lx+1, ly+2, '^', fg, bg)
            mzo.set_cell(lx+2, ly+2, '^', fg, bg)
            mzo.set_cell(lx+3, ly+2, '^', fg, bg)
        lx += 4

def update_and_redraw_all(mx, my):
    global runes, curRune
    mzo.clear(mzo.color("Default"), mzo.color("Default"))
    # if mx != -1 and my != -1:
    #     backbuf[bbw*my+mx] = {"Ch": runes[curRune[0]], "Fg": colors[curCol[0]], "Bg": 0}
    # err = mzo.copy_into_cell_buffer(backbuf)
    # if err:
    #     raise(Exception(err))
    _, h = mzo.size()

    def rune_cb(i):
        return runes[i], mzo.color("Default"), mzo.color("Default")

    # def color_cb(i):
    #     return ' ', mzo.color("Default"), colors[i]

    updateAndDrawButtons(curRune, 0, 0, mx, my, len(runes), rune_cb)
    # updateAndDrawButtons(curCol, 0, h-3, mx, my, len(colors), color_cb)
    mzo.flush()

def reallocBackBuffer(w, h):
    global backbuf, bbw, bbh
    bbw, bbh = w, h
    backbuf = [{"Ch": "", "Fg": 0, "Bg": 0} for _ in range(w*h)]

def main():
    err = mzo.init()
    if err:
        raise(Exception(err))
    mzo.set_input_mode(mzo.input("Esc") | mzo.input("Mouse"))
    w, h = mzo.size()
    reallocBackBuffer(w, h)
    update_and_redraw_all(-1, -1)

    while True:
        mx, my = -1, -1
        evt = mzo.poll_event()
        if evt["Type"] == mzo.event("Key"):
            if evt["Key"] == mzo.key("Esc"):
                break
        elif evt["Type"] == mzo.event("Mouse"):
            if evt["Key"] == mzo.mouse("Left"):
                mx, my = evt["MouseX"], evt["MouseY"]
        elif evt["Type"] == mzo.event("Resize"):
            reallocBackBuffer(evt["Width"], evt["Height"])
        update_and_redraw_all(mx, my)

if __name__ == "__main__":
    try:
        main()
    finally:
        mzo.close()
