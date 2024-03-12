#!/bin/bash

#SBATCH --job-name=array
#SBATCH --array=1-3
#SBATCH --time=01:00:00
#SBATCH --partition=anaq
#SBATCH --nodelist=drp-srcf-cmp035
#SBATCH --ntasks=1
#SBATCH --mem=1G
#SBATCH --output=array_%A-%a.out

# Print the task id.
srun bash -c "./mycmd.sh $SLURM_ARRAY_TASK_ID"

