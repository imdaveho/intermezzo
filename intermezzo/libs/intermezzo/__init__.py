from .py_api import lib, ffi

class Intermezzo:
    def cell_buffer(self):
        cellslice = lib.CellBuffer()
        buffer = []
        for i in range(cellslice.len):
            ch = cellslice.data[i].Ch
            fg = cellslice.data[i].Fg
            bg = cellslice.data[i].Bg
            buffer.append({
                "Ch": ch,
                "Fg": fg,
                "Bg": bg,
            })
        # free that CellSlice* memory!
        lib.freeCells(cellslice)
        del cellslice
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
        cevt = lib.PollEvent()
        pyevt = {
            "Type":   cevt.Type,
            "Mod":    cevt.Mod,
            "Key":    cevt.Key,
            "Ch":     cevt.Ch,
            "Width":  cevt.Width,
            "Height": cevt.Height,
            "Err":    ffi.string(cevt.Err),
            "MouseX": cevt.MouseX,
            "MouseY": cevt.MouseY,
            "N":      cevt.N
        }
        # TODO: confirm memory usage and lifecycle
        cevt_ptr = ffi.addressof(cevt)
        lib.freeEvent(cevt_ptr)
        del cevt_ptr
        del cevt
        return pyevt

    def set_input_mode(self, mode):
        input_mode = lib.SetInputMode(mode)
        return input_mode

    def set_output_mode(self, mode):
        output_mode = lib.SetOutputMode(mode)
        return output_mode
