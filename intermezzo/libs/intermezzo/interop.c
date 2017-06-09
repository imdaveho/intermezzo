#include "interop.h"

CellSlice *createCells(int len)
{
  CellSlice *ptr = malloc(sizeof(CellSlice));
  Cell *cells = malloc(sizeof(Cell) * len);
  if (cells == NULL) {
    return NULL;
  }
  ptr->data = cells;
  ptr->len = len;
  return ptr;
}

void insertCells(CellSlice *ptr, Cell cell, int index)
{
  ptr->data[index] = cell;
}

void freeCCells(CellSlice *ptr)
{
  Cell *cells = ptr->data;
  free(cells); // free Cell*
  free(ptr);   // free CellSlice*
}

void freeCString(char *str)
{
  free(str);
}

void freeCSizeTuple(SizeTuple *ptr)
{
  free(ptr);
}

void freeCEvent(Event *ptr)
{
  Error err = ptr->Err;
  free(err);
  free(ptr);
}
