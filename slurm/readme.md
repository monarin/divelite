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

### slurmrestd
Installation:
Check version of slurm (the version no. for the rpm must match)
```
monarin@psslurm-drp tmp rpm -qa | grep slurm
slurm-libs-20.11.9-1.el7.x86_64
...
```
Download the rpm (on node with internet/ RPMFind.net):
```
wget https://rpmfind.net/linux/epel/7/x86_64/Packages/s/slurm-slurmrestd-20.11.9-1.el7.x86_64.rpm
```
Install the prerequisites and the downloaded rpm (on psslurm-drp):
```
sudo yum install http-parser-devel json-c-devel libjwt-devel libyaml-devel
sudo yum install slurm-slurmrestd-20.11.9-1.el7.x86_64.rpm
```
Useful links:
https://kb.brightcomputing.com/knowledge-base/installing-and-operating-slurmrestd/#setting-up-jwt-authentication

### configless setup
On control node (ex. psslurm-drp), add the following line to /etc/slurm/slurm.conf and restart the slurmctld.
```
SlurmctldParameters=enable_configless
```
On client nodes, restart slurmd with --conf-server option:
```
slurmd --conf-server psslurm-drp:6817
```
Note that 6817 is the default port and can be omitted if left unchange in slurm.conf.  
IMPORTANT: You must remove $SLURM_CONF environment variable on the client nodes. This takes priority over --conf-server and can
cause unexpected behaviours.


