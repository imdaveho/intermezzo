from .py_api import lib, ffi


class Intermezzo:
    def __init__(self):
        self.hanging = None

    def init(self):
        lib.Init()

    def close(self):
        lib.Close()

    def get_cell_buffer(self):
        # testing
        hanging = lib.CellBuffer()
        self.hanging = hanging
        print(hanging)
        buffer = ffi.new("CellSlice *", hanging[0])
        return buffer

    def get_cell_buffer_c_addr(self):
        addr = lib.CellBuffer()[0]
        return addr

    def clear_cell_buffer(self, cdata):
        ptr = ffi.addressof(cdata)
        lib.freeCells(ptr)

    def get_addr(self, cdata):
        ptr = ffi.addressof(cdata)
        return ptr

    # testing
    def get_hanging(self):
        return self.hanging
