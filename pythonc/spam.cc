#include <Python.h>

static PyObject *SpamError; // Custom error

static PyObject *
spam_system(PyObject *self, PyObject *args)
{
    const char *command;
    int sts;

    if (!PyArg_ParseTuple(args, "s", &command))
        return NULL;
    sts = system(command);
    if (sts < 0) {
        PyErr_SetString(SpamError, "Systemm command failed");
        return NULL;
    }
    return PyLong_FromLong(sts);
}

// method table
static PyMethodDef SpamMethods[] = {
    {"system", spam_system, METH_VARARGS,
        "Execute a shell command."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef spammodule = {
    PyModuleDef_HEAD_INIT,
    "spam",     /* name of module */
    NULL,   /* module documentation, may be NULL */
    -1,         /* size of per-interpreter state of the module,
                   or -1 if the module keeps state in global variables. */
    SpamMethods
};


PyMODINIT_FUNC 
PyInit_Spam(void)
{
    PyObject *m;

    m = PyModule_Create(&spammodule);
    if (m == NULL)
        return NULL;

    SpamError = PyErr_NewException("spam.error", NULL, NULL);
    Py_INCREF(SpamError);
    PyModule_AddObject(m, "error", SpamError);
    return m;
}

PyMODINIT_FUNC
PyInit_spam(void)
{
    return PyModule_Create(&spammodule);
}

int
main(int argc, char *argv[])
{
    wchar_t *program = Py_DecodeLocale(argv[0], NULL);
    if (program == NULL) {
        fprintf(stderr, "Fatal error: cannot decode argv[0]\n");
        exit(1);
    }

    /* Add a built-in module, before Py_Initialize */
    PyImport_AppendInittab("spam", PyInit_spam);

    /* Pass argv[0] to the Python intepreter */
    Py_SetProgramName(program);

    /* Initialize the Python Interpreter. Required. */
    Py_Initialize();

    /* Optionally import the module; alternatively,
     * import can be deferred until the embedded script
     * imports it. */
    PyImport_ImportModule("spam");

    PyMem_RawFree(program);
    return 0;
}
