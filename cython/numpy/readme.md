To compile manually:

# compile cython code to get .c code (use -a for html file)
cython compute_cy.pyx

# compile c code (Python.h file path is in the currect conda include env)
gcc -shared -pthread -fPIC -fwrapv -O2 -Wall -fno-strict-aliasing -I/reg/g/psdm/sw/conda2/inst/envs/ps-2.0.5/include/python3.7m -o compute_cy.so compute_cy.c



