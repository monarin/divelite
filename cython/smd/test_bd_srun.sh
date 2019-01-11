#!/bin/bash -l

export OMP_PROC_BIND=true
export OMP_PLACES=threads

# Asking for 2 MPI tasks per node (each has 16 threads)
export OMP_NUM_THREADS=2
echo "32 MPI tasks per node (unpacked)"
export PS_SMD0_THREADS=32
srun -N 5 -n 160 -c 2 shifter python test_bd.py 1000
