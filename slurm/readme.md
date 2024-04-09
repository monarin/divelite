## Note for SLURM

### slurmctld 
The central management daemon of Slurm. For drpq test partition, this is runninng on psslurm-drp. 
To stop, locate pid and kill it.
```
pgrep slurmctld
kill -9 <pid>
```
To start in foreground with extra verbosity mode, 
```
sudo slurmctld -D [-vvvvv] 
```
or start in background then tail the log file:
```
sudo slurmctld
sudo tail -f /var/log/slurm/slurmctld.log 
```
