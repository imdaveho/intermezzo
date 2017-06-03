package main

import "C"
import "github.com/nsf/termbox-go"

//export Init
func Init() {
	if err := termbox.Init(); err != nil {
		panic(err)
	}
}

//export Close
func Close() {
	termbox.Close()
}

func main() {}

// package main

// import (
// 	"fmt"
// 	"github.com/nsf/termbox-go"
// 	"time"
// )

// func tbPrint(x, y int, fg, bg termbox.Attribute, msg string) {
// 	for _, c := range msg {
// 		termbox.SetCell(x, y, c, fg, bg)
// 		x++
// 	}
// }

// func draw(i int) {
// 	termbox.Clear(termbox.ColorDefault, termbox.ColorDefault)
// 	defer termbox.Flush()

// 	w, h := termbox.Size()
// 	s := fmt.Sprintf("count = %d", i)

// 	tbPrint((w/2)-(len(s)/2), h/2, termbox.ColorRed, termbox.ColorDefault, s)
// }

// func mainLoop(count int) {
// 	exit := false
// 	for {
// 		switch ev := termbox.PollEvent(); ev.Type {
// 		case termbox.EventKey:
// 			if ev.Ch == '+' {
// 				count++
// 			} else if ev.Ch == '-' {
// 				count--
// 			}
// 		case termbox.EventError:
// 			panic(ev.Err)
// 		case termbox.EventInterrupt:
// 			exit = true
// 			break
// 		}
// 		if exit {
// 			break
// 		}
// 		draw(count)
// 	}
// }

// func main() {
// 	err := termbox.Init()
// 	if err != nil {
// 		panic(err)
// 	}
// 	termbox.SetInputMode(1)

// 	go func() {
// 		time.Sleep(5 * time.Second)
// 		termbox.Interrupt()

// 		time.Sleep(1 * time.Second)
// 		panic("this should never run")
// 	}()

// 	var count int
// 	draw(count)

// 	mainLoop(count)

// 	termbox.Close()
// 	fmt.Println("Done.")
// }
