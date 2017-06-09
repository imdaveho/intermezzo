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
void freeSize(SizeTuple* p0);
void freeEvent(Event* p0);

CellSlice* CellBuffer();
void Close();
Error Flush();
void HideCursor();
Error Init();
void Interrupt();
void SetCell(int p0, int p1, int32_t p2, uint16_t p3, uint16_t p4);
void SetCursor(int p0, int p1);
SizeTuple Size();
char* Sync();
Event PollEvent();
int SetInputMode(int p0);
int SetOutputMode(int p0);
"""
)

ffibuilder.set_source("py_api",
"""
#include "cgo_api.h"
""",
extra_objects=["cgo_api.so"],
extra_link_args=["-Wl,-rpath=$ORIGIN"]
)

if __name__ == "__main__":
    ffibuilder.compile(tmpdir="..", verbose=True)
