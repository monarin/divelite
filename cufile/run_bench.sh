#!/usr/bin/env bash
set -euo pipefail

export MAMBA_ROOT_PREFIX="$HOME/micromamba"
eval "$($HOME/bin/micromamba shell hook -s bash)"
micromamba activate gpuio311

export KVIKIO_COMPAT_MODE="${KVIKIO_COMPAT_MODE:-OFF}"
export KVIKIO_NTHREADS="${KVIKIO_NTHREADS:-1}"
export KVIKIO_TASK_SIZE="${KVIKIO_TASK_SIZE:-16777216}"
export KVIKIO_AUTO_DIRECT_IO_READ="${KVIKIO_AUTO_DIRECT_IO_READ:-1}"

exec python "$HOME/divelite/cufile/gpu_host_stage_bench.py" "$@"

