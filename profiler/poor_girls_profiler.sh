#!/bin/bash

pid=${1}
log="${pid}.log"

#fds=($(grep 'open("/reg/d/psdm/xpp' $log | awk '{print $6}'))
fds=($(grep 'open("/gpfs/alpine/scratch/monarin/chm137/data/xtcdata/smalldata/data-' $log | awk '{print $6}'))
#fds=($(grep 'open("/reg/d/psdm/xpp/xpptut15/scratch/mona/xtc2/data-r0001-epc.xtc2' $log | awk '{print $6}'))

for i in "${fds[@]}"
do
    t1=`grep -m1 read\(${i} $log | awk '{print $2}'`
    t2=`grep -m2 read\(${i} $log | grep -v ${t1} | awk '{print $2}'`
    t3=`grep -m3 read\(${i} $log | grep -v ${t1} | grep -v ${t2} | awk '{print $2}'`
    t4=`grep -m4 read\(${i} $log | grep -v ${t1} | grep -v ${t2} | grep -v ${t3} | awk '{print $2}'`
    t5=`grep -m5 read\(${i} $log | grep -v ${t1} | grep -v ${t2} | grep -v ${t3} | grep -v ${t4} | awk '{print $2}'`
    echo $i $t1 $t2 $t3 $t4 $t5
    #grep -m1 "read($i, \"\\" $log
done
