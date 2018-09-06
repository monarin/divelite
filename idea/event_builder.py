import numpy as np

#data = np.array([[3,6,9], range(1,10), [2,3,5,6,8,9]])
#data=np.array([range(1,10), range(1,10), range(1,10)])
#data = np.array([[3,6], range(1,10), [2,3,5,6,8,9]])
data = np.array([[1,2,3,4],[1,2,3,5],[1,2,4,6]])
data_sizes = np.array([len(d) for d in data])
indices = np.array([0, 0, 0])
requested = 9
got = 0

while got < requested and (indices < data_sizes).any():
    timestamps = np.zeros(len(data), dtype='i')
    for i, d in enumerate(data):
        if indices[i] < data_sizes[i]:
            timestamps[i] = d[indices[i]]

    sorted_det_id = np.argsort(timestamps)
    for det_id in sorted_det_id:
        if timestamps[det_id] == 0:
            continue

        evt = np.zeros(len(data), dtype='i')
        evt[det_id] = timestamps[det_id]
        indices[det_id] += 1
        for i, d in enumerate(data):
            if i == det_id or indices[i] >= data_sizes[i]: 
                continue
            
            while d[indices[i]] <= evt[det_id]:
                evt[i] = d[indices[i]]
                timestamps[i] = 0
                indices[i] +=1

                if indices[i] == data_sizes[i]:
                    break

        got += 1
        print('got', got, 'evt', evt)
        if got == requested:
            break



