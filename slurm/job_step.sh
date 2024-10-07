#!/bin/bash

#SBATCH --account=lcls:data
#SBATCH --partition=milano  ## the partitions to run in (comma seperated)
#SBATCH --job-name parallel   ## name that will show up in the queue
#SBATCH --output slurm-%j.out   ## filename of the output; the %j is equal to jobID; default is slurm-[jobID].out
#SBATCH --ntasks=4  ## number of tasks (analyses) to run
#SBATCH --ntasks-per-node=2
#SBATCH --cpus-per-task=2  ## the number of threads allocated to each task
#SBATCH --nodelist=sdfmilan[048-049]
#SBATCH --mem-per-cpu=1G   # memory per CPU core
#SBATCH --time=0-00:10:00  ## time for analysis (day-hour:min:sec)

# Execute job steps
srun --ntasks=1 --nodes=1 --cpus-per-task=$SLURM_CPUS_PER_TASK --job-name hello1 bash -c "sleep 2; echo 'hello 1 $HOSTNAME'" &
srun --ntasks=1 --nodes=1 --cpus-per-task=$SLURM_CPUS_PER_TASK --job-name hello2 bash -c "sleep 4; echo 'hello 2 $HOSTNAME'" &
srun --ntasks=1 --nodes=1 --cpus-per-task=$SLURM_CPUS_PER_TASK --job-name hello3 bash -c "sleep 8; echo 'hello 3 $HOSTNAME'" &
wait

