from intermezzo import Intermezzo as mzo


TABSTOP_LEN = 8
PREFERRED_HORIZONTAL_THRESHOLD = 5
EDITBOX_WIDTH = 30

def tbPrint(x, y, fg, bg, msg):
    for c in msg:
        mzo.set_cell(x, y, c, fg, bg)
        x += len(c)

def fill(x, y, w, h, cell):
    for ly in range(0, h):
        for lx in range(0, w):
            mzo.set_cell(x+lx, y+ly, cell["Ch"], cell["Fg"], cell["Bg"])

def rune_advance_len(r, pos):
    if r == '\t':
        return TABSTOP_LEN - (pos % TABSTOP_LEN)
    return len(r)

# def voffset_coffset(text, boffset):
#     """
#     NOTE: unnecessary; Python string/unicode
#     support is very good and we don't have to
#     jump through all the hoops that Golang has
#     to because Golang represents strings as []byte
#     and that causes issues with unicode characters
#     FYI - if you want unicode byte string, do
#     something like this: '☆'.encode("utf-8")
#     """
#     text = text[:boffset]
#     coffset, voffset = 0, 0
#     while len(text) > 0:
#         rune = text[0]
#         text = text[len(rune):]
#         coffset += 1
#         voffset += rune_advance_len(rune, voffset)
#     return coffset, voffset

def byte_slice_grow():
    # NOTE: unnecessary; this is Python -
    # arrays are dynamically sized already!
    pass

def byte_slice_remove(text, start, end):
    text = text[:start] + text[end:]
    return text

def byte_slice_insert(text, offset, what):
    text = text[:offset] + what + text[offset:]
    return text

class EditBox:
    def __init__(self):
        self.text = ""
        self.line_voffset = 0
        self.cursor_coffset = 0 # cursor offset in unicode code points
        self.cursor_voffset = 0 # visual cursor offset in termbox cells
        super().__init__()
        # NOTE: unnecessary; Python doesn't have the same
        # concerns with bytes, runes, and characters wrt
        # unicode characters as Go does
        # self.cursor_boffset = 0 # cursor offset in bytes

    def draw(self, x, y, w, h):
        self.adjust_voffset(w)
        coldef = mzo.color("Default")
        celldef = {"Ch": ' ', "Fg": 0, "Bg": 0}
        fill(x, y, w, h, celldef)
        t = self.text
        lx = 0
        tabstop = 0
        while True:
            rx = lx - self.line_voffset
            if len(t) == 0:
                break

            if lx == tabstop:
                tabstop += TABSTOP_LEN

            if rx >= w:
                mzo.set_cell(x+w-1, y, '→', coldef, coldef)
                break
            rune = t[0]
            if rune == '\t':
                while lx < tabstop:
                    rx = lx - self.line_voffset
                    if rx >= w:
                        # breaking effectively is
                        # goto next
                        break
                    if rx >= 0:
                        mzo.set_cell(x+rx, y, ' ', coldef, coldef)
                    lx += 1
            else:
                if rx >= 0:
                    mzo.set_cell(x+rx, y, rune, coldef, coldef)
                lx += len(rune)
            # next:
            t = t[len(rune):]

        if self.line_voffset != 0:
            mzo.set_cell(x, y, '←', coldef, coldef)

    def adjust_voffset(self, width):
        ht = PREFERRED_HORIZONTAL_THRESHOLD
        max_h_threshold = int((width-1)/2)
        if ht > max_h_threshold:
            ht = max_h_threshold

        threshold = width - 1
        if self.line_voffset != 0:
            threshold = width - ht

        if (self.cursor_voffset - self.line_voffset) >= threshold:
            self.line_voffset = self.cursor_voffset + (ht - width + 1)

        if self.line_voffset != 0 and (self.cursor_voffset - self.line_voffset) < ht:
            self.line_voffset = self.cursor_voffset - ht
            if self.line_voffset < 0:
                self.line_voffset = 0

    def move_cursor_to(self, coffset):
        # NOTE: adaptation based on voffset_coffset() which normalized
        # special characters and unicode from []byte in Go; not needed
        # in Python since string handling / unicode support is built in
        text = self.text[:coffset]
        voffset = 0
        while len(text) > 0:
            rune = text[0]
            text = text[len(rune):]
            voffset += rune_advance_len(rune, voffset)
        self.cursor_coffset = coffset
        self.cursor_voffset = voffset

    def rune_under_cursor(self):
        return self.text[self.cursor_coffset]

    def rune_before_cursor(self):
        return self.text[self.cursor_coffset - 1]

    def move_cursor_one_rune_backward(self):
        if self.cursor_coffset == 0:
            return
        size = len(self.rune_before_cursor())
        self.move_cursor_to(self.cursor_coffset - size)

    def move_cursor_one_rune_forward(self):
        if self.cursor_coffset == len(self.text):
            return
        size = len(self.rune_under_cursor())
        self.move_cursor_to(self.cursor_coffset + size)

    def move_cursor_to_beginning_of_the_line(self):
        self.move_cursor_to(0)

    def move_cursor_to_the_end_of_the_line(self):
        self.move_cursor_to(len(self.text))

    def delete_rune_backward(self):
        if self.cursor_coffset == 0:
            return
        self.move_cursor_one_rune_backward()
        size = len(self.rune_under_cursor())
        self.text = byte_slice_remove(self.text, self.cursor_coffset, self.cursor_coffset + size)

    def delete_rune_forward(self):
        if self.cursor_coffset == len(self.text):
            return
        size = len(self.rune_under_cursor())
        self.text = byte_slice_remove(self.text, self.cursor_coffset, self.cursor_coffset + size)

    def delete_the_rest_of_line(self):
        self.text = self.text[:self.cursor_coffset]

    def insert_rune(self, rune):
        self.text = byte_slice_insert(self.text, self.cursor_coffset, rune)
        self.move_cursor_one_rune_forward()

    def cursorX(self):
        return self.cursor_voffset - self.line_voffset

