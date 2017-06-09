#include "../_libtermbox.h"

int main() {
  int length = MakeBuffer();
  int i = 0;
  Cell *buffer = malloc(sizeof(Cell) * (size_t)(length));
  for (i = 0; i < length; i++) {
    Cell s = GetCell(i);
    buffer[i] = s;
    printf("Pass %d: [Ch: %d, Fg: %d, Bg: %d]\n", i, (&s)->Ch, (&s)->Fg, (&s)->Bg);
  }

  for (i = 0; i < length; i++) {
    Cell *l = &buffer[i];
    printf("Local C array item %d: [Ch: %d, Fg: %d, Bg: %d]\n", i, l->Ch, l->Fg, l->Bg);
  }
  for (i = 0; i < length; i++) {
    Cell *f = &buffer[i];
    free(f);
  }
  /* free(buffer); */
}


/*                                                     100% C IMPLEMETNATION                     */
/* #include <stdio.h> */
/* #include <stdint.h> */
/* #include <stdlib.h> */
/* #include <string.h> */

/* typedef struct Cell */
/* { */
/*   int32_t  Ch; */
/*   uint32_t Fg; */
/*   uint32_t Bg; */
/* } Cell; */

/* int main() { */
/*  /\* go_cell1 := Cell{1, 1, 1} *\/ */
/*  /\* go_cell2 := Cell{24, 33, 33} *\/ */
/*  /\* go_cells := []*Cell{&go_cell1, &go_cell2} *\/ */
/*  /\* c_array := (**C.Cell)(C.malloc(C.sizeof_Cell * C.size_t(len(go_cells)))) *\/ */
/*   Cell *c_cell1 = malloc(sizeof(Cell)); */
/*   c_cell1->Ch = (int32_t)132; */
/*   c_cell1->Fg = (uint32_t)164; */
/*   c_cell1->Bg = (uint32_t)165; */
/*   Cell *c_cell2 = malloc(sizeof(Cell)); */
/*   c_cell2->Ch = (int32_t)232; */
/*   c_cell2->Fg = (uint32_t)264; */
/*   c_cell2->Bg = (uint32_t)265; */
/*   int len = 2; */
/*   Cell **c_array = malloc(sizeof(Cell) * len); */
/*   c_array[0] = c_cell1; */
/*   c_array[1] = c_cell2; */
/*   int i = 0; */
/*   for (i = 0; i < len; i++) { */
/*     printf("Pass %d: [Ch: %d, Fg: %d, Bg: %d]\n", i, c_array[i]->Ch, c_array[i]->Fg, c_array[i]->Bg); */
/*   } */

/*   for (i = 0; i < len; i++) { */
/*     free(c_array[i]); */
/*   } */
/*   free(c_array); */
/* } */


/* Cell *new_cell(int32_t Ch, uint32_t Fg, uint32_t Bg) */
/* { */
/*   Cell *z; */
/*   if((z = malloc(sizeof *z)) != NULL) { */
/*     z->Ch = Ch; */
/*     z->Fg = Fg; */
/*     z->Bg = Bg; */
/*   } */
/*   return z; */
/* } */

/* int main() { */
/*   CellSlice x = CellBuffer(); */
/*   printf("From C file\n"); */
/*   printf("%p\n", &x); */
/*   printf("%d\n", (&x)->ref); */
/*   printf("%d\n", (&x)->len); */
/*   uint32_t i = 0; */
/*   uint32_t ref = (&x)->ref; */
/*   uint32_t len = (&x)->len; */
/*   Cell *cells = GetCellData(ref); */
/*   Cell local[len]; */
/*   for (i = 0; i < len; i++) { */
/*     Cell *cell = &(cells[i]); */
/*     int32_t ch = cell->Ch; */
/*     uint32_t fg = cell->Fg; */
/*     uint32_t bg = cell->Bg; */
/*     local[i] = *(new_cell(ch, fg, bg)); */
/*   } */
/*   printf("This is the address for locally allocated CellBuffer"); */
/*   printf("%p\n", &local); */
/*   printf("This is the address for referenced CellBuffer (Go)"); */
/*   printf("%p\n", cells); */
/*   return 0; */
/* } */
