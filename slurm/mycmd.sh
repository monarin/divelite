#!/bin/bash

echo arg: ${1} SLURM_ARRAY_TASK_ID: $SLURM_ARRAY_TASK_ID SLURM_ARRAY_JOB_ID: $SLURM_ARRAY_JOB_ID $HOSTNAME

if [ $SLURM_ARRAY_TASK_ID -eq 1 ]; then
    drp -P tst -C drp-srcf-cmp035 -M /cds/group/psdm/psdatmgr/etc/config/prom/tst -d /dev/datadev_1 -o /cds/data/drpsrcf -k batching=yes,directIO=yes -l 0x1 -D ts -u timing_0 -p 4

elif [ $SLURM_ARRAY_TASK_ID -eq 2 ]; then
    teb -P tst -C drp-srcf-cmp035 -M /cds/group/psdm/psdatmgr/etc/config/prom/tst -k script_path=/cds/home/c/claus/lclsii/daq/runs/eb/data/srcf -u teb0 -p 4

elif [ $SLURM_ARRAY_TASK_ID -eq 3 ]; then
    control -P tst -B DAQ:NEH -x 0 -C BEAM --user tstopr --url https://pswww.slac.stanford.edu/ws-auth/lgbk/ -d https://pswww.slac.stanford.edu/ws-auth/configdb/ws/configDB -t trigger -S 1 -T 20000 -V /cds/group/pcds/dist/pds/tst/misc/elog_tst.txt -u control -p 4
fi
