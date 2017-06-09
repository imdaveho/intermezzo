#include "cellslice.h"

CellSlice *CellSlice_create(uint32_t len, uint32_t cap)
{
  CellSlice *slice = malloc(sizeof(CellSlice));
  if (slice == NULL) {
    return NULL;
  }
  slice->len = len;
  slice->cap = cap;
  slice->data = malloc(sizeof(Cell) * len);
  return slice;
}

CellSlice *CellSlice_insert(CellSlice *slice, Cell *cell, int index)
{
  Cell **data = slice->data;
  data[index] = cell;
  return slice;
}

void CellSlice_destroy(CellSlice *slice)
{
  Cell **data = slice->data;
  // Free memory for each Cell*
  int i = 0;
  for (i = 0; i < slice->len; i++) {
    free(data[i]);
  }
  // Free Cell**
  free(data);
  // Free CellSlice*
  free(slice);
}
