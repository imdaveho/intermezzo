#include "buffer-go/_buffer.h"

int main() {
  CellSlice *slice = MakeBuffer();
  int len = slice->len;
  Cell *cells = slice->data;
  int i = 0;
  for (i = 0; i < len; i++) {
    Cell *c = &cells[i];
    printf("Cell %d: [Ch: %d, Fg: %d, Bg: %d]\n", i, c->Ch, c->Fg, c->Bg);
  }
  FreeBuffer(slice);
}
