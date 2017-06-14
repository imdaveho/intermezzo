from .py_api import lib, ffi

class Intermezzo:
    @staticmethod
    def cell_buffer():
        cellslice_ptr = lib.CellBuffer()
        buffer = []
        for i in range(cellslice_ptr.len):
            ch = cellslice_ptr.data[i].Ch
            fg = cellslice_ptr.data[i].Fg
            bg = cellslice_ptr.data[i].Bg
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
        lib.SetCell(x, y, ch, fg, bg)

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
