#from distutils.core import setup
#from Cython.Build import cythonize
#setup(ext_modules = cythonize(["smdreader.pyx"]))

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

ext_modules = [
    Extension(
        "smdreader",
        ["smdreader.pyx"],
        extra_compile_args=['-fopenmp'],
        extra_link_args=['-fopenmp'],
    )
]

setup(
    name='smdreader-parallel',
    ext_modules=cythonize(ext_modules),
)
