#!/bin/bash -l

export OMP_PROC_BIND=true
export OMP_PLACES=threads

# Asking for 2 MPI tasks per node (each has 8 threads)
export OMP_NUM_THREADS=8
echo "2 MPI tasks per node (unpacked)"
srun -N 2 -n 4 -c 32 shifter python test_mpi.py

echo "4 MPI tasks per node (fully packed)"
srun -N 2 -n 8 -c 16 shifter python test_mpi.py

echo "4 MPI tasks per node (with hyperthreading)"
export OMP_NUM_THREADS=16
srun -N 2 -n 8 -c 16 shifter python test_mpi.py


# Running parallel jobs simultaneously
echo "Running parallel jobs simultaneously."
export OMP_NUM_THREADS=""
export OMP_PROC_BIND=""
export OMP_PLACES=""
srun -N 1 -n 22 -c 2 --cpu_bind=cores shifter python test_mpi.py &
srun -N 2 -n 54 -c 2 --cpu_bind=cores shifter python test_mpi.py &
srun -N 1 -n 20 -c 3 --cpu_bind=cores shifter python test_mpi.py &
wait


