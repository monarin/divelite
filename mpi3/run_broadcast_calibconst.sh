#!/bin/bash
#SBATCH -J bcast_caliconst          # Job name
#SBATCH -N 5                        # Number of nodes
#SBATCH --ntasks-per-node=10        # MPI ranks per node
#SBATCH -t 00:10:00                 # Time limit hh:mm:ss
#SBATCH -p milano                   # Partition/queue name (adjust for your cluster)
#SBATCH -A lcls:data                # Account if required
#SBATCH -o bcast_caliconst_%j.out   # Standard output log
#SBATCH -e bcast_caliconst_%j.err   # Error log

# -- Optional useful info for debugging --
echo "Job started at $(date)"
echo "Running on nodes:"
scontrol show hostnames $SLURM_JOB_NODELIST


# -- Launch MPI job --
echo "Launching MPI job with $SLURM_NTASKS ranks across $SLURM_NNODES nodes..."

# -- Launch bcast job --
echo "Running broadcast_calibconst_shared.py ..."
mpirun -n 50 python broadcast_calibconst_shared.py

# -- Launch send/recv job --
echo "Running sendrecv_calibconst_shared.py ..."
mpirun -n 50 python broadcast_calibconst_sendrecv_timed.py

echo "Job finished at $(date)"
