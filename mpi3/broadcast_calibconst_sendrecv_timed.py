#!/usr/bin/env python3
from mpi4py import MPI
import numpy as np
import pickle, os, mmap, time

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Split per node
node_comm = comm.Split_type(MPI.COMM_TYPE_SHARED)
node_rank = node_comm.Get_rank()
is_node_leader = node_rank == 0
node_name = MPI.Get_processor_name()

node_comm.Barrier()
t_total_start = MPI.Wtime()

# ---------------------------------------------------------------------
# Step 1. Rank 0 loads sbcast’ed file
# ---------------------------------------------------------------------
t0 = MPI.Wtime()
src_file = "/sdf/home/m/monarin/tmp/calibconst.pkl"
if rank == 0:
    if not os.path.exists(src_file):
        raise FileNotFoundError(src_file)
    with open(src_file, "rb") as f:
        data_bytes = f.read()
    data_size = len(data_bytes)
else:
    data_bytes = None
    data_size = 0
t_load = MPI.Wtime() - t0

# ---------------------------------------------------------------------
# Step 2. Gather node-leader world ranks and distribute to them only
# ---------------------------------------------------------------------
t0 = MPI.Wtime()

# Each node leader shares its world rank
local_leader_rank = rank if is_node_leader else MPI.PROC_NULL
leaders = comm.allgather(local_leader_rank)
node_leaders = [r for r in leaders if r != MPI.PROC_NULL]
num_nodes = len(node_leaders)

if rank == 0:
    print(f"[Rank 0] Detected {num_nodes} node leaders: {node_leaders}")

# Tell everyone the size
data_size = comm.bcast(data_size, root=0)

# Only rank 0 sends to node leaders (skip itself)
if rank == 0:
    for dest in node_leaders:
        if dest == 0:
            continue
        comm.send(data_bytes, dest=dest, tag=100)
else:
    if is_node_leader:
        data_bytes = comm.recv(source=0, tag=100)

# Each node leader now shares within its node
data_bytes = node_comm.bcast(data_bytes, root=0)
t_sendrecv = MPI.Wtime() - t0

# ---------------------------------------------------------------------
# Step 3. Node leader writes atomically
# ---------------------------------------------------------------------
t0 = MPI.Wtime()
dest_file = "/dev/shm/calibconst.pkl"
temp_file = dest_file + ".inprogress"
if is_node_leader:
    if os.path.exists(temp_file):
        os.remove(temp_file)
    with open(temp_file, "wb") as f:
        f.write(data_bytes)
        f.flush()
        os.fsync(f.fileno())
    os.rename(temp_file, dest_file)
# wait for file visibility
while not os.path.exists(dest_file):
    time.sleep(0.01)
node_comm.Barrier()
t_write_atomic = MPI.Wtime() - t0

# ---------------------------------------------------------------------
# Step 4. All ranks mmap + unpickle
# ---------------------------------------------------------------------
t0 = MPI.Wtime()
with open(dest_file, "rb") as f:
    filesize = os.path.getsize(dest_file)
    mm = mmap.mmap(f.fileno(), length=filesize, access=mmap.ACCESS_READ)
    data_obj = pickle.loads(mm.read(filesize))
mm.close()
t_load_mmap = MPI.Wtime() - t0

# ---------------------------------------------------------------------
# Step 5. Total + print
# ---------------------------------------------------------------------
node_comm.Barrier()
t_total = MPI.Wtime() - t_total_start
if is_node_leader:
    print(
        f"[NodeLeader rank {rank:04d} on {node_name}] "
        f"load={t_load:.3f}s sendrecv={t_sendrecv:.3f}s "
        f"atomic_write={t_write_atomic:.3f}s load_mmap={t_load_mmap:.3f}s "
        f"total={t_total:.3f}s"
    )
if rank == 0:
    print(f"[Rank 0] calibconst object type: {type(data_obj)} total time: {t_total:.3f}s")
