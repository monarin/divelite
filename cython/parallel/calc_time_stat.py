import sys
import numpy as np

a=[]
with open(sys.argv[1], 'r') as f:
    for line in f:
        cols = line.split()
        if len(cols) == 4 or len(cols) == 3:
            a.append(float(cols[2]))
a=np.asarray(a)
a*=1e-3 # convert to milliseconds
print(f'avg={np.average(a):.4f} max={np.max(a):.4f} min={np.min(a):.4f} std={np.std(a):.4f}')
