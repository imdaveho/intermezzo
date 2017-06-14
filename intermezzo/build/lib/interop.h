#ifndef TERMBOX_GO_INTEROP_H_
#define TERMBOX_GO_INTEROP_H_

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

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

CellSlice *createCells(int len);
void insertCells(CellSlice *ptr, Cell cell, int index);
Event *createEvent(void);
void freeCCells(CellSlice *ptr);
void freeCString(char *str);
void freeCEvent(Event *ptr);
/* void freeCSizeTuple(SizeTuple *ptr); */

#endif
