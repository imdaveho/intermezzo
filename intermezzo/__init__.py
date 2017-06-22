import os
import platform
import intermezzo
from ._ffi import ffi


PKGPATH = os.path.dirname(os.path.abspath(__file__))
OS = platform.system()
ARCH = platform.processor()
lib = None

if OS == 'Windows':
    # TODO: add support for Win32
    pass
elif OS == 'Darwin':
    if ARCH == "x86_64" or ARCH == "i386":
        lib = ffi.dlopen(os.path.join(PKGPATH, "build", "macos", "libtermbox-intel.so"))
    pass
elif OS == 'Linux':
    if ARCH == "x86_64" or ARCH == "i386":
        lib = ffi.dlopen(os.path.join(PKGPATH, "build", "linux", "libtermbox-intel.so"))
    else:
        # TODO: add support for ARM and others
        pass


class Intermezzo:
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
        event_ptr = lib.PollEvent()
        pyevt = {
            "Type":   event_ptr.Type,
            "Mod":    event_ptr.Mod,
            "Key":    event_ptr.Key,
            "Ch":     event_ptr.Ch,
            "Width":  event_ptr.Width,
            "Height": event_ptr.Height,
            "Err":    ffi.string(event_ptr.Err).decode("utf-8"),
            "MouseX": event_ptr.MouseX,
            "MouseY": event_ptr.MouseY,
            "N":      event_ptr.N
        }
        # free that Event* (and char*) memory!
        lib.freeEvent(event_ptr)
        del event_ptr
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
