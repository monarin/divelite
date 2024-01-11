from mpi4py import MPI
import numpy as np
import h5py
import time


# Get and merge parent comm to get the common comm
comm = MPI.Comm.Get_parent()
common_comm=comm.Merge(True)


# Start receving data
while True:
    common_comm.Send(np.array([common_comm.Get_rank()], dtype='i'), dest=0)
    info = MPI.Status()
    common_comm.Probe(source=0, status=info)
    count = info.Get_elements(MPI.INT64_T)
    if count > 0:
        data = np.empty(count, dtype=np.int64)
        common_comm.Recv(data, source=0)
    else:
        data = bytearray()
        common_comm.Recv(data, source=0)
        break
    tag = info.Get_tag()
    print (f"WRITER RANK:{common_comm.Get_rank()} got {data.shape=} {tag=}")

    # Access the large h5 and slice with the obtained indices
    in_f = h5py.File('/sdf/data/lcls/drpsrcf/ffb/users/monarin/h5/mylargeh5.h5', 'r')
    out_f = h5py.File(f'/sdf/data/lcls/drpsrcf/ffb/users/monarin/h5/output/result_part{tag}.h5', 'w') 
    for key in in_f.keys():
        t0 = time.monotonic()
        in_ds = in_f[key][data]
        t1 = time.monotonic()
        out_f.create_dataset(key, data=in_ds)
        t2 = time.monotonic()
        print(f'WRITER RANK:{common_comm.Get_rank()} {key=} {in_ds.size=} ({in_ds.size*in_ds.itemsize/1e6:.2f}MB) slicing {t1-t0:.2f}s. writing:{t2-t1:.2f}s. total:{t2-t0:.2f}s.')
    in_f.close()
    out_f.close()


print(f"WRITER RANK:{common_comm.Get_rank()} DONE")

