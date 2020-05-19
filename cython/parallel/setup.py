from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

ext_modules = [
        Extension(
            "ex_prange",
            ["ex_prange.pyx"],
            extra_compile_args=['-fopenmp'],
            extra_link_args=['-fopenmp'],
            )
        ]

"""
ext_modules = [
        Extension(
            "ex_prange",
            ["ex_prange.pyx"],
            extra_compile_args=['-fopenmp'],
            extra_link_args=['-fopenmp'],
            ),
        Extension(
            "ex_parallel",
            ["ex_parallel.pyx"],
            extra_compile_args=['-fopenmp'],
            extra_link_args=['-fopenmp'],
            ),
        Extension(
            "parallel_reader",
            ["parallel_reader.pyx"],
            extra_compile_args=['-fopenmp'],
            extra_link_args=['-fopenmp'],
            ),
        Extension(
            "smdreader",
            ["smdreader.pyx"],
            extra_compile_args=['-fopenmp'],
            extra_link_args=['-fopenmp'],
            ),
        Extension(
            "multi_tasking",
            ["multi_tasking.pyx"],
            extra_compile_args=['-fopenmp'],
            extra_link_args=['-fopenmp'],
            )
        ]
"""

setup(
        name='example-parallel',
        ext_modules=cythonize(ext_modules),
        )
