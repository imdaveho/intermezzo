#include "buffer-go/_buffer.h"

int main() {
  int count = MakeBuffer();
  Cell *cells = malloc(sizeof(Cell) * count);
  if (cells == NULL) {
    return 0;
  }
  int i = 0;
  for (i = 0; i < count; i++) {
    Cell cell = GetCell(i);
    cells[i] = cell;
  }
  printf("Printing cells...\n");
  for (i = 0; i < count; i++) {
    Cell cell = cells[i];
    printf("Cell #%d: {Ch: %d, Fg: %d, Bg: %d}\n", i, (&cell)->Ch, (&cell)->Fg, (&cell)->Bg);
  }
  printf("Now clearing cells malloc'd in C.\n");
  /* for (i = 0; i < count; i++) { */
  /*   free(&cells[i]); */
  /* } */
  free(cells);
  printf("Clearing []Cell in Go. Setting to nil...\n");
  ClearCells();
  return 0;
}
