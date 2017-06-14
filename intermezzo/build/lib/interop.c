#include "interop.h"

CellSlice *createCells(int len)
{
  CellSlice *ptr = malloc(sizeof(CellSlice));
  if (ptr == NULL) {
    return NULL;
  }
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

Event *createEvent(void)
{
  Event *ptr = malloc(sizeof(Event));
  if (ptr == NULL) {
    return NULL;
  }
  return ptr;
}

void freeCCells(CellSlice *ptr)
{
  Cell *cells = ptr->data;
  free(cells); // free Cell*
  cells = NULL;
  free(ptr);   // free CellSlice*
  ptr = NULL;
}

void freeCString(char *str)
{
  free(str);
  str = NULL;
}

void freeCEvent(Event *ptr)
{
  Error err = ptr->Err;
  free(err);
  err = NULL;
  free(ptr);
  ptr = NULL;
}

// NOTE: cgo may GC structs created in Go;
// this means that we don't have to manually
// free since we didn't use malloc to create
// the C.SizeTuple
// TODO: confirm the above

// void freeCSizeTuple(SizeTuple *ptr)
// {
//   free(ptr);
//   ptr = NULL;
// }
