import os
import platform
import intermezzo
from ._ffi import ffi


PKGPATH = os.path.dirname(os.path.abspath(__file__))
OS = platform.system()
ARCH = platform.machine()
lib = None

# TODO: differentiate between 32-bit and 64-bit
if OS == 'Windows':
    if ARCH in ("x86_64", "i386", "i686", "AMD64"):
        lib = ffi.dlopen(os.path.join(PKGPATH, "build", "win32", "libtermbox-intel.dll"))
    elif ARCH in "aarch64"():
        lib = ffi.dlopen(os.path.join(PKGPATH, "build", "win32", "libtermbox-arm.dll"))
    else:
        pass
elif OS == 'Darwin':
    if ARCH in ("x86_64", "i386", "i686", "AMD64"):
        lib = ffi.dlopen(os.path.join(PKGPATH, "build", "macos", "libtermbox-intel.so"))
    else:
        # OSX doesn't support ARM
        pass
elif OS == 'Linux':
    if ARCH in ("x86_64", "i386", "i686", "AMD64"):
        lib = ffi.dlopen(os.path.join(PKGPATH, "build", "linux", "libtermbox-intel.so"))
    elif ARCH in ("aarch64",):
        lib = ffi.dlopen(os.path.join(PKGPATH, "build", "linux", "libtermbox-arm.so"))
    else:
        pass


