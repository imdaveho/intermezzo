import time
# from termbox import Intermezzo
from libs.intermezzo import Intermezzo

if __name__ == "__main__":
    Intermezzo.init()
    buffer_ffi = Intermezzo.get_cell_buffer()
    # print(Intermezzo.get_addr(buffer_ffi[0]))
    # buffer_ffi_addr = Intermezzo.get_addr(buffer_ffi[0])
    # print(buffer_ffi_addr)
    print(buffer_ffi.data)
    print(buffer_ffi.len)

    buffer_cgo = Intermezzo.get_cell_buffer_c_addr()
    print(buffer_cgo.data)
    print(buffer_cgo.len)
    time.sleep(2)
    Intermezzo.close()

    print(Intermezzo.get_addr(buffer_ffi[0]))
    buffer_ffi_addr = Intermezzo.get_addr(buffer_ffi[0])
    Intermezzo.clear_cell_buffer(buffer_ffi_addr)
    print(buffer_ffi.data)
    print(buffer_ffi.len)

    Intermezzo.clear_cell_buffer(buffer_cgo)
    print(buffer_cgo.data)
    print(buffer_cgo.len)
