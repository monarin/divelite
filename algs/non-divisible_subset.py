import math
import os
import random
import re
import sys

#
# Complete the 'nonDivisibleSubset' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. INTEGER k
#  2. INTEGER_ARRAY s
#

def nonDivisibleSubset(k, s):
    # Write your code here
    
    # Create an exclude dict
    excl = {}
    excl_sizes = [0] * len(s)
    for i in range(len(s)):
        excl[i] = []
        for j in range(len(s)):
            if i == j: continue
            if (s[i] + s[j]) % k == 0:
                excl[i].append(s[j])
        excl_sizes[i] = len(excl[i])
    
    for s_id, excludes in excl.items():
        print(s_id, s[s_id], excludes, excl_sizes[s_id])

    # Build s' for each starting point 
    s_p = [0] * len(s) 
    for s_id, excludes in excl.items():
        s_p[s_id] = 1
        includes = [s[s_id]]
        for j in range(len(s)):
            if s_id == j: continue
            if s[j] not in excludes:
                s_p[s_id] += 1
                includes.append(s[j])
                for x in excl[j]:
                    if x not in excludes:
                        excludes.append(x)
                print(f's_p[{s_id}]={s_p[s_id]} includes={includes} excludes={excludes}')
    
    print(f'max non-divisible set size = {max(s_p)}')
    return max(s_p)

if __name__ == '__main__':
    
    #n = 15 
    #k = 7
    #s_str = "278 576 496 727 410 124 338 149 209 702 282 718 771 575 436"
    
    n = 10
    k = 5
    s_str ="770528134 663501748 384261537 800309024 103668401 538539662 385488901 101262949 557792122 46058493"
    s = list(map(int, s_str.split()))

    result = nonDivisibleSubset(k, s)

    print(result)
