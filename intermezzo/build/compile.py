import os
import platform
from cffi import FFI

ffibuilder = FFI()

ffibuilder.cdef(
"""
typedef struct Cell
{
  int32_t  Ch;
  uint16_t Fg;
  uint16_t Bg;
} Cell;

typedef struct CellSlice
{
  Cell* data;
  int   len;
} CellSlice;

typedef struct SizeTuple
{
  int width;
  int height;
} SizeTuple;

typedef char* Error;

typedef struct Event
{
  uint8_t  Type;
  uint8_t  Mod;
  uint16_t Key;
  int32_t  Ch;
  int      Width;
  int      Height;
  Error    Err;
  int      MouseX;
  int      MouseY;
  int      N;
} Event;

void freeCells(CellSlice* p0);
void freeString(char* p0);
void freeEvent(Event* p0);

CellSlice*  CellBuffer();
Error       Clear(uint16_t p0, uint16_t p1);
void        Close();
Error       Flush();
void        HideCursor();
Error       Init();
void        Interrupt();
void        SetCell(int p0, int p1, int32_t p2, uint16_t p3, uint16_t p4);
void        SetCursor(int p0, int p1);
SizeTuple   Size();
Error       Sync();
Event*      PollEvent();
int         SetInputMode(int p0);
int         SetOutputMode(int p0);
"""
)

if platform.processor() == 'x86_64':
    if platform.system() == "Windows":
        # TODO: add build process for Windows libs
        pass
    elif platform.system() == "Darwin":
        # TODO: add build process of Mac OS libs
        pass
    elif platform.system() == "Linux":
        path = os.path.dirname(os.path.abspath(__file__))
        ffibuilder.set_source("_intermezzo", '#include "{}"'
                              .format(os.path.join(path, "pkg", "intel", "linux_api.h")),
            extra_objects=[os.path.join(path, "pkg", "intel", "linux_api.so")],
            extra_link_args=["-L$ORIGIN/pkg/intel -llinux_api -Wl,-rpath=$ORIGIN/pkg/intel"],
            extra_compile_args=["-I{}".format(os.path.join(path, "pkg", "intel"))]
        )
else:
    # TODO: add support for ARM libs
    pass

if __name__ == "__main__":
    ffibuilder.compile(tmpdir="..", verbose=True)
