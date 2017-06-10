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
  cells = NULL;
  free(ptr);   // free CellSlice*
  ptr = NULL;
}

void freeCString(char *str)
{
  free(str);
  str = NULL;
}

// NOTE: cgo may GC structs created in Go;
// this means that we don't have to manually
// free since we didn't use malloc to create
// the C.SizeTuple and C.Event except in the
// case of C.Event->Err (which is a char*)
// and cgo specifically says to make sure to
// free the memory allocated for char*

// TODO: confirm the above; or to be sure,
// create the structs in C like CellBuffer
// and return the pointers to each

// void freeCSizeTuple(SizeTuple *ptr)
// {
//   free(ptr);
//   ptr = NULL;
// }

void freeCEvent(Event *ptr)
{
  Error err = ptr->Err;
  free(err);
  err = NULL;
  free(ptr);
  ptr = NULL;
}
