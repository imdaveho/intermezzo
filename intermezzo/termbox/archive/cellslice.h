#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

typedef struct Cell
{
  int32_t  Ch;
  uint32_t Fg;
  uint32_t Bg;
} Cell;

typedef struct CellSlice
{
  Cell**   data;
  int len;
  int cap;
} CellSlice;

CellSlice *CellSlice_create(uint32_t len, uint32_t cap);
CellSlice *CellSlice_insert(CellSlice *slice, Cell *cell, int index);
void CellSlice_destroy(CellSlice *slice);
