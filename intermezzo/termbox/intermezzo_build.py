import os
from cffi import FFI

ffi = FFI()

ffi.cdef("""
    void _Init();
    void _Close();
""")

ffi.set_source("_intermezzo",
"""
    #include "termbox.h"

    void _Init() { Init(); }
    void _Close() { Close(); }
""",
extra_objects=["termbox.so"],
extra_link_args=["-Wl,-rpath=$ORIGIN"])

if __name__ == "__main__":
    ffi.compile(verbose=True)
