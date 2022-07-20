#define PY_SSIZE_T_CLEAN
#include "Python.h"
#include "fpng.h"

using namespace fpng;

PyObject *py_fpng_cpu_supports_sse41(PyObject *self, PyObject *unused)
{
    PyObject* result = fpng_cpu_supports_sse41() ? Py_True : Py_False;
    Py_INCREF(result);
    return result;
}

PyObject *py_fpng_crc32(PyObject *self, PyObject *args)
{
    const char *pData;
    Py_ssize_t size;
    uint32_t prev_crc32;
    if (!PyArg_ParseTuple(args, "y#i", &pData, &size, &prev_crc32))
    {
        PyErr_SetString(PyExc_ValueError, "Invalid arguments");
        return NULL;
    }
    return PyLong_FromUnsignedLong(fpng_crc32(pData, size, prev_crc32));
}

PyObject *py_fpng_adler32(PyObject *self, PyObject *args)
{
    const char *pData;
    Py_ssize_t size;
    uint32_t adler;
    if (!PyArg_ParseTuple(args, "y#i", &pData, &size, &adler))
    {
        PyErr_SetString(PyExc_ValueError, "Invalid arguments");
        return NULL;
    }
    return PyLong_FromUnsignedLong(fpng_adler32(pData, size, adler));
}

PyObject *py_fpng_encode_image_to_memory(PyObject *self, PyObject *args)
{
    const char *pImage;
    Py_ssize_t size;
    uint32_t w, h;
    uint32_t num_chans = 0;
    uint32_t flags = 0;
    if (!PyArg_ParseTuple(args, "y#II|II", &pImage, &size, &w, &h, &num_chans, &flags))
    {
        PyErr_SetString(PyExc_ValueError, "Invalid arguments");
        return NULL;
    }
    // calculate channels from size, making their input optional
    if (num_chans == 0)
    {
        num_chans = size / (w * h);
    }
    if (num_chans != 3 && num_chans != 4)
    {
        PyErr_SetString(PyExc_ValueError, "Invalid number of channels");
        return NULL;
    }
    if (flags > 2)
    {
        PyErr_SetString(PyExc_ValueError, "Invalid flags");
        return NULL;
    }
    std::vector<uint8_t> out_buf;
    if (!fpng_encode_image_to_memory(pImage, w, h, num_chans, out_buf, flags))
    {
        PyErr_SetString(PyExc_ValueError, "Error encoding image");
        return NULL;
    }
    return PyBytes_FromStringAndSize((char*)out_buf.data(), out_buf.size());
}

PyObject *py_fpng_encode_image_to_file(PyObject *self, PyObject *args)
{
    const char *pImage;
    Py_ssize_t size;
    uint32_t w, h;
    uint32_t num_chans = 0;
    uint32_t flags = 0;
    const char *pFilename;
    if (!PyArg_ParseTuple(args, "sy#II|II", &pFilename, &pImage, &size, &w, &h, &num_chans, &flags))
    {
        PyErr_SetString(PyExc_ValueError, "Invalid arguments");
        return NULL;
    }
    // calculate channels from size, making their input optional
    if (num_chans == 0)
    {
        num_chans = size / (w * h);
    }
    if (num_chans != 3 && num_chans != 4)
    {
        PyErr_SetString(PyExc_ValueError, "Invalid number of channels");
        return NULL;
    }
    if (flags > 2)
    {
        PyErr_SetString(PyExc_ValueError, "Invalid flags");
        return NULL;
    }
    if (!fpng_encode_image_to_file(pFilename, pImage, w, h, num_chans, flags))
    {
        PyErr_SetString(PyExc_ValueError, "Error encoding image");
        return NULL;
    }
    Py_RETURN_NONE;
}

