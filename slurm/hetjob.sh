#!/bin/bash

##SBATCH --partition=milano  
##SBATCH --account=lcls:data
##SBATCH --job-name parallel   ## name that will show up in the queue
#SBATCH --output slurm-%j.out   ## filename of the output; the %j is equal to jobID; default is slurm-[jobID].out
#SBATCH --partition=milano --account=lcls:data --nodelist=sdfmilan001 --ntasks=3
#SBATCH hetjob
#SBATCH --partition=milano --account=lcls:data --nodelist=sdfmilan004 --ntasks=1

set -xe
# Execute job steps
export BLAH="blah"
HETGROUP="--het-group=0 "
srun -n 1 $HETGROUP --exclusive bash -c "sleep 5; echo $BLAH 1" &
srun -n 1 $HETGROUP --exclusive bash -c "sleep 10; echo $BLAH 2" &
srun -n 1 $HETGROUP --exclusive bash -c "sleep 15; echo $BLAH 3" &

HETGROUP="--het-group=1 "
srun -n 1 $HETGROUP --exclusive bash -c "sleep 15; echo $BLAH 4" &
wait

