#python setup.py build_ext --inplace

from distutils.core import setup, Extension
from Cython.Build import cythonize

setup(ext_modules = cythonize(Extension(
            "mypybuffer",                
            sources=["mypybuffer.pyx"],    
      )))
