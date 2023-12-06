#!/bin/bash
#SBATCH --partition=milano
#SBATCH --account=lcls:data
#SBATCH --job-name=test-psana2-live
#SBATCH --output=output-%j.txt
#SBATCH --error=output-%j.txt
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --time=1:00:00


t_start=`date +%s`


mpirun -np 10 python gen_h5.py


t_end=`date +%s`
echo PSJobCompleted TotalElapsed $((t_end-t_start)) 
