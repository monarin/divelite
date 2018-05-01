#include <Python.h>
#include <structmember.h>
#include <stdio.h>
#include <stdlib.h>

using namespace std;

typedef struct {
    PyObject_HEAD
    /* Type-specific fields go here. */
    size_t offset;
} BufferedReader;

static void BufferedReader_dealloc(BufferedReader* self)
{
    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject* BufferedReader_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    BufferedReader* self;
    
    self = (BufferedReader*)type->tp_alloc(type, 0);
    if (self != NULL) {
        self->offset = 0;
    }

    return (PyObject *)self;
}

static int BufferedReader_init(BufferedReader* self, PyObject* args, PyObject* kwds)
{
    static char *kwlist[] = {"offset", NULL};

    if (! PyArg_ParseTupleAndKeywords(args, kwds, "|i", kwlist, 
                                      &self->offset))
        return -1;
    
    return 0;    
}

static PyMethodDef BufferedReader_methods[] = {
    {NULL}  /* sentinel */
};

static PyMemberDef BufferedReader_members[] = {
    { (char*)"_offset",
      T_UINT, offsetof(BufferedReader, offset),
      0,
      (char*)"attribute offset" },
    { NULL } /* sentinel */
};

static PyTypeObject BufferedReaderType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "bufferedreader.BufferedReader",        /* tp_name */
    sizeof(BufferedReader),  /* tp_basicsize */
    0,                                      /* tp_itemsize */
    (destructor)BufferedReader_dealloc,     /* tp_dealloc */
    0,                                      /* tp_print */
    0,                                      /* tp_getattr */
    0,                                      /* tp_setattr */
    0,                                      /* tp_compare */
    0,                                      /* tp_repr */
    0,                                      /* tp_as_number */
    0,                                      /* tp_as_sequence */
    0,                                      /* tp_as_mapping */
    0,                                      /* tp_hash */
    0,                                      /* tp_call */
    0,                                      /* tp_str */
    0,                                      /* tp_getattro */
    0,                                      /* tp_setattro */
    0,                                      /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT |
        Py_TPFLAGS_BASETYPE,                /* tp_flags */
    "BufferedReader objects",               /* tp_doc */
    0,                                      /* tp_traverse */
    0,                                      /* tp_clear */
    0,                                      /* tp_richcompare */
    0,                                      /* tp_weaklistoffset */
    0,                                      /* tp_iter */
    0,                                      /* tp_iternext */
    BufferedReader_methods,                 /* tp_methods */
    BufferedReader_members,                 /* tp_members */
    0,                                      /* tp_getset */
    0,                                      /* tp_base */
    0,                                      /* tp_dict */
    0,                                      /* tp_descr_get */
    0,                                      /* tp_descr_set */
    0,                                      /* tp_dictoffset */
    (initproc)BufferedReader_init,          /* tp_init */
    0,                                      /* tp_alloc */
    BufferedReader_new,                     /* tp_new */
    0,                                      /* tp_free;  Low-level free-memory routine */
    0,                                      /* tp_is_gc;  For PyObject_IS_GC */
    0,                                      /* tp_bases*/
    0,                                      /* tp_mro;  method resolution order */
    0,                                      /* tp_cache*/
    0,                                      /* tp_subclasses*/
    0,                                      /* tp_weaklist*/
    (destructor)BufferedReader_dealloc,     /* tp_del*/
};

#ifndef PyMODINIT_FUNC /* declarations for DLL import export */
#define PyMODINIT_FUNC void
#endif

#if PY_MAJOR_VERSION > 2
static PyModuleDef BufferedReader_module =
{ PyModuleDef_HEAD_INIT, "bufferedreader", NULL, -1, NULL, NULL, NULL, NULL, NULL };

PyMODINIT_FUNC PyInit_bufferedreader(void)
{
    PyObject* m;

    if (PyType_Ready(&BufferedReaderType) < 0){
        return NULL;
    }

    m = PyModule_Create(&BufferedReader_module);
    if (m == NULL) {
        return NULL;
    }

    Py_INCREF(&BufferedReaderType);
    PyModule_AddObject(m, "BufferedReader", (PyObject *)&BufferedReaderType);
    return m;
}
#else
PyMODINIT_FUNC initbufferedreader(void)
{
    PyObject *m;

    BufferedReaderType.tp_new = PyType_GenericNew;
    if (PyType_Ready(&BufferedReaderType) < 0)
        return;

    m = Py_InitModule3("bufferedreader", BufferedReader_methods,
                       "Methods for bufferedreader type.");
    
    if (m == NULL)
        return;

    Py_INCREF(&BufferedReaderType);
    PyModule_AddObject(m, "BufferedReader", (PyObject *)&BufferedReaderType);
}
#endif
