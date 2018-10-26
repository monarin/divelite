from distutils.core import setup, Extension
setup(name="smdreader", version="1.0",
      ext_modules=[Extension("smdreader", ["smdreader.cc"])])