class Intermezzo:
    # *****************************
    # Termbox-Go API wrapper:     *
    # *****************************
    @staticmethod
    def is_init():
        init = lib.IsInit()
        if init == 0:
            return False
        elif init == 1:
            return True

    @staticmethod
    def cell_buffer():
        cellslice_ptr = lib.CellBuffer()
        buffer = []
        for i in range(cellslice_ptr.len):
            cell = cellslice_ptr.data[i]
            ch = cell.Ch
            fg = cell.Fg
            bg = cell.Bg
            buffer.append({
                "Ch": ch,
                "Fg": fg,
                "Bg": bg,
            })
        # free that CellSlice* memory!
        lib.freeCells(cellslice_ptr)
        del cellslice_ptr
        return buffer

    @staticmethod
    def copy_into_cell_buffer(cells):
        length = len(cells)
        size = ffi.sizeof("Cell")
        # Python CFFI managed memory
        array = ffi.new("Cell[]", length)
        for i, cell in enumerate(cells):
            c_cell = array[i]
            if cell["Ch"]:
                c_cell.Ch = ord(cell["Ch"])
            else:
                # null string ("") is
                # blank space (32) as
                # default Ch for cell
                c_cell.Ch = 32
            c_cell.Fg = cell["Fg"]
            c_cell.Bg = cell["Bg"]
        error_ptr = lib.CopyIntoCellBuffer(array, size, length)
        err = ffi.string(error_ptr).decode("utf-8")
        # free that char* memory!
        lib.freeString(error_ptr)
        del error_ptr
        # array should be GC'd once err is returned
        return err

    @staticmethod
    def clear(fg, bg):
        error_ptr = lib.Clear(fg, bg)
        err = ffi.string(error_ptr).decode("utf-8")
        # free that char* memory!
        lib.freeString(error_ptr)
        del error_ptr
        return err

    @staticmethod
    def close():
        lib.Close()

    @staticmethod
    def flush():
        error_ptr = lib.Flush()
        err = ffi.string(error_ptr).decode("utf-8")
        # free that char* memory!
        lib.freeString(error_ptr)
        del error_ptr
        return err

    @staticmethod
    def hide_cursor():
        lib.HideCursor()

    @staticmethod
    def init():
        error_ptr = lib.Init()
        err = ffi.string(error_ptr).decode("utf-8")
        # free that char* memory!
        lib.freeString(error_ptr)
        del error_ptr
        return err

    @staticmethod
    def interrupt():
        lib.Interrupt()

    @staticmethod
    def set_cell(x, y, ch, fg, bg):
        lib.SetCell(x, y, ord(ch), fg, bg)

    @staticmethod
    def set_cursor(x, y):
        lib.SetCursor(x, y)

    @staticmethod
    def size():
        size_tuple = lib.Size()
        w, h = size_tuple.width, size_tuple.height
        return w, h

    @staticmethod
    def sync():
        error_ptr = lib.Sync()
        err = ffi.string(error_ptr).decode("utf-8")
        # free that char* memory!
        lib.freeString(error_ptr)
        del error_ptr
        return err

    @staticmethod
    def poll_event():
        evt_ptr = lib.PollEvent()
        pyevt = {
            "Type":   evt_ptr.Type,
            "Mod":    evt_ptr.Mod,
            "Key":    evt_ptr.Key,
            "Ch":     evt_ptr.Ch,
            "Width":  evt_ptr.Width,
            "Height": evt_ptr.Height,
            "Err":    ffi.string(evt_ptr.Err).decode("utf-8"),
            "MouseX": evt_ptr.MouseX,
            "MouseY": evt_ptr.MouseY,
            "N":      evt_ptr.N
        }
        # free that Event* (and char*) memory!
        lib.freeEvent(evt_ptr)
        del evt_ptr
        return pyevt

    @staticmethod
    def set_input_mode(mode):
        input_mode = lib.SetInputMode(mode)
        return input_mode

    @staticmethod
    def set_output_mode(mode):
        output_mode = lib.SetOutputMode(mode)
        return output_mode

    @staticmethod
    def parse_event(bytedata):
        length = len(bytedata)
        c_bytes = ffi.new("uint8_t[]", length)
        for i, b in enumerate(bytedata):
            c_bytes[i] = b
        raw_ptr = lib.ParseEvent(c_bytes, length)
        pyevt = {
            "Type":   raw_ptr.ev.Type,
            "Mod":    raw_ptr.ev.Mod,
            "Key":    raw_ptr.ev.Key,
            "Ch":     raw_ptr.ev.Ch,
            "Width":  raw_ptr.ev.Width,
            "Height": raw_ptr.ev.Height,
            "Err":    ffi.string(raw_ptr.ev.Err).decode("utf-8"),
            "MouseX": raw_ptr.ev.MouseX,
            "MouseY": raw_ptr.ev.MouseY,
            "N":      raw_ptr.ev.N
        }
        bytedata = ffi.unpack(raw_ptr.data, length)
        # free that RawEvent* and associated memory!
        lib.freeRawEvent(raw_ptr)
        del raw_ptr
        return pyevt, bytedata

    @staticmethod
    def poll_raw_event(bytedata):
        length = len(bytedata)
        c_bytes = ffi.new("uint8_t[]", length)
        for i, b in enumerate(bytedata):
            c_bytes[i] = b
        raw_ptr = lib.PollRawEvent(c_bytes, length)
        pyevt = {
            "Type":   raw_ptr.ev.Type,
            "Mod":    raw_ptr.ev.Mod,
            "Key":    raw_ptr.ev.Key,
            "Ch":     raw_ptr.ev.Ch,
            "Width":  raw_ptr.ev.Width,
            "Height": raw_ptr.ev.Height,
            "Err":    ffi.string(raw_ptr.ev.Err).decode("utf-8"),
            "MouseX": raw_ptr.ev.MouseX,
            "MouseY": raw_ptr.ev.MouseY,
            "N":      raw_ptr.ev.N
        }
        bytedata = ffi.unpack(raw_ptr.data, length)
        # free that RawEvent* and associated memory!
        lib.freeRawEvent(raw_ptr)
        del raw_ptr
        return pyevt, bytedata

    # *****************************
    # Termbox-Go constants:       *
    # *****************************
    @staticmethod
    def event(name):
        return {
            "Key":       0,
            "Resize":    1,
            "Mouse":     2,
            "Error":     3,
            "Interrupt": 4,
            "Raw":       5,
            "None":      6,
        }.get(name, 5)

    @staticmethod
    def input(mode):
        return {
            "Current": 0,
            "Esc":     1,
            "Alt":     2,
            "Mouse":   4,
        }.get(mode, 0)

    @staticmethod
    def output(mode):
        return {
            "Current":   0,
            "Normal":    1,
            "256":       2,
            "216":       3,
            "Grayscale": 4,
        }.get(mode, 0)

    @staticmethod
    def mod(name):
        return {
            "Alt":    1,
            "Motion": 2,
        }.get(name, 0)

    @staticmethod
    def key(name):
        return {
            "F1":             65535,
            "F2":             65534,
            "F3":             65533,
            "F4":             65532,
            "F5":             65531,
            "F6":             65530,
            "F7":             65529,
            "F8":             65528,
            "F9":             65527,
            "F10":            65526,
            "F11":            65525,
            "F12":            65524,
            "Insert":         65523,
            "Delete":         65522,
            "Home":           65521,
            "End":            65520,
            "Pgup":           65519,
            "Pgdn":           65518,
            "ArrowUp":        65517,
            "ArrowDown":      65516,
            "ArrowLeft":      65515,
            "ArrowRight":     65514,

            "CtrlTilde":      0,
            "Ctrl2":          0,
            "CtrlSpace":      0,
            "CtrlA":          1,
            "CtrlB":          2,
            "CtrlC":          3,
            "CtrlD":          4,
            "CtrlE":          5,
            "CtrlF":          6,
            "CtrlG":          7,
            "Backspace":      8,
            "CtrlH":          8,
            "Tab":            9,
            "CtrlI":          9,
            "CtrlJ":          10,
            "CtrlK":          11,
            "CtrlL":          12,
            "Enter":          13,
            "CtrlM":          13,
            "CtrlN":          14,
            "CtrlO":          15,
            "CtrlP":          16,
            "CtrlQ":          17,
            "CtrlR":          18,
            "CtrlS":          19,
            "CtrlT":          20,
            "CtrlU":          21,
            "CtrlV":          22,
            "CtrlW":          23,
            "CtrlX":          24,
            "CtrlY":          25,
            "CtrlZ":          26,
            "Esc":            27,
            "CtrlLsqBracket": 27,
            "Ctrl3":          27,
            "Ctrl4":          28,
            "CtrlBackslash":  28,
            "Ctrl5":          29,
            "CtrlRsqBracket": 29,
            "Ctrl6":          30,
            "Ctrl7":          31,
            "CtrlSlash":      31,
            "CtrlUnderscore": 31,
            "Space":          32,
            "Backspace2":     127,
            "Ctrl8":          127,
        }.get(name, None)

    @staticmethod
    def mouse(name):
        return {
            "Left":      65512,
            "Middle":    65511,
            "Right":     65510,
            "Release":   65509,
            "WheelUp":   65508,
            "WheelDown": 65507,
        }.get(name, None)

    @staticmethod
    def color(name):
        return {
            "Default": 0,
            "Black":   1,
            "Red":     2,
            "Green":   3,
            "Yellow":  4,
            "Blue":    5,
            "Magenta": 6,
            "Cyan":    7,
            "White":   8,
        }.get(name, 0)

    @staticmethod
    def attr(name):
        return {
            "Bold":      512,
            "Underline": 1024,
            "Reverse":   2048,
        }.get(name, 0)

    # *****************************
    # Runewidth-Go API wrapper:   *
    # *****************************
    @staticmethod
    def rune_width(r):
        return lib.RuneWidth(ord(r))

    @staticmethod
    def is_ambiguous_width(r):
        is_ambiguous = lib.IsAmbiguousWidth(ord(r))
        if is_ambiguous == 0:
            return False
        elif is_ambiguous == 1:
            return True

    @staticmethod
    def fill_left(s, w):
        ffi_str = ffi.new("char[]", s.encode("utf-8"))
        str_ptr = lib.FillLeft(ffi_str, w)
        new_str = ffi.string(str_ptr).decode("utf-8")
        # free that char* memory!
        lib.freeString(str_ptr)
        del str_ptr
        return new_str

    @staticmethod
    def fill_right(s, w):
        ffi_str = ffi.new("char[]", s.encode("utf-8"))
        str_ptr = lib.FillRight(ffi_str, w)
        new_str = ffi.string(str_ptr).decode("utf-8")
        # free that char* memory!
        lib.freeString(str_ptr)
        del str_ptr
        return new_str

    @staticmethod
    def is_east_asian():
        is_east_asian = lib.IsEastAsian()
        if is_east_asian == 0:
            return False
        elif is_east_asian == 1:
            return True

    @staticmethod
    def is_neutral_width(r):
        is_neutral = lib.IsNeutralWidth(ord(r))
        if is_neutral == 0:
            return False
        elif is_neutral == 1:
            return True

    @staticmethod
    def string_width(s):
        ffi_str = ffi.new("char[]", s.encode("utf-8"))
        return lib.StringWidth(ffi_str)

    @staticmethod
    def truncate(s, w, tail):
        ffi_s = ffi.new("char[]", s.encode("utf-8"))
        ffi_tail = ffi.new("char[]", tail.encode("utf-8"))
        str_ptr = lib.Truncate(ffi_s, w, ffi_tail)
        new_str = ffi.string(str_ptr).decode("utf-8")
        # free that char* memory!
        lib.freeString(str_ptr)
        del str_ptr
        return new_str

    @staticmethod
    def wrap(s, w):
        ffi_str = ffi.new("char[]", s.encode("utf-8"))
        str_ptr = lib.Wrap(ffi_str, w)
        new_str = ffi.string(str_ptr).decode("utf-8")
        # free that char* memory!
        lib.freeString(str_ptr)
        del str_ptr
        return new_str
