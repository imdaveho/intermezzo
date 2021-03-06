import os
import platform
from cffi import FFI

ffi = FFI()

ffi.cdef(
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

typedef struct RawEvent
{
  Event*    ev;
  uint8_t*  data;
} RawEvent;

void freeCells(CellSlice* p0);
void freeString(char* p0);
void freeEvent(Event* p0);
void freeRawEvent(RawEvent* p0);

int         IsInit();
CellSlice*  CellBuffer();
Error       CopyIntoCellBuffer(Cell* p0, int p1, int p2);
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
RawEvent*   ParseEvent(void* p0, int p1);
RawEvent*   PollRawEvent(void* p0, int p1);

char*       FillLeft(char* p0, int p1);
char*       FillRight(char* p0, int p1);
int         IsAmbiguousWidth(uint32_t p0);
int         IsEastAsian();
int         IsNeutralWidth(uint32_t p0);
int         RuneWidth(uint32_t p0);
int         StringWidth(char* p0);
char*       Truncate(char* p0, int p1, char* p2);
char*       Wrap(char* p0, int p1);
"""
)

ffi.set_source("intermezzo._ffi", None)

if __name__ == "__main__":
    ffi.compile()
