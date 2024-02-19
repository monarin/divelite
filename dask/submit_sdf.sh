#!/bin/bash
#SBATCH --partition=milano
#SBATCH --account=lcls:data
#SBATCH --job-name=test-psana2-ts-sort
#SBATCH --output=output-%j.txt
#SBATCH --error=output-%j.txt
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --time=00:10:00


t_start=`date +%s`


python -u parallel_h5_w_dask_dataframe.py


t_end=`date +%s`
echo PSJobCompleted TotalElapsed $((t_end-t_start)) 
