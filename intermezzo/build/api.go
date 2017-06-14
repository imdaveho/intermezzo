package main

//#cgo CFLAGS: -Wall -g -I${SRCDIR}/lib
//#cgo LDFLAGS: -L${SRCDIR}/lib -linterop -Wl,-rpath=${SRCDIR}/lib
//#include "interop.h"
import "C"
import (
	"github.com/nsf/termbox-go"
)

/****************************************************
* These are free() calls to ensure that malloc'd    *
* memory is appropriately released after use. It    *
* is wrapped here in order to pass along to Py.CFFI *
****************************************************/
//export freeCells
func freeCells(ptr *C.CellSlice) {
	C.freeCCells(ptr)
}

//export freeString
func freeString(str *C.char) {
	C.freeCString(str)
}

//export freeEvent
func freeEvent(ptr *C.Event) {
	C.freeCEvent(ptr)
}

// NOTE: cgo may GC structs created in Go;
// this means that we don't have to manually
// free since we didn't use malloc to create
// the C.SizeTuple
// TODO: confirm the above

// //export freeSize
// func freeSize(ptr *C.SizeTuple) {
// 	C.freeCSizeTuple(ptr)
// }

/****************************************************
* Termbox-Go API Wrappers                           *
****************************************************/
//export CellBuffer
func CellBuffer() *C.CellSlice {
	buffer := termbox.CellBuffer()
	cells := C.createCells(C.int(len(buffer)))
	for i, c := range buffer {
		cell := C.Cell{
			Ch: C.int32_t(c.Ch),
			Fg: C.uint16_t(c.Fg),
			Bg: C.uint16_t(c.Bg),
		}
		C.insertCells(cells, cell, C.int(i))
	}
	return cells
	// for freeing memory, freeCells() would be called
	// from a Python CFFI interface wrapping this func
}

//export Clear
func Clear(fg, bg C.uint16_t) C.Error {
	_fg := termbox.Attribute(fg)
	_bg := termbox.Attribute(bg)
	err := termbox.Clear(_fg, _bg)
	if err != nil {
		return C.CString(err.Error())
	} else {
		return C.CString("")
	}
	// remember to free the CString!
}

//export Close
func Close() {
	termbox.Close()
}

//export Flush
func Flush() C.Error {
	err := termbox.Flush()
	if err != nil {
		return C.CString(err.Error())
	} else {
		return C.CString("")
	}
	// remember to free the CString!
}

//export HideCursor
func HideCursor() {
	termbox.HideCursor()
}

//export Init
func Init() C.Error {
	err := termbox.Init()
	if err != nil {
		return C.CString(err.Error())
	} else {
		return C.CString("")
	}
	// remember to free the CString!
}

//export Interrupt
func Interrupt() {
	termbox.Interrupt()
}

//export SetCell
func SetCell(x, y C.int, ch C.int32_t, fg, bg C.uint16_t) {
	_x := int(x)
	_y := int(y)
	_ch := rune(ch)
	_fg := termbox.Attribute(fg)
	_bg := termbox.Attribute(bg)
	termbox.SetCell(_x, _y, _ch, _fg, _bg)
}

//export SetCursor
func SetCursor(x, y C.int) {
	_x := int(x)
	_y := int(y)
	termbox.SetCursor(_x, _y)
}

//export Size
func Size() C.SizeTuple {
	w, h := termbox.Size()
	size := C.SizeTuple{
		width:  C.int(w),
		height: C.int(h),
	}
	return size
}

//export Sync
func Sync() C.Error {
	err := termbox.Sync()
	if err != nil {
		return C.CString(err.Error())
	} else {
		return C.CString("")
	}
	// remember to free the CString!
}

//export PollEvent
func PollEvent() *C.Event {
	evt := termbox.PollEvent()
	evt_ptr := C.createEvent()
	evt_ptr.Type = C.uint8_t(evt.Type)
	evt_ptr.Mod = C.uint8_t(evt.Mod)
	evt_ptr.Key = C.uint16_t(evt.Key)
	evt_ptr.Ch = C.int32_t(evt.Ch)
	evt_ptr.Width = C.int(evt.Width)
	evt_ptr.Height = C.int(evt.Height)
	if evt.Err != nil {
		evt_ptr.Err = C.CString(evt.Err.Error())
	} else {
		evt_ptr.Err = C.CString("")
	}
	evt_ptr.MouseX = C.int(evt.MouseX)
	evt_ptr.MouseY = C.int(evt.MouseY)
	evt_ptr.N = C.int(evt.N)

	return evt_ptr
}

//export SetInputMode
func SetInputMode(mode C.int) C.int {
	inputMode := termbox.SetInputMode(termbox.InputMode(mode))
	return C.int(inputMode)
}

//export SetOutputMode
func SetOutputMode(mode C.int) C.int {
	outputMode := termbox.SetOutputMode(termbox.OutputMode(mode))
	return C.int(outputMode)
}

// From godoc.org/github.com/nsf/termbox-go:
// NOTE: This API is experimental and may change in the future
// NOTE: Not Implemented
// func ParseEvent(data unsafe.Pointer) Event {
// 	evt := termbox.ParseEvent(...)
//      ???
// }

// From godoc.org/github.com/nsf/termbox-go:
// NOTE: This API is experimental and may change in the future
// NOTE: Not Implemented
// func PollRawEvent(data unsafe.Pointer) Event {
// 	evt := termbox.PollRawEvent(...)
//      ???
// }

func main() {}
