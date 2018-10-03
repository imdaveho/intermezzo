/* Created by "go tool cgo" - DO NOT EDIT. */

/* package command-line-arguments */


#line 1 "cgo-builtin-prolog"

#include <stddef.h> /* for ptrdiff_t below */

#ifndef GO_CGO_EXPORT_PROLOGUE_H
#define GO_CGO_EXPORT_PROLOGUE_H

typedef struct { const char *p; ptrdiff_t n; } _GoString_;

#endif

/* Start of preamble from import "C" comments.  */


#line 3 "/Users/sharongraceho/Dave/sandbox/intermezzo/intermezzo/build/build_cgo_nix.go"


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


#line 1 "cgo-generated-wrapper"


/* End of preamble from import "C" comments.  */


/* Start of boilerplate cgo prologue.  */
#line 1 "cgo-gcc-export-header-prolog"

#ifndef GO_CGO_PROLOGUE_H
#define GO_CGO_PROLOGUE_H

typedef signed char GoInt8;
typedef unsigned char GoUint8;
typedef short GoInt16;
typedef unsigned short GoUint16;
typedef int GoInt32;
typedef unsigned int GoUint32;
typedef long long GoInt64;
typedef unsigned long long GoUint64;
typedef GoInt64 GoInt;
typedef GoUint64 GoUint;
typedef __SIZE_TYPE__ GoUintptr;
typedef float GoFloat32;
typedef double GoFloat64;
typedef float _Complex GoComplex64;
typedef double _Complex GoComplex128;

/*
  static assertion to make sure the file is being used on architecture
  at least with matching size of GoInt.
*/
typedef char _check_for_64_bit_pointer_matching_GoInt[sizeof(void*)==64/8 ? 1:-1];

typedef _GoString_ GoString;
typedef void *GoMap;
typedef void *GoChan;
typedef struct { void *t; void *v; } GoInterface;
typedef struct { void *data; GoInt len; GoInt cap; } GoSlice;

#endif

/* End of boilerplate cgo prologue.  */

#ifdef __cplusplus
extern "C" {
#endif


/****************************************************
* These are free() calls to ensure that malloc'd    *
* memory is appropriately released after use. It    *
* is wrapped here in order to pass along to Py.CFFI *
****************************************************/

extern void freeCells(CellSlice* p0);

extern void freeString(char* p0);

extern void freeEvent(Event* p0);

extern void freeRawEvent(RawEvent* p0);

/****************************************************
* Termbox-Go API Wrappers                           *
****************************************************/

extern int IsInit();

extern CellSlice* CellBuffer();

extern Error CopyIntoCellBuffer(Cell* p0, int p1, int p2);

extern Error Clear(uint16_t p0, uint16_t p1);

extern void Close();

extern Error Flush();

extern void HideCursor();

extern Error Init();

extern void Interrupt();

extern void SetCell(int p0, int p1, int32_t p2, uint16_t p3, uint16_t p4);

extern void SetCursor(int p0, int p1);

extern SizeTuple Size();

extern Error Sync();

extern Event* PollEvent();

extern int SetInputMode(int p0);

extern int SetOutputMode(int p0);

// From godoc.org/github.com/nsf/termbox-go:
// NOTE: This API is experimental and may change in the future

extern RawEvent* ParseEvent(void* p0, int p1);

// From godoc.org/github.com/nsf/termbox-go:
// NOTE: This API is experimental and may change in the future

extern RawEvent* PollRawEvent(void* p0, int p1);

/****************************************************
* Go-Runewidth API Wrappers                         *
* NOTE: As a dependency for Termbox-Go, including   *
* runewidth attempts to keep the library as stand-  *
* alone as possible while still maintaining a small *
* and simple footprint                              *
****************************************************/

extern char* FillLeft(char* p0, int p1);

extern char* FillRight(char* p0, int p1);

extern int IsAmbiguousWidth(uint32_t p0);

extern int IsEastAsian();

extern int IsNeutralWidth(uint32_t p0);

extern int RuneWidth(uint32_t p0);

extern int StringWidth(char* p0);

extern char* Truncate(char* p0, int p1, char* p2);

extern char* Wrap(char* p0, int p1);

#ifdef __cplusplus
}
#endif