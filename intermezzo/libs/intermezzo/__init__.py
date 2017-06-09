from .py_api import lib, ffi

class Intermezzo:
    def init():
        lib.Init()

    def close():
        lib.Close()

    def get_cell_buffer():
        buffer = ffi.new("CellSlice *", lib.CellBuffer()[0])
        return buffer

    def get_cell_buffer_c_addr():
        addr = lib.CellBuffer()[0]
        return addr

    def clear_cell_buffer(cdata):
        ptr = ffi.addressof(cdata)
        lib.freeCells(ptr)

    def get_addr(cdata):
        ptr = ffi.addressof(cdata)
        return ptr
