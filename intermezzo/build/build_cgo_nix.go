package main

//#cgo CFLAGS: -Wall -g
/*
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

typedef struct Cell
{
  int32_t  Ch;
  uint16_t Fg;
  uint16_t Bg;
} Cell;

typedef struct CellSlice
{
  Cell* data;
  int   len;
} CellSlice;

typedef struct SizeTuple
{
  int width;
  int height;
} SizeTuple;

typedef char* Error;

typedef struct Event
{
  uint8_t  Type;
  uint8_t  Mod;
  uint16_t Key;
  int32_t  Ch;
  int      Width;
  int      Height;
  Error    Err;
  int      MouseX;
  int      MouseY;
  int      N;
} Event;

typedef struct RawEvent
{
  Event*    ev;
  uint8_t*  data;
} RawEvent;

static CellSlice *createCells(int len)
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

static void insertCells(CellSlice *ptr, Cell cell, int index)
{
  ptr->data[index] = cell;
}

static Event *createEvent(void)
{
  Event *ptr = malloc(sizeof(Event));
  if (ptr == NULL) {
    return NULL;
  }
  return ptr;
}

static RawEvent *createRawEvent(void)
{
  RawEvent *ptr = malloc(sizeof(RawEvent));
  if (ptr == NULL) {
    return NULL;
  }
  Event *ev = createEvent();
  ptr->ev = ev;
  // NOTE: uint8_t *data is malloc'd with C.CBytes
  return ptr;
}

static void freeCCells(CellSlice *ptr)
{
  Cell *cells = ptr->data;
  free(cells); // free Cell*
  cells = NULL;
  free(ptr);   // free CellSlice*
  ptr = NULL;
}

static void freeCString(char *str)
{
  free(str);
  str = NULL;
}

static void freeCEvent(Event *ptr)
{
  Error err = ptr->Err;
  free(err);
  err = NULL;
  free(ptr);
  ptr = NULL;
}

static void freeCRawEvent(RawEvent *ptr)
{
  Event *ev = ptr->ev;
  uint8_t *data = ptr->data;
  freeCEvent(ev);
  free(data);
  data = NULL;
  free(ptr);
  ptr = NULL;
}

*/
import "C"
import (
	"bytes"
	"encoding/binary"
	"github.com/mattn/go-runewidth"
	"github.com/nsf/termbox-go"
	"unsafe"
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

//export freeRawEvent
func freeRawEvent(ptr *C.RawEvent) {
	C.freeCRawEvent(ptr)
}

/****************************************************
* Termbox-Go API Wrappers                           *
****************************************************/
//export IsInit
func IsInit() C.int {
	if termbox.IsInit {
		return C.int(1)
	} else {
		return C.int(0)
	}
}

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

//export CopyIntoCellBuffer
func CopyIntoCellBuffer(cells *C.Cell, size C.int, length C.int) C.Error {
	array := C.GoBytes(unsafe.Pointer(cells), length*size)
	buffer := bytes.NewBuffer(array)
	var newcells []termbox.Cell
	for i := 0; i < int(length); i++ {
		var cell termbox.Cell
		err := binary.Read(buffer, binary.LittleEndian, &cell)
		if err != nil {
			return C.CString(err.Error())
		}
		newcells = append(newcells, cell)
	}
	copy(termbox.CellBuffer(), newcells)
	return C.CString("")
	// remember to free the CString!
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
//export ParseEvent
func ParseEvent(data unsafe.Pointer, length C.int) *C.RawEvent {
	b := C.GoBytes(data, length)
	evt := termbox.ParseEvent(b)
	// create the Event*
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
	// revert GoBytes back and cast to uint8_t*
	// www.lobaro.com/embedded-development-with-c-and-golang-cgo
	data_ptr := (*C.uint8_t)(C.CBytes(b))
	// create RawEvent*
	raw_ptr := C.createRawEvent()
	raw_ptr.ev = evt_ptr
	raw_ptr.data = data_ptr

	return raw_ptr
}

// From godoc.org/github.com/nsf/termbox-go:
// NOTE: This API is experimental and may change in the future
//export PollRawEvent
func PollRawEvent(data unsafe.Pointer, length C.int) *C.RawEvent {
	b := C.GoBytes(data, length)
	evt := termbox.PollRawEvent(b)
	// create the Event*
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
	// revert GoBytes back and cast to uint8_t*
	// www.lobaro.com/embedded-development-with-c-and-golang-cgo
	data_ptr := (*C.uint8_t)(C.CBytes(b))
	// create RawEvent*
	raw_ptr := C.createRawEvent()
	raw_ptr.ev = evt_ptr
	raw_ptr.data = data_ptr

	return raw_ptr
}

/****************************************************
* Go-Runewidth API Wrappers                         *
* NOTE: As a dependency for Termbox-Go, including   *
* runewidth attempts to keep the library as stand-  *
* alone as possible while still maintaining a small *
* and simple footprint                              *
****************************************************/
//export FillLeft
func FillLeft(s *C.char, w C.int) *C.char {
	go_str := runewidth.FillLeft(C.GoString(s), int(w))
	return C.CString(go_str)
	// remember to free the CString!
}

//export FillRight
func FillRight(s *C.char, w C.int) *C.char {
	go_str := runewidth.FillRight(C.GoString(s), int(w))
	return C.CString(go_str)
	// remember to free the CString!
}

//export IsAmbiguousWidth
func IsAmbiguousWidth(r C.uint32_t) C.int {
	if runewidth.IsAmbiguousWidth(rune(r)) {
		return C.int(1)
	} else {
		return C.int(0)
	}
}

//export IsEastAsian
func IsEastAsian() C.int {
	if runewidth.IsEastAsian() {
		return C.int(1)
	} else {
		return C.int(0)
	}

}

//export IsNeutralWidth
func IsNeutralWidth(r C.uint32_t) C.int {
	if runewidth.IsNeutralWidth(rune(r)) {
		return C.int(1)
	} else {
		return C.int(0)
	}
}

//export RuneWidth
func RuneWidth(r C.uint32_t) C.int {
	return C.int(runewidth.RuneWidth(rune(r)))
}

//export StringWidth
func StringWidth(s *C.char) C.int {
	return C.int(runewidth.StringWidth(C.GoString(s)))
}

//export Truncate
func Truncate(s *C.char, w C.int, tail *C.char) *C.char {
	go_str := runewidth.Truncate(C.GoString(s), int(w), C.GoString(tail))
	return C.CString(go_str)
	// remember to free the CString!
}

//export Wrap
func Wrap(s *C.char, w C.int) *C.char {
	go_str := runewidth.Wrap(C.GoString(s), int(w))
	return C.CString(go_str)
	// remember to free the CString!
}

func main() {}
