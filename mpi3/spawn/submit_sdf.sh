#!/bin/bash
#SBATCH --partition=milano
#SBATCH --account=lcls:data
#SBATCH --job-name=test-psana2-ts-sort
#SBATCH --output=output-%j.txt
#SBATCH --error=output-%j.txt
#SBATCH --nodes=2
#SBATCH --exclusive
#SBATCH --time=00:30:00


t_start=`date +%s`


mpirun -np 1 python t1.py 


t_end=`date +%s`
echo PSJobCompleted TotalElapsed $((t_end-t_start)) 
