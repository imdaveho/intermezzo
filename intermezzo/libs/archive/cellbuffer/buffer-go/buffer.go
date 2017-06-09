package main

// #cgo CFLAGS: -IWall -g
// #include "libbuffer.h"
import "C"

type Cell struct {
	Ch int32
	Fg uint32
	Bg uint32
}

//export MakeBuffer
func MakeBuffer() *C.CellSlice {
	// this is actually just the CellBuffer() function
	// in termbox-go, so it's really just allocating
	// the return value from that into the global []Cell
	one := Cell{1, 2, 3}
	two := Cell{4, 5, 6}
	slice := []Cell{one, two}
	cells := C.CellSlice_create(C.int(len(slice)))
	for i, c := range slice {
		cell := C.Cell{
			Ch: C.int32_t(c.Ch),
			Fg: C.uint32_t(c.Fg),
			Bg: C.uint32_t(c.Bg),
		}
		C.Cells_insert(cells, cell, C.int(i))
	}
	return cells
}

//export FreeBuffer
func FreeBuffer(cells *C.CellSlice) {
	C.CellSlice_destroy(cells)
}

func main() {}
