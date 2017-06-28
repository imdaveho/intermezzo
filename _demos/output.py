from intermezzo import Intermezzo as mzo


chars = "nnnnnnnnnbbbbbbbbbuuuuuuuuuBBBBBBBBB"

output_mode = mzo.output("Normal")

def next_char(current):
    current += 1
    if current >= len(chars):
        return 0
    return current

def print_combinations_table(sx, sy, attrs):
    bg = 0
    current_char = 0
    y = sy

    all_attrs = [
        0,
        mzo.attr("Bold"),
        mzo.attr("Underline"),
        mzo.attr("Bold") | mzo.attr("Underline"),
    ]

    def draw_line():
        nonlocal current_char
        x = sx
        for a in all_attrs:
            for c in range(mzo.color("Default"), mzo.color("White") + 1):
                fg = a | c
                mzo.set_cell(x, y, chars[current_char], fg, bg)
                current_char = next_char(current_char)
                x += 1

    for a in attrs:
        for c in range(mzo.color("Default"), mzo.color("White") + 1):
            bg = a | c
            draw_line()
            y += 1

def print_wide(x, y, s):
    red = False
    for r in s:
        c = mzo.color("Default")
        if red:
            c = mzo.color("Red")
        mzo.set_cell(x, y, r, mzo.color("Default"), c)
        w = mzo.rune_width(r)
        # NOTE: if using wcwidth, it does
        # not have a 1:1 equivalent to
        # IsAmbiguousWidth()
        if w == 0 or (w == 2 and mzo.is_ambiguous_width(r)):
            w = 1
        x += w
        red = not red

hello_world = "こんにちは世界"

def draw_all():
    mzo.clear(mzo.color("Default"), mzo.color("Default"))

    if output_mode == mzo.output("Normal"):
        print_combinations_table(1, 1, [0, mzo.attr("Bold")])
        print_combinations_table(2+len(chars), 1, [mzo.attr("Reverse"),])
        print_wide(2+len(chars), 11, hello_world)

    elif output_mode == mzo.output("Grayscale"):
        for y in range(0, 26):
            for x in range(0, 26):
                mzo.set_cell(x, y, 'n', x+1, y+1)
                mzo.set_cell(x+27, y, 'b', (x+1)|mzo.attr("Bold"), 26-y)
                mzo.set_cell(x+54, y, 'u', (x+1)|mzo.attr("Underline"), y+1)
            mzo.set_cell(82, y, 'd', y+1, mzo.color("Default"))
            mzo.set_cell(83, y, 'd', mzo.color("Default"), 26-y)

    elif output_mode == mzo.output("216"):
        for r in range(0, 6):
            for g in range(0, 6):
                for b in range(0, 6):
                    y = r
                    x = g + 6*b
                    c1 = 1 + r*36 + g*6 + b
                    bg = 1 + g*36 + b*6 + r
                    c2 = 1 + b*36 + r*6 + g

                    bc1 = c1 | mzo.attr("Bold")
                    uc1 = c1 | mzo.attr("Underline")
                    bc2 = c2 | mzo.attr("Bold")
                    uc2 = c2 | mzo.attr("Underline")
                    mzo.set_cell(x, y, 'n', c1, bg)
                    mzo.set_cell(x, y+6, 'b', bc1, bg)
                    mzo.set_cell(x, y+12, 'u', uc1, bg)
                    mzo.set_cell(x, y+18, 'B', bc1|uc1, bg)
                    mzo.set_cell(x+37, y, 'n', c2, bg)
                    mzo.set_cell(x+37, y+6, 'b', bc2, bg)
                    mzo.set_cell(x+37, y+12, 'u', uc2, bg)
                    mzo.set_cell(x+37, y+18, 'B', bc2|uc2, bg)
                c1 = 1 + g*6 + r*36
                c2 = 6 + g*6 + r*36
                mzo.set_cell(74+g, r, 'd', c1, mzo.color("Default"))
                mzo.set_cell(74+g, r+6, 'd', c2, mzo.color("Default"))
                mzo.set_cell(74+g, r+12, 'd', mzo.color("Default"), c1)
                mzo.set_cell(74+g, r+18, 'd', mzo.color("Default"), c2)

    elif output_mode == mzo.output("256"):
        for y in range(0, 4):
            for x in range(0, 8):
                for z in range(0, 8):
                    bg = 1 + y*64 + x*8 + z
                    c1 = 256 - y*64 - x*8 - z
                    c2 = 1 + y*64 + z*8 + x
                    c3 = 256 - y*64 - z*8 - x
                    c4 = 1 + y*64 + x*4 + z*4
                    bold = c2 | mzo.attr("Bold")
                    under = c3 | mzo.attr("Underline")
                    both = c1 | mzo.attr("Bold") | mzo.attr("Underline")
                    mzo.set_cell(z+8*x, y, ' ', 0, bg)
                    mzo.set_cell(z+8*x, y+5, 'n', c4, bg)
                    mzo.set_cell(z+8*x, y+10, 'b', bold, bg)
                    mzo.set_cell(z+8*x, y+15, 'u', under, bg)
                    mzo.set_cell(z+8*x, y+20, 'B', both, bg)

        for x in range(0, 12):
            for y in range(0, 2):
                c1 = 233 + y*12 + x
                mzo.set_cell(66+x, y, 'd', c1, mzo.color("Default"))
                mzo.set_cell(66+x, 2+y, 'd', mzo.color("Default"), c1)

        for x in range(0, 6):
            for y in range(0, 6):
                c1 = 17 + x*6 + y*36
                c2 = 17 + 5 + x*6 + y*36
                mzo.set_cell(66+x, 6+y, 'd', c1, mzo.color("Default"))
                mzo.set_cell(66+x, 12+y, 'd', c2, mzo.color("Default"))
                mzo.set_cell(72+x, 6+y, 'd', mzo.color("Default"), c1)
                mzo.set_cell(72+x, 12+y, 'd', mzo.color("Default"), c2)

    mzo.flush()

available_modes = [
    mzo.output("Normal"),
    mzo.output("Grayscale"),
    mzo.output("216"),
    mzo.output("256"),
]

output_mode_index = 0

def switch_output_mode(direction):
    global output_mode
    global output_mode_index
    output_mode_index += direction
    if output_mode_index < 0:
        output_mode_index = len(available_modes) - 1
    elif output_mode_index >= len(available_modes):
        output_mode_index = 0
    output_mode = mzo.set_output_mode(available_modes[output_mode_index])
    mzo.clear(mzo.color("Default"), mzo.color("Default"))
    mzo.sync()

def main():
    err = mzo.init()
    if err:
        raise(Exception(err))
    draw_all()
    while True:
        evt = mzo.poll_event()
        if evt["Type"] == mzo.event("Key"):
            if evt["Key"] == mzo.key("Esc"):
                break
            elif evt["Key"] == mzo.key("ArrowUp") or evt["Key"] == mzo.key("ArrowRight"):
                switch_output_mode(1)
                draw_all()
            elif evt["Key"] == mzo.key("ArrowDowm") or evt["Key"] == mzo.key("ArrowLeft"):
                switch_output_mode(-1)
                draw_all()
        elif evt["Type"] == mzo.event("Resize"):
            draw_all()

if __name__ == "__main__":
    try:
        main()
    finally:
        mzo.close()
