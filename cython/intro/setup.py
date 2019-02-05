# build with 
# python setup.py build_ext --inplace

from distutils.core import setup
from Cython.Build import cythonize

setup(
    #ext_modules = cythonize("helloworld.pyx")
    #ext_modules = cythonize("fib.pyx")
    ext_modules = cythonize("convert_to_pybytes.pyx")
)
