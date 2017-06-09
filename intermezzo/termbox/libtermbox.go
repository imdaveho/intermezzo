package main

// =================================================================== [ No Valgrind Errors ]
import "fmt"

type Cell struct {
	Ch int32
	Fg uint32
	Bg uint32
}

func main() {
	cell1 := Cell{1, 2, 3}
	cell2 := Cell{4, 5, 6}
	cells := []Cell{cell1, cell2}
	for i, c := range cells {
		fmt.Printf("Go loop %d: [Ch: %d, Fg: %d, Bg: %d]\n", i, c.Ch, c.Fg, c.Bg)
	}
}
