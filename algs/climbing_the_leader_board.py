#!/bin/python3

import math
import os
import random
import re
import sys

# Complete the climbingLeaderboard function below.
def climbingLeaderboard(scores, alice):

    # remember ranks for the first (smallest) alice' score
    unique_scores = []
    ranks = []
    a = alice[0]
    cur_rank, cur_score = 1,0
    for i, s in enumerate(scores):
        if i == 0:
            unique_scores.append(s)
            ranks.append(cur_rank)
            cur_score = s
        else:
            if s != cur_score:
                cur_rank += 1
                unique_scores.append(s)
                ranks.append(cur_rank)
                cur_score = s
        
        if s < a:
            break
    
    print('unique_scores')
    print(unique_scores)
    print('rank')
    print(ranks)
    print()
    st = len(unique_scores)-1
    results = [0] * len(alice)
    for i, a in enumerate(alice):
        found = False
        for j in range(st, -1, -1):
            if a <= unique_scores[j]:
                if a < unique_scores[j]:
                    results[i] = ranks[j] + 1
                else:
                    results[i] = ranks[j]
                st = j
                found = True
                break
        
        if not found:
            results[i] = 1
    
    return results
                

if __name__ == '__main__':
    case_no = sys.argv[1]
    with open('output_case_%s.txt'%(case_no), 'r') as f:
        output = list(map(int, [line.rstrip() for line in f]))

    with open('test_case_%s.txt'%(case_no), 'r') as f:
        line = f.readline()
        scores_count = int(line.rstrip())
        line = f.readline()
        scores = list(map(int, line.rstrip().split()))
        print('scores')
        print(scores)
        print()
        line = f.readline()
        alice_count = int(line.rstrip())
        line = f.readline()
        alice = list(map(int, line.rstrip().split()))
        print('alice')
        print(alice)
        print()

        result = climbingLeaderboard(scores, alice)

    print('items not matching with correct output')
    print('item# | correct output | computed output')
    for i, (o, r) in enumerate(zip(output, result)):
        if o != r:
            print(i, o, r)


