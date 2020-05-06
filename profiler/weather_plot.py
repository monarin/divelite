import sys
import numpy as np
import matplotlib.pyplot as plt

log_fname = sys.argv[1]
size = int(sys.argv[2])

data = {}
with open(log_fname) as f:
    for line in f:
        cols = line.split()
        if len(cols) == 2:
            try:
                rank = int(cols[0])
                ts = float(cols[1])
                if rank not in data:
                    data[rank] = [ts]
                else:
                    data[rank].append(ts)

            except:
                print(f'unexpected two columns data: {line}')
                pass
deltas = []
for rank, ts_list in data.items():
    min_ts=min(ts_list)
    max_ts=max(ts_list)
    deltas.append(len(ts_list))

deltas = np.asarray(deltas)
plt.hist(deltas, bins=100)
thres = np.average(deltas) + ( np.std(deltas) )
plt.title(f"No. points more than {thres:.2f} s: {len(deltas[deltas>thres]):d}  avg={np.average(deltas):.2f} max={np.max(deltas):.2f} min={np.min(deltas):.2f}")
plt.show()

deltas = []
for rank, ts_list in data.items():
    if rank < 2000:
        plt.scatter([rank]*len(ts_list), ts_list, s=2, marker='o')
    # calculate delta
    ts_arr = np.asarray(ts_list)
    deltas.extend(list(ts_list - np.roll(ts_list, 1))[1:])

plt.show()

# plot histogram of deltas
deltas = np.asarray(deltas)
plt.hist(deltas, bins=100)
thres = np.average(deltas) + ( np.std(deltas) )
plt.title(f"No. points more than {thres:.2f} s: {len(deltas[deltas>thres]):d}  avg={np.average(deltas):.2f} max={np.max(deltas):.2f} min={np.min(deltas):.2f}")
plt.show()
