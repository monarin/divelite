Note for SLURM

Job/steps/tasks  
We submit a job using sbatch. Each job contains steps (each is like: running srun echo "hello") that uses tasks (no. of cpus).  

1. Running srun with & (running in the background) works on s3df but not on srcf.
2. If one step dies (exit 1/0), what happen?
3. Check job step log file
4. Can we use squeue/scontrol to check job step details?
5. Can we start/cancel individual steps?
6A. [DREAM] For srun, can we remove the nodelist and specify resource?
Example: Ask for 1 gpu? Ask for 2 timings? 
6B. [DREAM] Can we switch the BOS connection when the resources are allocated?



