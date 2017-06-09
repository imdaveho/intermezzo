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
  Cell* data;
  int   len;
} CellSlice;

CellSlice *CellSlice_create(int len);
void Cells_insert(CellSlice *cells, Cell cell, int index);
void CellSlice_destroy(CellSlice *slice);
