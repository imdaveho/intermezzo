import time
# from termbox import Intermezzo
from libs.intermezzo import Intermezzo

if __name__ == "__main__":
    mzo = Intermezzo()
    mzo.init()
    time.sleep(2)
    mzo.close()

    buffer_ffi = mzo.get_cell_buffer()
    print("ffi.new():")
    print(buffer_ffi)
    print(buffer_ffi.data)
    print(buffer_ffi.len)
    print("========================")
    print("interop C:")
    hanging = mzo.get_hanging()
    print(hanging[0])
    print(hanging.data[0])
    print(hanging.len)
    print(hanging)
    print("")

    print("========================")
    print("ffi.new():")
    for i in range(buffer_ffi.len):
        if i < 10:
            print(buffer_ffi.data[i].Ch)
    # mzo.clear_cell_buffer(buffer_ffi[0]) # errors out: free() invalid size

    print("interop C:")
    print("========================")
    for i in range(hanging.len):
        if i < 10:
            print(hanging.data[i].Ch)

    print("")
    print("clearing cgo")
    mzo.clear_cell_buffer(hanging[0])
    print("========================")
    print("ffi.new():")
    for i in range(buffer_ffi.len):
        if i < 10:
            print(buffer_ffi.data[i].Ch)

    print("")
    print("========================")
    print("checking cgo")
    print("should error out")
    print(hanging)
    print(hanging.data)
    print(hanging.len)
    for i in range(hanging.len):
        if i < 10:
            print(hanging.data[i].Ch)



    # # This seems to clean memory!
    # buffer_cgo = mzo.get_cell_buffer_c_addr()
    # print(buffer_cgo)
    # print(buffer_cgo.data)
    # print(buffer_cgo.len)
    # time.sleep(2)
    # mzo.close()

    # for i in range(buffer_cgo.len):
    #     if i < 10:
    #         print(buffer_cgo.data[i].Ch)


    # mzo.clear_cell_buffer(buffer_cgo)
    # for i in range(buffer_cgo.len):
    #     if i < 10:
    #         print(buffer_cgo.data[i].Ch)






    # print(Intermezzo.get_addr(buffer_ffi[0]))
    # buffer_ffi_addr = Intermezzo.get_addr(buffer_ffi[0])
    # Intermezzo.clear_cell_buffer(buffer_ffi_addr)
    # print(buffer_ffi.data)
    # print(buffer_ffi.len)

    # Intermezzo.clear_cell_buffer(buffer_cgo)
    # print(buffer_cgo.data)
    # print(buffer_cgo.len)
