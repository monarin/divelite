#!/usr/bin/env python3
from mpi4py import MPI
import numpy as np
import pickle
import os
import mmap
import time

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Split per physical node
node_comm = comm.Split_type(MPI.COMM_TYPE_SHARED)
node_rank = node_comm.Get_rank()
is_node_leader = (node_rank == 0)
node_name = MPI.Get_processor_name()

node_comm.Barrier()
t_total_start = MPI.Wtime()

# -----------------------------------------------------------------------------
# Step 1. Rank 0 loads calibration constant data (already sbcast'ed file)
# -----------------------------------------------------------------------------
t0 = MPI.Wtime()
src_file = "/sdf/home/m/monarin/tmp/calibconst.pkl"
if rank == 0:
    if not os.path.exists(src_file):
        raise FileNotFoundError(f"{src_file} not found!")
    with open(src_file, "rb") as f:
        data_bytes = f.read()
    data_size = len(data_bytes)
else:
    data_bytes = None
    data_size = 0
t_load = MPI.Wtime() - t0

# -----------------------------------------------------------------------------
# Step 2. Broadcast file contents to all ranks
# -----------------------------------------------------------------------------
t0 = MPI.Wtime()
data_size = comm.bcast(data_size, root=0)
if rank != 0:
    data_bytes = bytearray(data_size)
comm.Bcast([data_bytes, MPI.BYTE], root=0)
t_bcast = MPI.Wtime() - t0

# -----------------------------------------------------------------------------
# Step 3. Node leader writes atomically via .inprogress -> calibconst.pkl
# -----------------------------------------------------------------------------
t0 = MPI.Wtime()
dest_file = "/dev/shm/calibconst.pkl"
temp_file = dest_file + ".inprogress"

if is_node_leader:
    # Clean up old .inprogress if left behind
    if os.path.exists(temp_file):
        os.remove(temp_file)
    with open(temp_file, "wb") as f:
        f.write(data_bytes)
        f.flush()
        os.fsync(f.fileno())
    # Atomic rename: other ranks will only ever see complete file
    os.rename(temp_file, dest_file)

# Wait for file to exist
while not os.path.exists(dest_file):
    time.sleep(0.01)
node_comm.Barrier()
t_write_atomic = MPI.Wtime() - t0

# -----------------------------------------------------------------------------
# Step 4. All ranks mmap + unpickle the finalized file
# -----------------------------------------------------------------------------
t0 = MPI.Wtime()
with open(dest_file, "rb") as f:
    filesize = os.path.getsize(dest_file)
    mm = mmap.mmap(f.fileno(), length=filesize, access=mmap.ACCESS_READ)
    data_obj = pickle.loads(mm.read(filesize))
mm.close()
t_load_mmap = MPI.Wtime() - t0

# -----------------------------------------------------------------------------
# Step 5. Total timing
# -----------------------------------------------------------------------------
node_comm.Barrier()
t_total = MPI.Wtime() - t_total_start

# -----------------------------------------------------------------------------
# Step 6. Print per-node timing summary
# -----------------------------------------------------------------------------
if is_node_leader:
    print(
        f"[NodeLeader rank {rank:04d} on {node_name}] "
        f"load={t_load:.3f}s "
        f"bcast={t_bcast:.3f}s "
        f"atomic_write={t_write_atomic:.3f}s "
        f"load_mmap={t_load_mmap:.3f}s "
        f"total={t_total:.3f}s"
    )

if rank == 0:
    print(f"[Rank 0] calibconst object type: {type(data_obj)} total time: {t_total:.3f}s")
