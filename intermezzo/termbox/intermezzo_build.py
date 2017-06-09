import os
from cffi import FFI

ffi = FFI()

ffi.cdef("""
typedef int32_t  rune;
typedef uint32_t Attribute;

typedef struct Cell
{
    rune      Ch;
    Attribute Fg;
    Attribute Bg;
} Cell;

typedef struct Cell_GoSlice
{
    Cell*    data;
    uint32_t len;
    uint32_t cap;
} Cell_GoSlice;

Cell_GoSlice _CellBuffer();
""")

ffi.set_source("_slice",
"""
    #include <stdlib.h>
    #include <stdint.h>
    #include "_libtermbox.h"

    Cell_GoSlice _CellBuffer() {
        Cell_GoSlice slice = CellBuffer();
        return slice;
    }
""",
extra_objects=["_libtermbox.so"],
extra_link_args=["-Wl,-rpath=$ORIGIN"])

if __name__ == "__main__":
    ffi.compile(verbose=True)

# import os
# from cffi import FFI

# ffi = FFI()

# ffi.cdef("""
#     void _Init();
#     void _Close();
# """)

# ffi.set_source("_intermezzo",
# """
#     #include "termbox.h"

#     void _Init() { Init(); }
#     void _Close() { Close(); }
# """,
# extra_objects=["termbox.so"],
# extra_link_args=["-Wl,-rpath=$ORIGIN"])

# if __name__ == "__main__":
#     ffi.compile(verbose=True)
