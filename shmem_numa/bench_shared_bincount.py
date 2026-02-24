#!/usr/bin/env python3
import argparse
import os
import time
from glob import glob

import numpy as np
from mpi4py import MPI

try:
    import psutil
except Exception:
    psutil = None


def parse_cpulist(s):
    cpus = []
    for part in s.split(','):
        part = part.strip()
        if not part:
            continue
        if '-' in part:
            a, b = part.split('-', 1)
            cpus.extend(range(int(a), int(b) + 1))
        else:
            cpus.append(int(part))
    return cpus


def build_cpu_to_numa():
    cpu_to_numa = {}
    node_paths = sorted(glob('/sys/devices/system/node/node*/cpulist'))
    for path in node_paths:
        node_str = path.split('node')[-1].split('/')[0]
        try:
            node_id = int(node_str)
        except ValueError:
            continue
        with open(path, 'r') as f:
            cpus = parse_cpulist(f.read().strip())
        for cpu in cpus:
            cpu_to_numa[cpu] = node_id
    return cpu_to_numa


def get_cpu_id():
    if hasattr(os, "sched_getcpu"):
        try:
            return os.sched_getcpu()
        except Exception:
            pass
    if psutil is not None:
        try:
            return psutil.Process().cpu_num()
        except Exception:
            pass
    # Fallback: parse /proc/self/stat (CPU field is #39, 0-based index 38)
    try:
        with open("/proc/self/stat", "r") as f:
            parts = f.read().split()
        return int(parts[38])
    except Exception:
        return -1


def alloc_shared(node_comm, shape, dtype, name):
    dtype = np.dtype(dtype)
    nbytes = int(np.prod(shape)) * dtype.itemsize
    if node_comm.Get_rank() == 0:
        alloc_bytes = nbytes
    else:
        alloc_bytes = 0
    win = MPI.Win.Allocate_shared(alloc_bytes, dtype.itemsize, comm=node_comm)
    buf, itemsize = win.Shared_query(0)
    if itemsize != dtype.itemsize:
        raise RuntimeError(
            f"Shared_query itemsize mismatch for {name}: {itemsize} vs {dtype.itemsize}"
        )
    arr = np.ndarray(buffer=buf, dtype=dtype, shape=shape)
    return arr, win


def fill_shared_arrays(rank, shared_rank, cake_idxs, correction, bins, seed):
    if shared_rank != 0:
        return
    rng = np.random.default_rng(seed + rank)
    # Cake indices: int64 in [0, bins)
    cake_idxs[:] = rng.integers(0, bins, size=cake_idxs.shape, dtype=np.int64)
    # Correction array (float32 by default)
    correction[:] = rng.random(size=correction.shape, dtype=correction.dtype) + 1.0


def make_local_img(rank, shape, dtype, seed):
    rng = np.random.default_rng(seed + rank)
    return rng.standard_normal(size=shape, dtype=np.dtype(dtype))


def run_bincount(cake_idxs, rank, img_len, img_dtype, img_seed, correction, bins, iters, warmup):
    # Warmup
    for _ in range(warmup):
        # Per-rank local image (simulates per-event det.raw.calib output)
        img_local = make_local_img(rank, (img_len,), img_dtype, img_seed)
        weights = img_local / correction
        np.bincount(cake_idxs, weights=weights, minlength=bins)

    times = []
    for _ in range(iters):
        # Per-rank local image (simulates per-event det.raw.calib output)
        img_local = make_local_img(rank, (img_len,), img_dtype, img_seed)

        t0 = time.perf_counter()
        weights = img_local / correction
        np.bincount(cake_idxs, weights=weights, minlength=bins)
        t1 = time.perf_counter()
        times.append(t1 - t0)
    return times


def summarize(comm, label, times):
    rank = comm.Get_rank()
    all_times = comm.gather(times, root=0)
    if rank != 0:
        return
    flat = [t for rank_times in all_times for t in rank_times]
    if not flat:
        print(f"{label}: no data")
        return
    avg = float(np.mean(flat))
    vmin = float(np.min(flat))
    vmax = float(np.max(flat))
    std = float(np.std(flat))
    print(f"{label} avg/min/max/std: {avg:.6f} {vmin:.6f} {vmax:.6f} {std:.6f}")


