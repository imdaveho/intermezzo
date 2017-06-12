from .py_api import lib, ffi

class Intermezzo:
    def cell_buffer(self):
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

    def clear(self, fg, bg):
        error_ptr = lib.Clear(fg, bg)
        err = ffi.string(error_ptr).decode("utf-8")
        # free that char* memory!
        lib.freeString(error_ptr)
        del error_ptr
        return err

    def close(self):
        lib.Close()

    def flush(self):
        error_ptr = lib.Flush()
        err = ffi.string(error_ptr).decode("utf-8")
        # free that char* memory!
        lib.freeString(error_ptr)
        del error_ptr
        return err

    def hide_cursor(self):
        lib.HideCursor()

    def init(self):
        error_ptr = lib.Init()
        err = ffi.string(error_ptr).decode("utf-8")
        # free that char* memory!
        lib.freeString(error_ptr)
        del error_ptr
        return err

    def interrupt(self):
        lib.Interrupt()

    def set_cell(self, x, y, ch, fg, bg):
        lib.SetCell(x, y, ch, fg, bg)

    def set_cursor(self, x, y):
        lib.SetCursor(x, y)

    def size(self):
        size_tuple = lib.Size()
        w, h = size_tuple.width, size_tuple.height
        return w, h

    def sync(self):
        error_ptr = lib.Sync()
        err = ffi.string(error_ptr).decode("utf-8")
        # free that char* memory!
        lib.freeString(error_ptr)
        del error_ptr
        return err

    def poll_event(self):
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

    def set_input_mode(self, mode):
        input_mode = lib.SetInputMode(mode)
        return input_mode

    def set_output_mode(self, mode):
        output_mode = lib.SetOutputMode(mode)
        return output_mode
