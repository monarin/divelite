import sys
import numpy as np
import matplotlib.pyplot as plt

log_fname = sys.argv[1]
lite = True

data = {}
cn_ts = 0
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
                cn_ts += 1
            except:
                print(f'unexpected two columns data: {line}')
                pass


# Clean up data by excluding ranks that ran for more than 10 mins
# Also collect the first timestamp of each rank so we can sort
# and display it according to the time order (and not the rank order)
deltas = []
first_ts = []
ranks = []
print(f'#ts={cn_ts}')
excluded_ranks = []
for rank, ts_list in data.items():
    min_ts=min(ts_list)
    max_ts=max(ts_list)

    if max_ts - min_ts > 600: # each rank should not run for more than n seconds
        excluded_ranks.append(rank)
    else:
        deltas.append(len(ts_list))


    if len(ts_list) > 0:
        first_ts.append(ts_list[0])
        ranks.append(rank)

sorted_indices = np.argsort(first_ts)
sorted_ranks = [ranks[i] for i in sorted_indices]

print(f'excluded ranks={excluded_ranks}')


# Display average processing time
if not lite:
    deltas = np.asarray(deltas)
    plt.hist(deltas, bins=100)
    thres = np.average(deltas) + ( np.std(deltas) )
    plt.title(f"#Evt per rank. avg={np.average(deltas):.2f} max={np.max(deltas):.2f} min={np.min(deltas):.2f}")
    plt.show()


# Display weather plot according to the first ts
deltas = []
for rank in sorted_ranks:
    ts_list = data[rank]
    if rank not in excluded_ranks:
        plt.scatter([rank]*len(ts_list), ts_list, s=2, marker='o')
        # calculate delta
        ts_arr = np.asarray(ts_list)
        deltas.extend(list(ts_list - np.roll(ts_list, 1))[1:])

plt.title('Weather plot')
plt.show()


# Plot histogram of deltas
if not lite:
    deltas = np.asarray(deltas)
    plt.hist(deltas, bins=100)
    thres = np.average(deltas) + ( np.std(deltas) )
    plt.title(f"Reading time (s) per evt. #points more than {thres:.2f} (s): {len(deltas[deltas>thres]):d}  avg={np.average(deltas):.2f} max={np.max(deltas):.2f} min={np.min(deltas):.2f}")
    plt.show()
