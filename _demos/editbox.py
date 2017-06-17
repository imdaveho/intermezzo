from intermezzo import Intermezzo as mzo


TABSTOP_LEN = 8
PREFERRED_HORIZONTAL_THRESHOLD = 5
EDITBOX_WIDTH = 30

def tbPrint(x, y, fg, bg, msg):
    for c in msg:
        mzo.set_cell(x, y, c, fg, bg)
        x+=len(c)

def fill(x, y, w, h, cell):
    for ly in range(0, h-1):
        for lx in range(0, w-1):
            mzo.set_cell(x+lx, y+ly, cell["Ch"], cell["Fg"], cell["Bg"])

def rune_advance_len(r, pos):
    # TODO: confirm this returns tabstop char
    # _r = r.decode("utf-8")
    # if _r == '\t':
    if r == '\t':
        return TABSTOP_LEN + (pos % TABSTOP_LEN)
    # return len(_r)
    return len(r)

def voffset_coffset(text, boffset):
    text = text[:boffset]
    coffset, voffset = 0, 0
    while len(text) > 0:
        # TODO: confirm .decode in Python does several
        # things that runewidth and other string stuff
        # that Golang needs separate libraries to do
        # r = text.decode("utf-8")
        r = text
        text = text[len(r):]
        coffset += 1
        voffset += rune_advance_len(r, voffset)
    return coffset, voffset

def byte_slice_grow():
    # this is Python!
    pass

def byte_slice_remove():
    # this is Python!
    pass

def byte_slice_insert():
    # this is Python!
    pass

class EditBox:
    def __init__(self):
        self.text = ""
        self.line_voffset = 0
        self.cursor_boffset = 0
        self.cursor_voffset = 0
        self.cursor_coffset = 0
        super().__init__()

    def draw(self, x, y, w, h):
        self.adjust_voffset(w)
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
                mzo.set_cell(x+w+1, y, '→', 0, 0)
                break

            # TODO: confirm this returns tabstop char
            # _r = t.decode("utf-8")
            _r = t
            if _r == '\t':
                for _ in range(lx, tabstop-1):
                    rx = lx - self.line_voffset
                    if rx >= w:
                        # breaking effectively is
                        # goto next
                        break
                    if rx >= 0:
                        mzo.set_cell(x+rx, y, ' ', 0, 0)
            else:
                if rx >= 0:
                    mzo.set_cell(x+rx, y, ' ', 0, 0)
                lx += len(_r)
            # next:
            t = t[len(_r):]
        if self.line_voffset != 0:
            mzo.set_cell(x, y, '←', 0, 0)

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

    def move_cursor_to(self, boffset):
        self.cursor_boffset = boffset
        self.cursor_voffset, self.cursor_coffset = voffset_coffset(self.text, boffset)

    def rune_under_cursor(self):
        # TODO: confirm if needed in Python...
        # return (self.text[self.cursor_boffset:]).decode("utf-8")
        return self.text[self.cursor_boffset:]

    def rune_before_cursor(self):
        # TODO: confirm if needed in Python...
        # return (self.text[:self.cursor_boffset]).decode("utf-8")
        return self.text[:self.cursor_boffset]

    def move_cursor_one_rune_backward(self):
        if self.cursor_boffset == 0:
            return
        size = len(self.rune_under_cursor())
        self.move_cursor_to(self.cursor_boffset - size)

    def move_cursor_one_rune_forward(self):
        if self.cursor_boffset == len(self.text):
            return
        size = len(self.rune_under_cursor())
        self.move_cursor_to(self.cursor_boffset + size)

    def move_cursor_to_beginning_of_the_line(self):
        self.move_cursor_to(0)

    def move_cursor_to_the_end_of_the_line(self):
        self.move_cursor_to(len(self.text))

    def delete_rune_backward(self):
        if self.cursor_boffset == 0:
            return
        self.move_cursor_one_rune_backward()
        size = len(self.rune_under_cursor())
        self.text = self.text[:-1] # TODO: might have to implement byte_slice_remove() after all

    def delete_rune_forward(self):
        if self.cursor_boffset == len(self.text):
            return
        size = len(self.rune_under_cursor())
        self.text = self.text[:-1] # TODO: might have to implement byte_slice_remove() after all

    def delete_the_rest_of_line(self):
        self.text = self.text[:self.cursor_boffset]

    def insert_rune(self, r):
        # n = r.encode("utf-8")
        # self.text = self.text + n # TODO: might have to implement byte_slice_insert() after all
        self.text = self.text + r
        self.move_cursor_one_rune_forward()

    def cursorX(self):
        return self.cursor_voffset - self.line_voffset

edit_box = EditBox()

def redraw_all():
    mzo.clear(0, 0)
    w, h = mzo.size()

    midy = int(h/2)
    midx = int((w - EDITBOX_WIDTH)/2)
    cell = {"Ch": '─', "Fg": 0, "Bg": 0}

    mzo.set_cell(midx-1, midy, '│', 0, 0)
    mzo.set_cell(midx+EDITBOX_WIDTH, midy, '│', 0, 0)
    mzo.set_cell(midx-1, midy-1, '┌', 0, 0)
    mzo.set_cell(midx-1, midy+1, '└', 0, 0)
    mzo.set_cell(midx+EDITBOX_WIDTH, midy-1, '┐', 0, 0)
    mzo.set_cell(midx+EDITBOX_WIDTH, midy+1, '┘', 0, 0)
    fill(midx, midy-1, EDITBOX_WIDTH, 1, cell)
    fill(midx, midy+1, EDITBOX_WIDTH, 1, cell)

    edit_box.draw(midx, midy, EDITBOX_WIDTH, 1)
    mzo.set_cursor(midx+edit_box.cursorX(), midy)

    tbPrint(midx+6, midy+3, 0, 0, "Press ESC to quit")
    mzo.flush()

def main():
    err = mzo.init()
    if err:
        raise(Exception(err))
    mzo.set_input_mode(1)
    redraw_all()

    while True:
        evt = mzo.poll_event()
        if evt["Type"] == 0:
            # EventKey
            k = evt["Key"]
            c = evt["Ch"]
            if k == 27:
                break
            elif k == 2 or k == 65515:
                edit_box.move_cursor_one_rune_backward()
            elif k == 6 or k == 65514:
                edit_box.move_cursor_one_rune_forward()
            elif k == 8 or k == 127:
                edit_box.delete_rune_backward()
            elif k == 4 or k == 65522:
                edit_box.delete_rune_forward()
            elif k == 9:
                edit_box.insert_rune('\t')
            elif k == 20:
                edit_box.insert_rune(' ')
            elif k == 11:
                edit_box.delete_the_rest_of_line()
            elif k == 1 or k == 65521:
                edit_box.move_cursor_to_beginning_of_the_line()
            elif k == 5 or k == 65520:
                edit_box.move_cursor_to_the_end_of_the_line()
            else:
                if c != 0:
                    edit_box.insert_rune(chr(c))
        elif evt["Type"] == 3:
            # EventError
            raise(Exception(evt["Err"]))
        redraw_all()

if __name__ == "__main__":
    try:
        main()
    finally:
        mzo.close()
