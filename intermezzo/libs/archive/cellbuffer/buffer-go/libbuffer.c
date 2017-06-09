#include "libbuffer.h"

CellSlice *CellSlice_create(int len)
{
  CellSlice *slice = malloc(sizeof(CellSlice));
  Cell *cells = malloc(sizeof(Cell) * len);
  if (cells == NULL) {
    return NULL;
  }
  slice->data = cells;
  slice->len = len;
  return slice;
}

void Cells_insert(CellSlice *cells, Cell cell, int index)
{
  cells->data[index] = cell;
}

void CellSlice_destroy(CellSlice *slice)
{
  Cell *cells = slice->data;
  // Free Cell*
  free(cells);
  // Free CellSlice *
  free(slice);
}
