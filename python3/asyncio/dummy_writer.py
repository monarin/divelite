#!/usr/bin/env python

from time import sleep

with open('dummy.txt', 'w') as f:
    for i in range(1000000):
        f.write('%d\n'%i)

    if i % 10 == 0:
        sleep(2)


