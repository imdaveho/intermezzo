/* Created by "go tool cgo" - DO NOT EDIT. */

/* package github.com/imdaveho/intermezzo/intermezzo/libs/intermezzo */

/* Start of preamble from import "C" comments.  */


#line 3 "/home/vagrant/development/gopher/workspace/src/github.com/imdaveho/intermezzo/intermezzo/libs/intermezzo/wrapper.go"

#include "interop.h"

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

typedef struct { const char *p; GoInt n; } GoString;
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

/****************************************************
* Termbox-Go API Wrappers                           *
****************************************************/

extern CellSlice* CellBuffer();

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

extern Event PollEvent();

extern int SetInputMode(int p0);

extern int SetOutputMode(int p0);

#ifdef __cplusplus
}
#endif