def main():
    parser = argparse.ArgumentParser(
        description="Shared-memory np.bincount benchmark (MPI shared memory)."
    )
    parser.add_argument("--n", type=int, default=16_765_786, help="Number of pixels")
    parser.add_argument("--nphi", type=int, default=11, help="nphi")
    parser.add_argument("--nq", type=int, default=169, help="nq")
    parser.add_argument(
        "--dtype",
        default="float32",
        choices=["float32", "float64"],
        help="dtype for img/correction",
    )
    parser.add_argument("--iters", type=int, default=5, help="Measured iterations")
    parser.add_argument("--warmup", type=int, default=2, help="Warmup iterations")
    parser.add_argument(
        "--local-copy",
        action="store_true",
        help="Make per-rank local copies of shared arrays (simulates per-rank cache).",
    )
    parser.add_argument(
        "--per-numa",
        action="store_true",
        help="Split node_comm by NUMA and allocate one shared region per NUMA domain.",
    )
    parser.add_argument("--seed", type=int, default=1234)
    args = parser.parse_args()

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    node_comm = comm.Split_type(MPI.COMM_TYPE_SHARED, 0, MPI.INFO_NULL)
    node_rank = node_comm.Get_rank()
    node_size = node_comm.Get_size()

    bins = args.nphi * args.nq

    if rank == 0:
        print(f"MPI ranks: {size}")
    if node_rank == 0:
        host = MPI.Get_processor_name()
    else:
        host = None
    host = node_comm.bcast(host, root=0)
    if rank == 0:
        print(f"Node leader host: {host} (node_comm size={node_size})")

    numa_id = -1
    if args.per_numa:
        cpu = get_cpu_id()
        cpu_to_numa = build_cpu_to_numa()
        numa_id = cpu_to_numa.get(cpu, -1)

    if args.per_numa and numa_id >= 0:
        shared_comm = node_comm.Split(color=numa_id, key=node_rank)
        shared_rank = shared_comm.Get_rank()
        shared_size = shared_comm.Get_size()
        if shared_rank == 0:
            print(
                f"NUMA leader: rank {rank} host {host} numa {numa_id} "
                f"(numa_comm size={shared_size})"
            )
        shared_scope = f"numa {numa_id}"
    else:
        shared_comm = node_comm
        shared_rank = node_rank
        shared_size = node_size
        shared_scope = "node"
        if args.per_numa and rank == 0:
            print("WARNING: NUMA id not found; falling back to node_comm")

    # Shared arrays (node/NUMA-local)
    cake_idxs, win_idxs = alloc_shared(shared_comm, (args.n,), np.int64, "cake_idxs")
    correction, win_corr = alloc_shared(shared_comm, (args.n,), args.dtype, "correction")

    fill_shared_arrays(rank, shared_rank, cake_idxs, correction, bins, args.seed)
    shared_comm.Barrier()

    if args.local_copy:
        # per-rank local copies (NUMA-local if ranks are pinned)
        cake_idxs_local = np.array(cake_idxs, copy=True)
        correction_local = np.array(correction, copy=True)
        target = "local-copy"
    else:
        cake_idxs_local = cake_idxs
        correction_local = correction
        target = "shared"

    if rank == 0:
        print(f"Mode: {target} (img is per-rank local)")
        print(f"Shared scope: {shared_scope} (shared_comm size={shared_size})")
        print(f"N={args.n} bins={bins} dtype={args.dtype}")
        print(
            f"Shapes: cake_idxs={cake_idxs_local.shape} int64, "
            f"correction={correction_local.shape} {correction_local.dtype}, I=({bins},) float64"
        )

    comm.Barrier()
    times = run_bincount(
        cake_idxs_local,
        rank,
        args.n,
        args.dtype,
        args.seed,
        correction_local,
        bins,
        args.iters,
        args.warmup,
    )
    summarize(comm, f"np.bincount ({target})", times)

    # Cleanup windows
    win_idxs.Free()
    win_corr.Free()
    if shared_comm != node_comm:
        shared_comm.Free()


if __name__ == "__main__":
    main()
