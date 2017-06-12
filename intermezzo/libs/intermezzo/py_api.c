#define _CFFI_

/* We try to define Py_LIMITED_API before including Python.h.

   Mess: we can only define it if Py_DEBUG, Py_TRACE_REFS and
   Py_REF_DEBUG are not defined.  This is a best-effort approximation:
   we can learn about Py_DEBUG from pyconfig.h, but it is unclear if
   the same works for the other two macros.  Py_DEBUG implies them,
   but not the other way around.
*/
#ifndef _CFFI_USE_EMBEDDING
#  include <pyconfig.h>
#  if !defined(Py_DEBUG) && !defined(Py_TRACE_REFS) && !defined(Py_REF_DEBUG)
#    define Py_LIMITED_API
#  endif
#endif

#include <Python.h>
#ifdef __cplusplus
extern "C" {
#endif
#include <stddef.h>

/* This part is from file 'cffi/parse_c_type.h'.  It is copied at the
   beginning of C sources generated by CFFI's ffi.set_source(). */

typedef void *_cffi_opcode_t;

#define _CFFI_OP(opcode, arg)   (_cffi_opcode_t)(opcode | (((uintptr_t)(arg)) << 8))
#define _CFFI_GETOP(cffi_opcode)    ((unsigned char)(uintptr_t)cffi_opcode)
#define _CFFI_GETARG(cffi_opcode)   (((intptr_t)cffi_opcode) >> 8)

#define _CFFI_OP_PRIMITIVE       1
#define _CFFI_OP_POINTER         3
#define _CFFI_OP_ARRAY           5
#define _CFFI_OP_OPEN_ARRAY      7
#define _CFFI_OP_STRUCT_UNION    9
#define _CFFI_OP_ENUM           11
#define _CFFI_OP_FUNCTION       13
#define _CFFI_OP_FUNCTION_END   15
#define _CFFI_OP_NOOP           17
#define _CFFI_OP_BITFIELD       19
#define _CFFI_OP_TYPENAME       21
#define _CFFI_OP_CPYTHON_BLTN_V 23   // varargs
#define _CFFI_OP_CPYTHON_BLTN_N 25   // noargs
#define _CFFI_OP_CPYTHON_BLTN_O 27   // O  (i.e. a single arg)
#define _CFFI_OP_CONSTANT       29
#define _CFFI_OP_CONSTANT_INT   31
#define _CFFI_OP_GLOBAL_VAR     33
#define _CFFI_OP_DLOPEN_FUNC    35
#define _CFFI_OP_DLOPEN_CONST   37
#define _CFFI_OP_GLOBAL_VAR_F   39
#define _CFFI_OP_EXTERN_PYTHON  41

#define _CFFI_PRIM_VOID          0
#define _CFFI_PRIM_BOOL          1
#define _CFFI_PRIM_CHAR          2
#define _CFFI_PRIM_SCHAR         3
#define _CFFI_PRIM_UCHAR         4
#define _CFFI_PRIM_SHORT         5
#define _CFFI_PRIM_USHORT        6
#define _CFFI_PRIM_INT           7
#define _CFFI_PRIM_UINT          8
#define _CFFI_PRIM_LONG          9
#define _CFFI_PRIM_ULONG        10
#define _CFFI_PRIM_LONGLONG     11
#define _CFFI_PRIM_ULONGLONG    12
#define _CFFI_PRIM_FLOAT        13
#define _CFFI_PRIM_DOUBLE       14
#define _CFFI_PRIM_LONGDOUBLE   15

#define _CFFI_PRIM_WCHAR        16
#define _CFFI_PRIM_INT8         17
#define _CFFI_PRIM_UINT8        18
#define _CFFI_PRIM_INT16        19
#define _CFFI_PRIM_UINT16       20
#define _CFFI_PRIM_INT32        21
#define _CFFI_PRIM_UINT32       22
#define _CFFI_PRIM_INT64        23
#define _CFFI_PRIM_UINT64       24
#define _CFFI_PRIM_INTPTR       25
#define _CFFI_PRIM_UINTPTR      26
#define _CFFI_PRIM_PTRDIFF      27
#define _CFFI_PRIM_SIZE         28
#define _CFFI_PRIM_SSIZE        29
#define _CFFI_PRIM_INT_LEAST8   30
#define _CFFI_PRIM_UINT_LEAST8  31
#define _CFFI_PRIM_INT_LEAST16  32
#define _CFFI_PRIM_UINT_LEAST16 33
#define _CFFI_PRIM_INT_LEAST32  34
#define _CFFI_PRIM_UINT_LEAST32 35
#define _CFFI_PRIM_INT_LEAST64  36
#define _CFFI_PRIM_UINT_LEAST64 37
#define _CFFI_PRIM_INT_FAST8    38
#define _CFFI_PRIM_UINT_FAST8   39
#define _CFFI_PRIM_INT_FAST16   40
#define _CFFI_PRIM_UINT_FAST16  41
#define _CFFI_PRIM_INT_FAST32   42
#define _CFFI_PRIM_UINT_FAST32  43
#define _CFFI_PRIM_INT_FAST64   44
#define _CFFI_PRIM_UINT_FAST64  45
#define _CFFI_PRIM_INTMAX       46
#define _CFFI_PRIM_UINTMAX      47

#define _CFFI__NUM_PRIM         48
#define _CFFI__UNKNOWN_PRIM           (-1)
#define _CFFI__UNKNOWN_FLOAT_PRIM     (-2)
#define _CFFI__UNKNOWN_LONG_DOUBLE    (-3)

#define _CFFI__IO_FILE_STRUCT         (-1)


struct _cffi_global_s {
    const char *name;
    void *address;
    _cffi_opcode_t type_op;
    void *size_or_direct_fn;  // OP_GLOBAL_VAR: size, or 0 if unknown
                              // OP_CPYTHON_BLTN_*: addr of direct function
};

struct _cffi_getconst_s {
    unsigned long long value;
    const struct _cffi_type_context_s *ctx;
    int gindex;
};

struct _cffi_struct_union_s {
    const char *name;
    int type_index;          // -> _cffi_types, on a OP_STRUCT_UNION
    int flags;               // _CFFI_F_* flags below
    size_t size;
    int alignment;
    int first_field_index;   // -> _cffi_fields array
    int num_fields;
};
#define _CFFI_F_UNION         0x01   // is a union, not a struct
#define _CFFI_F_CHECK_FIELDS  0x02   // complain if fields are not in the
                                     // "standard layout" or if some are missing
#define _CFFI_F_PACKED        0x04   // for CHECK_FIELDS, assume a packed struct
#define _CFFI_F_EXTERNAL      0x08   // in some other ffi.include()
#define _CFFI_F_OPAQUE        0x10   // opaque

struct _cffi_field_s {
    const char *name;
    size_t field_offset;
    size_t field_size;
    _cffi_opcode_t field_type_op;
};

struct _cffi_enum_s {
    const char *name;
    int type_index;          // -> _cffi_types, on a OP_ENUM
    int type_prim;           // _CFFI_PRIM_xxx
    const char *enumerators; // comma-delimited string
};

struct _cffi_typename_s {
    const char *name;
    int type_index;   /* if opaque, points to a possibly artificial
                         OP_STRUCT which is itself opaque */
};

struct _cffi_type_context_s {
    _cffi_opcode_t *types;
    const struct _cffi_global_s *globals;
    const struct _cffi_field_s *fields;
    const struct _cffi_struct_union_s *struct_unions;
    const struct _cffi_enum_s *enums;
    const struct _cffi_typename_s *typenames;
    int num_globals;
    int num_struct_unions;
    int num_enums;
    int num_typenames;
    const char *const *includes;
    int num_types;
    int flags;      /* future extension */
};

struct _cffi_parse_info_s {
    const struct _cffi_type_context_s *ctx;
    _cffi_opcode_t *output;
    unsigned int output_size;
    size_t error_location;
    const char *error_message;
};

struct _cffi_externpy_s {
    const char *name;
    size_t size_of_result;
    void *reserved1, *reserved2;
};

#ifdef _CFFI_INTERNAL
static int parse_c_type(struct _cffi_parse_info_s *info, const char *input);
static int search_in_globals(const struct _cffi_type_context_s *ctx,
                             const char *search, size_t search_len);
static int search_in_struct_unions(const struct _cffi_type_context_s *ctx,
                                   const char *search, size_t search_len);
#endif

/* this block of #ifs should be kept exactly identical between
   c/_cffi_backend.c, cffi/vengine_cpy.py, cffi/vengine_gen.py
   and cffi/_cffi_include.h */
#if defined(_MSC_VER)
# include <malloc.h>   /* for alloca() */
# if _MSC_VER < 1600   /* MSVC < 2010 */
   typedef __int8 int8_t;
   typedef __int16 int16_t;
   typedef __int32 int32_t;
   typedef __int64 int64_t;
   typedef unsigned __int8 uint8_t;
   typedef unsigned __int16 uint16_t;
   typedef unsigned __int32 uint32_t;
   typedef unsigned __int64 uint64_t;
   typedef __int8 int_least8_t;
   typedef __int16 int_least16_t;
   typedef __int32 int_least32_t;
   typedef __int64 int_least64_t;
   typedef unsigned __int8 uint_least8_t;
   typedef unsigned __int16 uint_least16_t;
   typedef unsigned __int32 uint_least32_t;
   typedef unsigned __int64 uint_least64_t;
   typedef __int8 int_fast8_t;
   typedef __int16 int_fast16_t;
   typedef __int32 int_fast32_t;
   typedef __int64 int_fast64_t;
   typedef unsigned __int8 uint_fast8_t;
   typedef unsigned __int16 uint_fast16_t;
   typedef unsigned __int32 uint_fast32_t;
   typedef unsigned __int64 uint_fast64_t;
   typedef __int64 intmax_t;
   typedef unsigned __int64 uintmax_t;
# else
#  include <stdint.h>
# endif
# if _MSC_VER < 1800   /* MSVC < 2013 */
#  ifndef __cplusplus
    typedef unsigned char _Bool;
#  endif
# endif
#else
# include <stdint.h>
# if (defined (__SVR4) && defined (__sun)) || defined(_AIX) || defined(__hpux)
#  include <alloca.h>
# endif
#endif

#ifdef __GNUC__
# define _CFFI_UNUSED_FN  __attribute__((unused))
#else
# define _CFFI_UNUSED_FN  /* nothing */
#endif

#ifdef __cplusplus
# ifndef _Bool
   typedef bool _Bool;   /* semi-hackish: C++ has no _Bool; bool is builtin */
# endif
#endif

/**********  CPython-specific section  **********/
#ifndef PYPY_VERSION


#if PY_MAJOR_VERSION >= 3
# define PyInt_FromLong PyLong_FromLong
#endif

#define _cffi_from_c_double PyFloat_FromDouble
#define _cffi_from_c_float PyFloat_FromDouble
#define _cffi_from_c_long PyInt_FromLong
#define _cffi_from_c_ulong PyLong_FromUnsignedLong
#define _cffi_from_c_longlong PyLong_FromLongLong
#define _cffi_from_c_ulonglong PyLong_FromUnsignedLongLong

#define _cffi_to_c_double PyFloat_AsDouble
#define _cffi_to_c_float PyFloat_AsDouble

#define _cffi_from_c_int(x, type)                                        \
    (((type)-1) > 0 ? /* unsigned */                                     \
        (sizeof(type) < sizeof(long) ?                                   \
            PyInt_FromLong((long)x) :                                    \
         sizeof(type) == sizeof(long) ?                                  \
            PyLong_FromUnsignedLong((unsigned long)x) :                  \
            PyLong_FromUnsignedLongLong((unsigned long long)x)) :        \
        (sizeof(type) <= sizeof(long) ?                                  \
            PyInt_FromLong((long)x) :                                    \
            PyLong_FromLongLong((long long)x)))

#define _cffi_to_c_int(o, type)                                          \
    ((type)(                                                             \
     sizeof(type) == 1 ? (((type)-1) > 0 ? (type)_cffi_to_c_u8(o)        \
                                         : (type)_cffi_to_c_i8(o)) :     \
     sizeof(type) == 2 ? (((type)-1) > 0 ? (type)_cffi_to_c_u16(o)       \
                                         : (type)_cffi_to_c_i16(o)) :    \
     sizeof(type) == 4 ? (((type)-1) > 0 ? (type)_cffi_to_c_u32(o)       \
                                         : (type)_cffi_to_c_i32(o)) :    \
     sizeof(type) == 8 ? (((type)-1) > 0 ? (type)_cffi_to_c_u64(o)       \
                                         : (type)_cffi_to_c_i64(o)) :    \
     (Py_FatalError("unsupported size for type " #type), (type)0)))

#define _cffi_to_c_i8                                                    \
                 ((int(*)(PyObject *))_cffi_exports[1])
#define _cffi_to_c_u8                                                    \
                 ((int(*)(PyObject *))_cffi_exports[2])
#define _cffi_to_c_i16                                                   \
                 ((int(*)(PyObject *))_cffi_exports[3])
#define _cffi_to_c_u16                                                   \
                 ((int(*)(PyObject *))_cffi_exports[4])
#define _cffi_to_c_i32                                                   \
                 ((int(*)(PyObject *))_cffi_exports[5])
#define _cffi_to_c_u32                                                   \
                 ((unsigned int(*)(PyObject *))_cffi_exports[6])
#define _cffi_to_c_i64                                                   \
                 ((long long(*)(PyObject *))_cffi_exports[7])
#define _cffi_to_c_u64                                                   \
                 ((unsigned long long(*)(PyObject *))_cffi_exports[8])
#define _cffi_to_c_char                                                  \
                 ((int(*)(PyObject *))_cffi_exports[9])
#define _cffi_from_c_pointer                                             \
    ((PyObject *(*)(char *, struct _cffi_ctypedescr *))_cffi_exports[10])
#define _cffi_to_c_pointer                                               \
    ((char *(*)(PyObject *, struct _cffi_ctypedescr *))_cffi_exports[11])
#define _cffi_get_struct_layout                                          \
    not used any more
#define _cffi_restore_errno                                              \
    ((void(*)(void))_cffi_exports[13])
#define _cffi_save_errno                                                 \
    ((void(*)(void))_cffi_exports[14])
#define _cffi_from_c_char                                                \
    ((PyObject *(*)(char))_cffi_exports[15])
#define _cffi_from_c_deref                                               \
    ((PyObject *(*)(char *, struct _cffi_ctypedescr *))_cffi_exports[16])
#define _cffi_to_c                                                       \
    ((int(*)(char *, struct _cffi_ctypedescr *, PyObject *))_cffi_exports[17])
#define _cffi_from_c_struct                                              \
    ((PyObject *(*)(char *, struct _cffi_ctypedescr *))_cffi_exports[18])
#define _cffi_to_c_wchar_t                                               \
    ((wchar_t(*)(PyObject *))_cffi_exports[19])
#define _cffi_from_c_wchar_t                                             \
    ((PyObject *(*)(wchar_t))_cffi_exports[20])
#define _cffi_to_c_long_double                                           \
    ((long double(*)(PyObject *))_cffi_exports[21])
#define _cffi_to_c__Bool                                                 \
    ((_Bool(*)(PyObject *))_cffi_exports[22])
#define _cffi_prepare_pointer_call_argument                              \
    ((Py_ssize_t(*)(struct _cffi_ctypedescr *,                           \
                    PyObject *, char **))_cffi_exports[23])
#define _cffi_convert_array_from_object                                  \
    ((int(*)(char *, struct _cffi_ctypedescr *, PyObject *))_cffi_exports[24])
#define _CFFI_CPIDX  25
#define _cffi_call_python                                                \
    ((void(*)(struct _cffi_externpy_s *, char *))_cffi_exports[_CFFI_CPIDX])
#define _CFFI_NUM_EXPORTS 26

struct _cffi_ctypedescr;

static void *_cffi_exports[_CFFI_NUM_EXPORTS];

#define _cffi_type(index)   (                           \
    assert((((uintptr_t)_cffi_types[index]) & 1) == 0), \
    (struct _cffi_ctypedescr *)_cffi_types[index])

static PyObject *_cffi_init(const char *module_name, Py_ssize_t version,
                            const struct _cffi_type_context_s *ctx)
{
    PyObject *module, *o_arg, *new_module;
    void *raw[] = {
        (void *)module_name,
        (void *)version,
        (void *)_cffi_exports,
        (void *)ctx,
    };

    module = PyImport_ImportModule("_cffi_backend");
    if (module == NULL)
        goto failure;

    o_arg = PyLong_FromVoidPtr((void *)raw);
    if (o_arg == NULL)
        goto failure;

    new_module = PyObject_CallMethod(
        module, (char *)"_init_cffi_1_0_external_module", (char *)"O", o_arg);

    Py_DECREF(o_arg);
    Py_DECREF(module);
    return new_module;

  failure:
    Py_XDECREF(module);
    return NULL;
}

/**********  end CPython-specific section  **********/
#else
_CFFI_UNUSED_FN
static void (*_cffi_call_python_org)(struct _cffi_externpy_s *, char *);
# define _cffi_call_python  _cffi_call_python_org
#endif


#define _cffi_array_len(array)   (sizeof(array) / sizeof((array)[0]))

#define _cffi_prim_int(size, sign)                                      \
    ((size) == 1 ? ((sign) ? _CFFI_PRIM_INT8  : _CFFI_PRIM_UINT8)  :    \
     (size) == 2 ? ((sign) ? _CFFI_PRIM_INT16 : _CFFI_PRIM_UINT16) :    \
     (size) == 4 ? ((sign) ? _CFFI_PRIM_INT32 : _CFFI_PRIM_UINT32) :    \
     (size) == 8 ? ((sign) ? _CFFI_PRIM_INT64 : _CFFI_PRIM_UINT64) :    \
     _CFFI__UNKNOWN_PRIM)

#define _cffi_prim_float(size)                                          \
    ((size) == sizeof(float) ? _CFFI_PRIM_FLOAT :                       \
     (size) == sizeof(double) ? _CFFI_PRIM_DOUBLE :                     \
     (size) == sizeof(long double) ? _CFFI__UNKNOWN_LONG_DOUBLE :       \
     _CFFI__UNKNOWN_FLOAT_PRIM)

#define _cffi_check_int(got, got_nonpos, expected)      \
    ((got_nonpos) == (expected <= 0) &&                 \
     (got) == (unsigned long long)expected)

#ifdef MS_WIN32
# define _cffi_stdcall  __stdcall
#else
# define _cffi_stdcall  /* nothing */
#endif

#ifdef __cplusplus
}
#endif

/************************************************************/


#include "cgo_api.h"


/************************************************************/

static void *_cffi_types[] = {
/*  0 */ _CFFI_OP(_CFFI_OP_FUNCTION, 16), // CellSlice *()(void)
/*  1 */ _CFFI_OP(_CFFI_OP_FUNCTION_END, 0),
/*  2 */ _CFFI_OP(_CFFI_OP_FUNCTION, 19), // Event *()(void)
/*  3 */ _CFFI_OP(_CFFI_OP_FUNCTION_END, 0),
/*  4 */ _CFFI_OP(_CFFI_OP_FUNCTION, 41), // SizeTuple()(void)
/*  5 */ _CFFI_OP(_CFFI_OP_FUNCTION_END, 0),
/*  6 */ _CFFI_OP(_CFFI_OP_FUNCTION, 22), // char *()(uint16_t, uint16_t)
/*  7 */ _CFFI_OP(_CFFI_OP_PRIMITIVE, 20), // uint16_t
/*  8 */ _CFFI_OP(_CFFI_OP_PRIMITIVE, 20),
/*  9 */ _CFFI_OP(_CFFI_OP_FUNCTION_END, 0),
/* 10 */ _CFFI_OP(_CFFI_OP_FUNCTION, 22), // char *()(void)
/* 11 */ _CFFI_OP(_CFFI_OP_FUNCTION_END, 0),
/* 12 */ _CFFI_OP(_CFFI_OP_FUNCTION, 13), // int()(int)
/* 13 */ _CFFI_OP(_CFFI_OP_PRIMITIVE, 7), // int
/* 14 */ _CFFI_OP(_CFFI_OP_FUNCTION_END, 0),
/* 15 */ _CFFI_OP(_CFFI_OP_FUNCTION, 44), // void()(CellSlice *)
/* 16 */ _CFFI_OP(_CFFI_OP_POINTER, 39), // CellSlice *
/* 17 */ _CFFI_OP(_CFFI_OP_FUNCTION_END, 0),
/* 18 */ _CFFI_OP(_CFFI_OP_FUNCTION, 44), // void()(Event *)
/* 19 */ _CFFI_OP(_CFFI_OP_POINTER, 40), // Event *
/* 20 */ _CFFI_OP(_CFFI_OP_FUNCTION_END, 0),
/* 21 */ _CFFI_OP(_CFFI_OP_FUNCTION, 44), // void()(char *)
/* 22 */ _CFFI_OP(_CFFI_OP_POINTER, 42), // char *
/* 23 */ _CFFI_OP(_CFFI_OP_FUNCTION_END, 0),
/* 24 */ _CFFI_OP(_CFFI_OP_FUNCTION, 44), // void()(int, int)
/* 25 */ _CFFI_OP(_CFFI_OP_PRIMITIVE, 7),
/* 26 */ _CFFI_OP(_CFFI_OP_PRIMITIVE, 7),
/* 27 */ _CFFI_OP(_CFFI_OP_FUNCTION_END, 0),
/* 28 */ _CFFI_OP(_CFFI_OP_FUNCTION, 44), // void()(int, int, int32_t, uint16_t, uint16_t)
/* 29 */ _CFFI_OP(_CFFI_OP_PRIMITIVE, 7),
/* 30 */ _CFFI_OP(_CFFI_OP_PRIMITIVE, 7),
/* 31 */ _CFFI_OP(_CFFI_OP_PRIMITIVE, 21), // int32_t
/* 32 */ _CFFI_OP(_CFFI_OP_PRIMITIVE, 20),
/* 33 */ _CFFI_OP(_CFFI_OP_PRIMITIVE, 20),
/* 34 */ _CFFI_OP(_CFFI_OP_FUNCTION_END, 0),
/* 35 */ _CFFI_OP(_CFFI_OP_FUNCTION, 44), // void()(void)
/* 36 */ _CFFI_OP(_CFFI_OP_FUNCTION_END, 0),
/* 37 */ _CFFI_OP(_CFFI_OP_POINTER, 38), // Cell *
/* 38 */ _CFFI_OP(_CFFI_OP_STRUCT_UNION, 0), // Cell
/* 39 */ _CFFI_OP(_CFFI_OP_STRUCT_UNION, 1), // CellSlice
/* 40 */ _CFFI_OP(_CFFI_OP_STRUCT_UNION, 2), // Event
/* 41 */ _CFFI_OP(_CFFI_OP_STRUCT_UNION, 3), // SizeTuple
/* 42 */ _CFFI_OP(_CFFI_OP_PRIMITIVE, 2), // char
/* 43 */ _CFFI_OP(_CFFI_OP_PRIMITIVE, 18), // uint8_t
/* 44 */ _CFFI_OP(_CFFI_OP_PRIMITIVE, 0), // void
};

static CellSlice * _cffi_d_CellBuffer(void)
{
  return CellBuffer();
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_CellBuffer(PyObject *self, PyObject *noarg)
{
  CellSlice * result;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = CellBuffer(); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  (void)noarg; /* unused */
  return _cffi_from_c_pointer((char *)result, _cffi_type(16));
}
#else
#  define _cffi_f_CellBuffer _cffi_d_CellBuffer
#endif

static char * _cffi_d_Clear(uint16_t x0, uint16_t x1)
{
  return Clear(x0, x1);
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_Clear(PyObject *self, PyObject *args)
{
  uint16_t x0;
  uint16_t x1;
  char * result;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_UnpackTuple(args, "Clear", 2, 2, &arg0, &arg1))
    return NULL;

  x0 = _cffi_to_c_int(arg0, uint16_t);
  if (x0 == (uint16_t)-1 && PyErr_Occurred())
    return NULL;

  x1 = _cffi_to_c_int(arg1, uint16_t);
  if (x1 == (uint16_t)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = Clear(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_pointer((char *)result, _cffi_type(22));
}
#else
#  define _cffi_f_Clear _cffi_d_Clear
#endif

static void _cffi_d_Close(void)
{
  Close();
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_Close(PyObject *self, PyObject *noarg)
{

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { Close(); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  (void)noarg; /* unused */
  Py_INCREF(Py_None);
  return Py_None;
}
#else
#  define _cffi_f_Close _cffi_d_Close
#endif

static char * _cffi_d_Flush(void)
{
  return Flush();
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_Flush(PyObject *self, PyObject *noarg)
{
  char * result;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = Flush(); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  (void)noarg; /* unused */
  return _cffi_from_c_pointer((char *)result, _cffi_type(22));
}
#else
#  define _cffi_f_Flush _cffi_d_Flush
#endif

static void _cffi_d_HideCursor(void)
{
  HideCursor();
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_HideCursor(PyObject *self, PyObject *noarg)
{

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { HideCursor(); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  (void)noarg; /* unused */
  Py_INCREF(Py_None);
  return Py_None;
}
#else
#  define _cffi_f_HideCursor _cffi_d_HideCursor
#endif

static char * _cffi_d_Init(void)
{
  return Init();
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_Init(PyObject *self, PyObject *noarg)
{
  char * result;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = Init(); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  (void)noarg; /* unused */
  return _cffi_from_c_pointer((char *)result, _cffi_type(22));
}
#else
#  define _cffi_f_Init _cffi_d_Init
#endif

static void _cffi_d_Interrupt(void)
{
  Interrupt();
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_Interrupt(PyObject *self, PyObject *noarg)
{

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { Interrupt(); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  (void)noarg; /* unused */
  Py_INCREF(Py_None);
  return Py_None;
}
#else
#  define _cffi_f_Interrupt _cffi_d_Interrupt
#endif

static Event * _cffi_d_PollEvent(void)
{
  return PollEvent();
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_PollEvent(PyObject *self, PyObject *noarg)
{
  Event * result;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = PollEvent(); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  (void)noarg; /* unused */
  return _cffi_from_c_pointer((char *)result, _cffi_type(19));
}
#else
#  define _cffi_f_PollEvent _cffi_d_PollEvent
#endif

static void _cffi_d_SetCell(int x0, int x1, int32_t x2, uint16_t x3, uint16_t x4)
{
  SetCell(x0, x1, x2, x3, x4);
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_SetCell(PyObject *self, PyObject *args)
{
  int x0;
  int x1;
  int32_t x2;
  uint16_t x3;
  uint16_t x4;
  PyObject *arg0;
  PyObject *arg1;
  PyObject *arg2;
  PyObject *arg3;
  PyObject *arg4;

  if (!PyArg_UnpackTuple(args, "SetCell", 5, 5, &arg0, &arg1, &arg2, &arg3, &arg4))
    return NULL;

  x0 = _cffi_to_c_int(arg0, int);
  if (x0 == (int)-1 && PyErr_Occurred())
    return NULL;

  x1 = _cffi_to_c_int(arg1, int);
  if (x1 == (int)-1 && PyErr_Occurred())
    return NULL;

  x2 = _cffi_to_c_int(arg2, int32_t);
  if (x2 == (int32_t)-1 && PyErr_Occurred())
    return NULL;

  x3 = _cffi_to_c_int(arg3, uint16_t);
  if (x3 == (uint16_t)-1 && PyErr_Occurred())
    return NULL;

  x4 = _cffi_to_c_int(arg4, uint16_t);
  if (x4 == (uint16_t)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { SetCell(x0, x1, x2, x3, x4); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  Py_INCREF(Py_None);
  return Py_None;
}
#else
#  define _cffi_f_SetCell _cffi_d_SetCell
#endif

static void _cffi_d_SetCursor(int x0, int x1)
{
  SetCursor(x0, x1);
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_SetCursor(PyObject *self, PyObject *args)
{
  int x0;
  int x1;
  PyObject *arg0;
  PyObject *arg1;

  if (!PyArg_UnpackTuple(args, "SetCursor", 2, 2, &arg0, &arg1))
    return NULL;

  x0 = _cffi_to_c_int(arg0, int);
  if (x0 == (int)-1 && PyErr_Occurred())
    return NULL;

  x1 = _cffi_to_c_int(arg1, int);
  if (x1 == (int)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { SetCursor(x0, x1); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  Py_INCREF(Py_None);
  return Py_None;
}
#else
#  define _cffi_f_SetCursor _cffi_d_SetCursor
#endif

static int _cffi_d_SetInputMode(int x0)
{
  return SetInputMode(x0);
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_SetInputMode(PyObject *self, PyObject *arg0)
{
  int x0;
  int result;

  x0 = _cffi_to_c_int(arg0, int);
  if (x0 == (int)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = SetInputMode(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_int(result, int);
}
#else
#  define _cffi_f_SetInputMode _cffi_d_SetInputMode
#endif

static int _cffi_d_SetOutputMode(int x0)
{
  return SetOutputMode(x0);
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_SetOutputMode(PyObject *self, PyObject *arg0)
{
  int x0;
  int result;

  x0 = _cffi_to_c_int(arg0, int);
  if (x0 == (int)-1 && PyErr_Occurred())
    return NULL;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = SetOutputMode(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  return _cffi_from_c_int(result, int);
}
#else
#  define _cffi_f_SetOutputMode _cffi_d_SetOutputMode
#endif

static SizeTuple _cffi_d_Size(void)
{
  return Size();
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_Size(PyObject *self, PyObject *noarg)
{
  SizeTuple result;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = Size(); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  (void)noarg; /* unused */
  return _cffi_from_c_struct((char *)&result, _cffi_type(41));
}
#else
static void _cffi_f_Size(SizeTuple *result)
{
  { *result = Size(); }
}
#endif

static char * _cffi_d_Sync(void)
{
  return Sync();
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_Sync(PyObject *self, PyObject *noarg)
{
  char * result;

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { result = Sync(); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  (void)noarg; /* unused */
  return _cffi_from_c_pointer((char *)result, _cffi_type(22));
}
#else
#  define _cffi_f_Sync _cffi_d_Sync
#endif

static void _cffi_d_freeCells(CellSlice * x0)
{
  freeCells(x0);
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_freeCells(PyObject *self, PyObject *arg0)
{
  CellSlice * x0;
  Py_ssize_t datasize;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(16), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = (CellSlice *)alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(16), arg0) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { freeCells(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  Py_INCREF(Py_None);
  return Py_None;
}
#else
#  define _cffi_f_freeCells _cffi_d_freeCells
#endif

static void _cffi_d_freeEvent(Event * x0)
{
  freeEvent(x0);
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_freeEvent(PyObject *self, PyObject *arg0)
{
  Event * x0;
  Py_ssize_t datasize;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(19), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = (Event *)alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(19), arg0) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { freeEvent(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  Py_INCREF(Py_None);
  return Py_None;
}
#else
#  define _cffi_f_freeEvent _cffi_d_freeEvent
#endif

static void _cffi_d_freeString(char * x0)
{
  freeString(x0);
}
#ifndef PYPY_VERSION
static PyObject *
_cffi_f_freeString(PyObject *self, PyObject *arg0)
{
  char * x0;
  Py_ssize_t datasize;

  datasize = _cffi_prepare_pointer_call_argument(
      _cffi_type(22), arg0, (char **)&x0);
  if (datasize != 0) {
    if (datasize < 0)
      return NULL;
    x0 = (char *)alloca((size_t)datasize);
    memset((void *)x0, 0, (size_t)datasize);
    if (_cffi_convert_array_from_object((char *)x0, _cffi_type(22), arg0) < 0)
      return NULL;
  }

  Py_BEGIN_ALLOW_THREADS
  _cffi_restore_errno();
  { freeString(x0); }
  _cffi_save_errno();
  Py_END_ALLOW_THREADS

  (void)self; /* unused */
  Py_INCREF(Py_None);
  return Py_None;
}
#else
#  define _cffi_f_freeString _cffi_d_freeString
#endif

_CFFI_UNUSED_FN
static void _cffi_checkfld__Cell(Cell *p)
{
  /* only to generate compile-time warnings or errors */
  (void)p;
  (void)((p->Ch) | 0);  /* check that 'Cell.Ch' is an integer */
  (void)((p->Fg) | 0);  /* check that 'Cell.Fg' is an integer */
  (void)((p->Bg) | 0);  /* check that 'Cell.Bg' is an integer */
}
struct _cffi_align__Cell { char x; Cell y; };

_CFFI_UNUSED_FN
static void _cffi_checkfld__CellSlice(CellSlice *p)
{
  /* only to generate compile-time warnings or errors */
  (void)p;
  { Cell * *tmp = &p->data; (void)tmp; }
  (void)((p->len) | 0);  /* check that 'CellSlice.len' is an integer */
}
struct _cffi_align__CellSlice { char x; CellSlice y; };

_CFFI_UNUSED_FN
static void _cffi_checkfld__Event(Event *p)
{
  /* only to generate compile-time warnings or errors */
  (void)p;
  (void)((p->Type) | 0);  /* check that 'Event.Type' is an integer */
  (void)((p->Mod) | 0);  /* check that 'Event.Mod' is an integer */
  (void)((p->Key) | 0);  /* check that 'Event.Key' is an integer */
  (void)((p->Ch) | 0);  /* check that 'Event.Ch' is an integer */
  (void)((p->Width) | 0);  /* check that 'Event.Width' is an integer */
  (void)((p->Height) | 0);  /* check that 'Event.Height' is an integer */
  { char * *tmp = &p->Err; (void)tmp; }
  (void)((p->MouseX) | 0);  /* check that 'Event.MouseX' is an integer */
  (void)((p->MouseY) | 0);  /* check that 'Event.MouseY' is an integer */
  (void)((p->N) | 0);  /* check that 'Event.N' is an integer */
}
struct _cffi_align__Event { char x; Event y; };

_CFFI_UNUSED_FN
static void _cffi_checkfld__SizeTuple(SizeTuple *p)
{
  /* only to generate compile-time warnings or errors */
  (void)p;
  (void)((p->width) | 0);  /* check that 'SizeTuple.width' is an integer */
  (void)((p->height) | 0);  /* check that 'SizeTuple.height' is an integer */
}
struct _cffi_align__SizeTuple { char x; SizeTuple y; };

static const struct _cffi_global_s _cffi_globals[] = {
  { "CellBuffer", (void *)_cffi_f_CellBuffer, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_N, 0), (void *)_cffi_d_CellBuffer },
  { "Clear", (void *)_cffi_f_Clear, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_V, 6), (void *)_cffi_d_Clear },
  { "Close", (void *)_cffi_f_Close, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_N, 35), (void *)_cffi_d_Close },
  { "Flush", (void *)_cffi_f_Flush, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_N, 10), (void *)_cffi_d_Flush },
  { "HideCursor", (void *)_cffi_f_HideCursor, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_N, 35), (void *)_cffi_d_HideCursor },
  { "Init", (void *)_cffi_f_Init, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_N, 10), (void *)_cffi_d_Init },
  { "Interrupt", (void *)_cffi_f_Interrupt, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_N, 35), (void *)_cffi_d_Interrupt },
  { "PollEvent", (void *)_cffi_f_PollEvent, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_N, 2), (void *)_cffi_d_PollEvent },
  { "SetCell", (void *)_cffi_f_SetCell, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_V, 28), (void *)_cffi_d_SetCell },
  { "SetCursor", (void *)_cffi_f_SetCursor, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_V, 24), (void *)_cffi_d_SetCursor },
  { "SetInputMode", (void *)_cffi_f_SetInputMode, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_O, 12), (void *)_cffi_d_SetInputMode },
  { "SetOutputMode", (void *)_cffi_f_SetOutputMode, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_O, 12), (void *)_cffi_d_SetOutputMode },
  { "Size", (void *)_cffi_f_Size, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_N, 4), (void *)_cffi_d_Size },
  { "Sync", (void *)_cffi_f_Sync, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_N, 10), (void *)_cffi_d_Sync },
  { "freeCells", (void *)_cffi_f_freeCells, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_O, 15), (void *)_cffi_d_freeCells },
  { "freeEvent", (void *)_cffi_f_freeEvent, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_O, 18), (void *)_cffi_d_freeEvent },
  { "freeString", (void *)_cffi_f_freeString, _CFFI_OP(_CFFI_OP_CPYTHON_BLTN_O, 21), (void *)_cffi_d_freeString },
};

static const struct _cffi_field_s _cffi_fields[] = {
  { "Ch", offsetof(Cell, Ch),
          sizeof(((Cell *)0)->Ch),
          _CFFI_OP(_CFFI_OP_NOOP, 31) },
  { "Fg", offsetof(Cell, Fg),
          sizeof(((Cell *)0)->Fg),
          _CFFI_OP(_CFFI_OP_NOOP, 7) },
  { "Bg", offsetof(Cell, Bg),
          sizeof(((Cell *)0)->Bg),
          _CFFI_OP(_CFFI_OP_NOOP, 7) },
  { "data", offsetof(CellSlice, data),
            sizeof(((CellSlice *)0)->data),
            _CFFI_OP(_CFFI_OP_NOOP, 37) },
  { "len", offsetof(CellSlice, len),
           sizeof(((CellSlice *)0)->len),
           _CFFI_OP(_CFFI_OP_NOOP, 13) },
  { "Type", offsetof(Event, Type),
            sizeof(((Event *)0)->Type),
            _CFFI_OP(_CFFI_OP_NOOP, 43) },
  { "Mod", offsetof(Event, Mod),
           sizeof(((Event *)0)->Mod),
           _CFFI_OP(_CFFI_OP_NOOP, 43) },
  { "Key", offsetof(Event, Key),
           sizeof(((Event *)0)->Key),
           _CFFI_OP(_CFFI_OP_NOOP, 7) },
  { "Ch", offsetof(Event, Ch),
          sizeof(((Event *)0)->Ch),
          _CFFI_OP(_CFFI_OP_NOOP, 31) },
  { "Width", offsetof(Event, Width),
             sizeof(((Event *)0)->Width),
             _CFFI_OP(_CFFI_OP_NOOP, 13) },
  { "Height", offsetof(Event, Height),
              sizeof(((Event *)0)->Height),
              _CFFI_OP(_CFFI_OP_NOOP, 13) },
  { "Err", offsetof(Event, Err),
           sizeof(((Event *)0)->Err),
           _CFFI_OP(_CFFI_OP_NOOP, 22) },
  { "MouseX", offsetof(Event, MouseX),
              sizeof(((Event *)0)->MouseX),
              _CFFI_OP(_CFFI_OP_NOOP, 13) },
  { "MouseY", offsetof(Event, MouseY),
              sizeof(((Event *)0)->MouseY),
              _CFFI_OP(_CFFI_OP_NOOP, 13) },
  { "N", offsetof(Event, N),
         sizeof(((Event *)0)->N),
         _CFFI_OP(_CFFI_OP_NOOP, 13) },
  { "width", offsetof(SizeTuple, width),
             sizeof(((SizeTuple *)0)->width),
             _CFFI_OP(_CFFI_OP_NOOP, 13) },
  { "height", offsetof(SizeTuple, height),
              sizeof(((SizeTuple *)0)->height),
              _CFFI_OP(_CFFI_OP_NOOP, 13) },
};

static const struct _cffi_struct_union_s _cffi_struct_unions[] = {
  { "Cell", 38, _CFFI_F_CHECK_FIELDS,
    sizeof(Cell), offsetof(struct _cffi_align__Cell, y), 0, 3 },
  { "CellSlice", 39, _CFFI_F_CHECK_FIELDS,
    sizeof(CellSlice), offsetof(struct _cffi_align__CellSlice, y), 3, 2 },
  { "Event", 40, _CFFI_F_CHECK_FIELDS,
    sizeof(Event), offsetof(struct _cffi_align__Event, y), 5, 10 },
  { "SizeTuple", 41, _CFFI_F_CHECK_FIELDS,
    sizeof(SizeTuple), offsetof(struct _cffi_align__SizeTuple, y), 15, 2 },
};

static const struct _cffi_typename_s _cffi_typenames[] = {
  { "Cell", 38 },
  { "CellSlice", 39 },
  { "Error", 22 },
  { "Event", 40 },
  { "SizeTuple", 41 },
};

static const struct _cffi_type_context_s _cffi_type_context = {
  _cffi_types,
  _cffi_globals,
  _cffi_fields,
  _cffi_struct_unions,
  NULL,  /* no enums */
  _cffi_typenames,
  17,  /* num_globals */
  4,  /* num_struct_unions */
  0,  /* num_enums */
  5,  /* num_typenames */
  NULL,  /* no includes */
  45,  /* num_types */
  0,  /* flags */
};

#ifdef __GNUC__
#  pragma GCC visibility push(default)  /* for -fvisibility= */
#endif

#ifdef PYPY_VERSION
PyMODINIT_FUNC
_cffi_pypyinit_py_api(const void *p[])
{
    p[0] = (const void *)0x2601;
    p[1] = &_cffi_type_context;
}
#  ifdef _MSC_VER
     PyMODINIT_FUNC
#  if PY_MAJOR_VERSION >= 3
     PyInit_py_api(void) { return NULL; }
#  else
     initpy_api(void) { }
#  endif
#  endif
#elif PY_MAJOR_VERSION >= 3
PyMODINIT_FUNC
PyInit_py_api(void)
{
  return _cffi_init("py_api", 0x2601, &_cffi_type_context);
}
#else
PyMODINIT_FUNC
initpy_api(void)
{
  _cffi_init("py_api", 0x2601, &_cffi_type_context);
}
#endif

#ifdef __GNUC__
#  pragma GCC visibility pop
#endif
