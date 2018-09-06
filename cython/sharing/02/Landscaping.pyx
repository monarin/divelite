cimport Shrubbing
import Shrubbing

cdef Shrubbing.Shrubbery sh
sh = Shrubbing.standard_shrubbery()
print("Shrubbery size is %d x %d" % (sh.width, sh.length))
