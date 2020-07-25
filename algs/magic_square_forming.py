#!/bin/python3

import math
import os
import random
import re
import sys

# calculate costs for all given combinations of positions and values
def calc_costs(s, pos_combos, val_combos):
    result = {}
    for pos_combo in pos_combos:
        for val_combo in val_combos:
            s_selected = [s[indices[0]][indices[1]] for indices in pos_combo]
            dif = sum([abs(s_selected[i] - val_combo[i]) for i in range(len(val_combo))])
            
            result[(pos_combo, val_combo)] = dif
    
    print(result)
    return result

# Complete the formingMagicSquare function below.
def formingMagicSquare(s):
    magics = [[8,3,4], [1,5,9], [6,7,2]]
    cost = 0
    
    # calculate all possible costs for 1,5,9
    pos_combos_a = [([0,1], [1,1], [2,1]), ([1,0], [1,1], [1,2]) ]
    val_combos_a = [[1,5,9], [9,5,1]]
    result_a = calc_costs(s, pos_combos_a, val_combos_a)

    # calculate all possible costs for 8,3,4
    for pos_combo_a in pos_combos_a:
    if pos_como_a == ([0,1], [1,1], [2,1]):
        # column base
        pos_combos_b = [([0,0],[1,0],[2,0]), ([0,2],[1,2],[2,2])]
    else:
        pos_combos = [([0,0],[0,1],[0,2]), ([2,0],[2,1],[2,2])]

    if result_val[0] == 9:
        val_combos =[[4,3,8]]
    else:
        val_combos = [[8,3,4]]
             
    result_pos, result_val, min_dif = locate(s, pos_combos, val_combos)
    cost += min_dif

    # Locate best positions for 2,7,6
    if result_val[0] == 4:
        val_combos =[[2,7,6]]
    else:  
        val_combos =[[6,7,2]]

    if result_pos == ([0,0],[1,0],[2,0]):
        pos_combos = [([0,2],[1,2],[2,2])]
    elif result_pos == ([0,2],[1,2],[2,2]):
        pos_combos = [([0,0],[1,0],[2,0])]
    elif result_pos == ([0,0],[0,1],[0,2]):
        pos_combos = [([2,0],[2,1],[2,2])]
    else:
        pos_combos = [([0,0],[0,1],[0,2])]

    result_pos, result_val, min_dif = locate(s, pos_combos, val_combos)
    cost += min_dif
    return cost

    

if __name__ == '__main__':

    s = [[4,5,8],[2,4,1],[1,9,7]]

    result = formingMagicSquare(s)
    print(result)


