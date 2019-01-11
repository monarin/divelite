import sys
import numpy as np

log_file = sys.argv[1]
n_files = int(sys.argv[2])

fds = [0]*n_files
cn_file = 0
ts = {}

lustre_dir = "/global/cscratch1/sd/monarin/testxtc2/hsd/smalldata"
bb_dir = "/var/opt/cray/dws/mounts/batch/psana2_hsd_16718487_striped_scratch/hsd/smalldata"

with open(sys.argv[1], "r") as f:
    for data in f:
        if data.find('open("%s'%bb_dir) > 0:
            fds[cn_file] = int(data.split()[5])
            cn_file += 1

        if cn_file == n_files: break
    
    for fd in fds:
        ts[fd] = []

    for data in f:
        for fd in fds:
            if data.find('read(%d'%fd) > 0 and data.find('..., 52) = 52') > 0 :
                ts[fd].append(data.split()[1])
            elif data.find('read(%d'%fd) > 0 and data.find('..., 2104) = 2104') > 0:
                ts[fd].append(data.split()[1])
            elif data.find('read(%d,  <unfinished ...>'%fd) > 0:
                if len(ts[fd]) < 5:
                    ts[fd].append(data.split()[1])
        
        flag_stop = False
        for key, val in ts.iteritems():
            if len(val) == 6: 
                flag_stop = True
        if flag_stop:
            break


for key, val in ts.iteritems():
    print('%d %s'%(key, ' '.join(val)))


