#!/bin/bash

pid=${1}
log="${pid}.log"

#fds=($(grep 'open("/reg/d/psdm/xpp' $log | awk '{print $6}'))
fds=($(grep 'open("/ffb01/monarin/hsd/smalldata' $log | awk '{print $6}'))

fds=(32 33 34 35 36 37 38 39 40 41 42)
for i in "${fds[@]}"
do
    t1=`grep -m1 read\(${i} $log | awk '{print $2}'`
    t2=`grep -m2 read\(${i} $log | grep -v ${t1} | awk '{print $2}'`
    t3=`grep -m3 read\(${i} $log | grep -v ${t1} | grep -v ${t2} | awk '{print $2}'`
    t4=`grep -m4 read\(${i} $log | grep -v ${t1} | grep -v ${t2} | grep -v ${t3} | awk '{print $2}'`
    echo $i $t1 $t2 $t3 $t4
done
