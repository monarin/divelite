#!/bin/bash
PS_SMD_NODES=10 mpirun -f hosts -n 111 python test_bd.py 1000000
