package main

/*
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
*/
import "C"

type Cell struct {
	Ch int32
	Fg uint32
	Bg uint32
}

var Cells []Cell

//export MakeBuffer
func MakeBuffer() C.int {
	// this is actually just the CellBuffer() function
	// in termbox-go, so it's really just allocating
	// the return value from that into the global []Cell
	one := Cell{1, 2, 3}
	two := Cell{4, 5, 6}
	Cells = []Cell{one, two}
	length := C.int(len(Cells))
	return length
}

//export GetCell
func GetCell(index C.int) C.Cell {
	i := int(index)
	c := &Cells[i]
	cell := C.Cell{
		Ch: C.int32_t(c.Ch),
		Fg: C.uint32_t(c.Fg),
		Bg: C.uint32_t(c.Bg),
	}
	return cell
}

//export ClearCells
func ClearCells() {
	Cells = nil
}

func main() {}