PyObject *py_decode_err(int code)
{
    switch (code)
    {
    case 1:
        PyErr_SetString(PyExc_ValueError, "file is a valid PNG file, but it wasn't written by FPNG so you should try decoding it with a general purpose PNG decoder");
        break;
    case 2:
        PyErr_SetString(PyExc_ValueError, "invalid function parameter");
        break;
    case 3:
        PyErr_SetString(PyExc_ValueError, "file cannot be a PNG file");
        break;
    case 4:
        PyErr_SetString(PyExc_ValueError, "a chunk CRC32 check failed, file is likely corrupted or not PNG");
        break;
    case 5:
        PyErr_SetString(PyExc_ValueError, "invalid image dimensions in IHDR chunk (0 or too large)");
        break;
    case 6:
        PyErr_SetString(PyExc_ValueError, "decoding the file fully into memory would likely require too much memory (only on 32bpp builds)");
        break;
    case 7:
        PyErr_SetString(PyExc_ValueError, "failed while parsing the chunk headers, or file is corrupted");
        break;
    case 8:
        PyErr_SetString(PyExc_ValueError, "IDAT data length is too small and cannot be valid, file is either corrupted or it's a bug");
        break;
    case 9:
        PyErr_SetString(PyExc_ValueError, "file open failed");
        break;
    case 10:
        PyErr_SetString(PyExc_ValueError, "file is too large");
        break;
    case 11:
        PyErr_SetString(PyExc_ValueError, "file read failed");
        break;
    case 12:
        PyErr_SetString(PyExc_ValueError, "file seek failed");
        break;
    default:
        PyErr_SetString(PyExc_ValueError, "unknown error");
        break;
    }
    return NULL;
}

PyObject *py_fpng_get_info(PyObject *self, PyObject *args)
{
    const char *pImage;
    Py_ssize_t size;
    uint32_t w, h, num_chans;
    if (!PyArg_ParseTuple(args, "y#", &pImage, &size))
    {
        PyErr_SetString(PyExc_ValueError, "Invalid arguments");
        return NULL;
    }
    int error = fpng_get_info(pImage, size, w, h, num_chans);
    if (error)
    {
        return py_decode_err(error);
    }
    return Py_BuildValue("III", w, h, num_chans);
}

PyObject *py_fpng_decode_memory(PyObject *self, PyObject *args)
{
    const char *pImage;
    Py_ssize_t image_size;
    uint32_t desired_channels;
    if (!PyArg_ParseTuple(args, "y#I", &pImage, &image_size, &desired_channels))
    {
        PyErr_SetString(PyExc_ValueError, "Invalid arguments");
        return NULL;
    }

    std::vector<uint8_t> out;
    uint32_t width, height, channels_in_file;
    int error = fpng_decode_memory(pImage, image_size, out, width, height, channels_in_file, desired_channels);
    if (error)
        return py_decode_err(error);
    return Py_BuildValue("y#III", (char*)out.data(), out.size(), width, height, channels_in_file);
}

PyObject *py_fpng_decode_file(PyObject *self, PyObject *args)
{
    const char *pFilename;
    uint32_t desired_channels;
    if (!PyArg_ParseTuple(args, "sI", &pFilename, &desired_channels))
    {
        PyErr_SetString(PyExc_ValueError, "Invalid arguments");
        return NULL;
    }
    std::vector<uint8_t> out;
    uint32_t width, height, channels_in_file;
    int error = fpng_decode_file(pFilename, out, width, height, channels_in_file, desired_channels);
    if (error)
        return py_decode_err(error);
    return Py_BuildValue("y#III", (char*)out.data(), out.size(), width, height, channels_in_file);
}

// Exported methods are collected in a table
static struct PyMethodDef method_table[] = {
    {"fpng_cpu_supports_sse41",
     (PyCFunction)py_fpng_cpu_supports_sse41,
     METH_VARARGS,
     ""},
    {"fpng_crc32",
     (PyCFunction)py_fpng_crc32,
     METH_VARARGS,
     ""},
    {"fpng_adler32",
     (PyCFunction)py_fpng_adler32,
     METH_VARARGS,
     ""},
    {"fpng_encode_image_to_memory",
     (PyCFunction)py_fpng_encode_image_to_memory,
     METH_VARARGS,
     ""},
    {"fpng_encode_image_to_file",
     (PyCFunction)py_fpng_encode_image_to_file,
     METH_VARARGS,
     ""},
    {"fpng_decode_from_memory",
     (PyCFunction)py_fpng_decode_memory,
     METH_VARARGS,
     ""},
    {"fpng_decode_from_file",
     (PyCFunction)py_fpng_decode_file,
     METH_VARARGS,
     ""},
    {NULL,
     NULL,
     0,
     NULL} // Sentinel value ending the table
};

// A struct contains the definition of a module
static PyModuleDef fpng_py_module = {
    PyModuleDef_HEAD_INIT,
    "fpng_py._fpng_py", // Module name
    "a python wrapper for fpng",
    -1, // Optional size of the module state memory
    method_table,
    NULL, // Optional slot definitions
    NULL, // Optional traversal function
    NULL, // Optional clear function
    NULL  // Optional module deallocation function
};

// The module init function
PyMODINIT_FUNC PyInit__fpng_py(void)
{
    // init fpng during module initialization
    fpng_init();
    // create & return the module
    return PyModule_Create(&fpng_py_module);
}