edit_box = EditBox()

def redraw_all():
    coldef = mzo.color("Default")
    mzo.clear(coldef, coldef)
    w, h = mzo.size()

    midy = int(h/2)
    midx = int((w - EDITBOX_WIDTH)/2)
    cell = {"Ch": '─', "Fg": 0, "Bg": 0}

    mzo.set_cell(midx-1, midy, '│', coldef, coldef)
    mzo.set_cell(midx+EDITBOX_WIDTH, midy, '│', coldef, coldef)
    mzo.set_cell(midx-1, midy-1, '┌', coldef, coldef)
    mzo.set_cell(midx-1, midy+1, '└', coldef, coldef)
    mzo.set_cell(midx+EDITBOX_WIDTH, midy-1, '┐', coldef, coldef)
    mzo.set_cell(midx+EDITBOX_WIDTH, midy+1, '┘', coldef, coldef)
    fill(midx, midy-1, EDITBOX_WIDTH, 1, cell)
    fill(midx, midy+1, EDITBOX_WIDTH, 1, cell)

    edit_box.draw(midx, midy, EDITBOX_WIDTH, 1)
    mzo.set_cursor(midx+edit_box.cursorX(), midy)

    tbPrint(midx+6, midy+3, coldef, coldef, "Press ESC to quit")
    mzo.flush()

def main():
    err = mzo.init()
    if err:
        raise(Exception(err))
    mzo.set_input_mode(mzo.input("Esc"))
    redraw_all()

    while True:
        evt = mzo.poll_event()
        if evt["Type"] == mzo.event("Key"):
            k, c = evt["Key"], evt["Ch"]
            if k == mzo.key("Esc"):
                break
            elif k == mzo.key("CtrlB") or k == mzo.key("ArrowLeft"):
                edit_box.move_cursor_one_rune_backward()
            elif k == mzo.key("CtrlF") or k == mzo.key("ArrowRight"):
                edit_box.move_cursor_one_rune_forward()
            elif k == mzo.key("Backspace") or k == mzo.key("Backspace2"):
                edit_box.delete_rune_backward()
            elif k == mzo.key("CtrlD") or k == mzo.key("Delete"):
                edit_box.delete_rune_forward()
            elif k == mzo.key("Tab"):
                edit_box.insert_rune('\t')
            elif k == mzo.key("Space"):
                edit_box.insert_rune(' ')
            elif k == mzo.key("CtrlK"):
                edit_box.delete_the_rest_of_line()
            elif k == mzo.key("Home") or k == mzo.key("CtrlA"):
                edit_box.move_cursor_to_beginning_of_the_line()
            elif k == mzo.key("End") or k == mzo.key("CtrlE"):
                edit_box.move_cursor_to_the_end_of_the_line()
            else:
                if c != 0:
                    edit_box.insert_rune(chr(c))

        elif evt["Type"] == mzo.event("Error"):
            # EventError
            raise(Exception(evt["Err"]))
        redraw_all()

if __name__ == "__main__":
    try:
        main()
    finally:
        mzo.close()
