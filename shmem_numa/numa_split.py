#!/usr/bin/env python3
import os
from glob import glob
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


def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    cpu = get_cpu_id()
    cpu_to_numa = build_cpu_to_numa()
    numa_id = cpu_to_numa.get(cpu, -1)

    numa_comm = comm.Split(color=numa_id, key=rank)
    numa_rank = numa_comm.Get_rank()

    if numa_rank == 0:
        host = MPI.Get_processor_name()
        print(f"NUMA leader: rank {rank} host {host} numa {numa_id}")

    # Optional: show mapping for all ranks
    # print(f"rank {rank} cpu {cpu} numa {numa_id}")


if __name__ == '__main__':
    main()
