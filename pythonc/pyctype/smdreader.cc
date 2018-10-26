#include <Python.h>
#include <structmember.h>
#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <assert.h>

using namespace std;

#define CHUNKSIZE 0x100000
#define MAXRETRIES 5

/* Xtc remanufactored struct for simple data acess and the Buffer struct */
struct Xtc {
    int junks[4];
    unsigned extent;
};

struct Sequence {
    int junks[2];
    unsigned low;
    unsigned high;
};

struct Dgram {
    Sequence seq;
    int junks[4];
    Xtc xtc;
};

struct Buffer {
    char* chunk;
    size_t got;
    size_t offset;
    size_t prev_offset;
    unsigned nevents;
    unsigned long timestamp;
    size_t block_offset;
    size_t block_size;
};

typedef struct {
    PyObject_HEAD
    /* Type-specific fields go here. */
    PyObject* fds;
    Buffer* bufs;
    ssize_t nfiles;
    unsigned got_events;
    unsigned long limit_ts;
    size_t dgram_size;
    size_t xtc_size;
} SmdReader;

/* member functions of SmdReader python object */
static void SmdReader_dealloc(SmdReader* self)
{
    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject* SmdReader_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    SmdReader* self;
    
    self = (SmdReader*)type->tp_alloc(type, 0);
    if (self != NULL) {
        //
    }

    return (PyObject *)self;
}

static int SmdReader_init(SmdReader* self, PyObject* args, PyObject* kwds)
{
    static char *kwlist[] = {"file_descriptors", NULL};

    if (! PyArg_ParseTupleAndKeywords(args, kwds, "O", kwlist, 
                                      &self->fds))
        return -1;
    self->nfiles = PyList_Size(self->fds);
    cout << self->nfiles << endl; 
    self->bufs = NULL;
    self->got_events = 0;
    self->limit_ts = 1;
    self->dgram_size = sizeof(Dgram);
    self->xtc_size = sizeof(Xtc);
    return 0;    
}

static void SmdReader_get(SmdReader* self, PyObject* args) {
    int nevents;

    if (! PyArg_ParseTuple(args, "i", &nevents)) {
        return;
    }

    cout << nevents << endl;

} 

static PyMethodDef SmdReader_methods[] = {
    {"get", (PyCFunction)SmdReader_get, METH_VARARGS,
     "Fill buffer with data that can be access through view."
    },
    {NULL}  /* sentinel */
};

static PyMemberDef SmdReader_members[] = {
    { (char*)"_fds",
      T_OBJECT_EX, offsetof(SmdReader, fds),
      0,
      (char*)"List of file descriptors" },
    { NULL } /* sentinel */
};

static PyTypeObject SmdReaderType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "smdreader.SmdReader",        /* tp_name */
    sizeof(SmdReader),  /* tp_basicsize */
    0,                                      /* tp_itemsize */
    (destructor)SmdReader_dealloc,     /* tp_dealloc */
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
    "SmdReader objects",               /* tp_doc */
    0,                                      /* tp_traverse */
    0,                                      /* tp_clear */
    0,                                      /* tp_richcompare */
    0,                                      /* tp_weaklistoffset */
    0,                                      /* tp_iter */
    0,                                      /* tp_iternext */
    SmdReader_methods,                 /* tp_methods */
    SmdReader_members,                 /* tp_members */
    0,                                      /* tp_getset */
    0,                                      /* tp_base */
    0,                                      /* tp_dict */
    0,                                      /* tp_descr_get */
    0,                                      /* tp_descr_set */
    0,                                      /* tp_dictoffset */
    (initproc)SmdReader_init,          /* tp_init */
    0,                                      /* tp_alloc */
    SmdReader_new,                     /* tp_new */
    0,                                      /* tp_free;  Low-level free-memory routine */
    0,                                      /* tp_is_gc;  For PyObject_IS_GC */
    0,                                      /* tp_bases*/
    0,                                      /* tp_mro;  method resolution order */
    0,                                      /* tp_cache*/
    0,                                      /* tp_subclasses*/
    0,                                      /* tp_weaklist*/
    (destructor)SmdReader_dealloc,     /* tp_del*/
};

#ifndef PyMODINIT_FUNC /* declarations for DLL import export */
#define PyMODINIT_FUNC void
#endif

#if PY_MAJOR_VERSION > 2
static PyModuleDef SmdReader_module =
{ PyModuleDef_HEAD_INIT, "smdreader", NULL, -1, NULL, NULL, NULL, NULL, NULL };

PyMODINIT_FUNC PyInit_smdreader(void)
{
    PyObject* m;

    if (PyType_Ready(&SmdReaderType) < 0){
        return NULL;
    }

    m = PyModule_Create(&SmdReader_module);
    if (m == NULL) {
        return NULL;
    }

    Py_INCREF(&SmdReaderType);
    PyModule_AddObject(m, "SmdReader", (PyObject *)&SmdReaderType);
    return m;
}
#else
PyMODINIT_FUNC initsmdreader(void)
{
    PyObject *m;

    SmdReaderType.tp_new = PyType_GenericNew;
    if (PyType_Ready(&SmdReaderType) < 0)
        return;

    m = Py_InitModule3("smdreader", SmdReader_methods,
                       "Methods for smdreader type.");
    
    if (m == NULL)
        return;

    Py_INCREF(&SmdReaderType);
    PyModule_AddObject(m, "SmdReader", (PyObject *)&SmdReaderType);
}
#endif

/* functions used by smdreader class (not exposed to users) */
static size_t _read_with_retries(SmdReader* self, int buf_id, size_t displacement, size_t count) {
    char* chunk = self->bufs[buf_id].chunk + displacement;
    size_t requested = count;
    size_t got = 0;
    for (int attempt=0; attempt<MAXRETRIES; attempt++) {
        int fd = PyInt_AsLong(PyList_GetItem(self->fds, buf_id));
        got = read(fd, chunk, count);
        if (got == count) 
            return requested;
        else {
            chunk += got;
            count -= got;
        }
    }
    return requested - count;
}

static void _init_buffers(SmdReader* self) {
    for (int i=0; i<self->nfiles; i++) {
        self->bufs[i].chunk = (char *)malloc(CHUNKSIZE);
        self->bufs[i].got = _read_with_retries(self, i, 0, CHUNKSIZE);
        self->bufs[i].offset = 0;
        self->bufs[i].prev_offset = 0;
        self->bufs[i].nevents = 0;
        self->bufs[i].timestamp = 0;
        self->bufs[i].block_offset = 0;
        self->bufs[i].block_size = 0;
    }
}
