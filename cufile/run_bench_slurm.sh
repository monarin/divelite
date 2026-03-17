#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

jobid="${NSIGHT_SLURM_JOB_ID:-}"
jobid_from_arg=0
profile_mode="${NSIGHT_PROFILE_MODE:-nsys}" # nsys|none
user_report_prefix="${NSIGHT_REPORT_PREFIX:-}"
cuda_memory_usage="${NSIGHT_CUDA_MEMORY_USAGE:-false}"
# New name preferred; old env kept as alias.
gpu_metrics_devices="${NSIGHT_GPU_METRICS_DEVICES:-${NSIGHT_GPU_METRICS_DEVICE:-}}"
bench_args=()

# Parse wrapper options anywhere; forward unknown options to benchmark script.
while [[ $# -gt 0 ]]; do
  case "$1" in
    --jobid)
      if [[ $# -lt 2 ]]; then
        echo "ERROR: --jobid requires a value" >&2
        exit 2
      fi
      jobid="$2"
      jobid_from_arg=1
      shift 2
      ;;
    --profile-mode)
      if [[ $# -lt 2 ]]; then
        echo "ERROR: --profile-mode requires a value (nsys|none)" >&2
        exit 2
      fi
      profile_mode="$2"
      shift 2
      ;;
    --report-prefix)
      if [[ $# -lt 2 ]]; then
        echo "ERROR: --report-prefix requires a value" >&2
        exit 2
      fi
      user_report_prefix="$2"
      shift 2
      ;;
    --cuda-memory-usage)
      if [[ $# -lt 2 ]]; then
        echo "ERROR: --cuda-memory-usage requires a value (true|false)" >&2
        exit 2
      fi
      cuda_memory_usage="$2"
      shift 2
      ;;
    --gpu-metrics-devices)
      if [[ $# -lt 2 ]]; then
        echo "ERROR: --gpu-metrics-devices requires a value (e.g. all|none|<id-list>)" >&2
        exit 2
      fi
      gpu_metrics_devices="$2"
      shift 2
      ;;
    --gpu-metrics-device)
      if [[ $# -lt 2 ]]; then
        echo "ERROR: --gpu-metrics-device requires a value" >&2
        exit 2
      fi
      echo "[run_bench_slurm] WARNING: --gpu-metrics-device is deprecated; use --gpu-metrics-devices." >&2
      gpu_metrics_devices="$2"
      shift 2
      ;;
    --)
      shift
      bench_args+=("$@")
      break
      ;;
    *)
      bench_args+=("$1")
      shift
      ;;
  esac
done

set -- "${bench_args[@]}"

if [[ "$profile_mode" != "nsys" && "$profile_mode" != "none" ]]; then
  echo "ERROR: --profile-mode must be one of: nsys, none" >&2
  exit 2
fi

# If caller did not provide --jobid but we have a Slurm allocation in this shell,
# use that allocation id and launch via srun from login/alloc shells.
if [[ $jobid_from_arg -eq 0 && -z "$jobid" && -n "${SLURM_JOB_ID:-}" ]]; then
  jobid="$SLURM_JOB_ID"
fi

# If no job id is known and we are already on a compute task, run directly.
if [[ -z "$jobid" && -n "${SLURMD_NODENAME:-}" ]]; then
  if [[ "$profile_mode" == "none" ]]; then
    exec "$SCRIPT_DIR/run_bench.sh" "$@"
  fi
  echo "ERROR: running directly on compute node requires --jobid for nsys output naming." >&2
  exit 2
fi

if [[ -z "$jobid" ]]; then
  cat >&2 <<USAGE
Usage:
  $0 --jobid <slurm_job_id> [--profile-mode nsys|none] [--report-prefix NAME] \
     [--cuda-memory-usage true|false] [--gpu-metrics-devices all|none|<id-list>] [bench args...]

Compatibility alias:
  --gpu-metrics-device <value>  (deprecated, mapped to --gpu-metrics-devices)

Or set NSIGHT_SLURM_JOB_ID and run:
  NSIGHT_SLURM_JOB_ID=<jobid> $0 [bench args...]
USAGE
  exit 2
fi

cpus_per_task="${NSIGHT_CPUS_PER_TASK:-8}"
gres="${NSIGHT_GRES:-gpu:a100:1}"
out_dir="${NSIGHT_OUT_DIR:-$HOME/divelite/cufile/nsight_reports}"
trace_set="${NSIGHT_TRACE:-cuda,nvtx,osrt}"
nsys_bin_hint="${NSYS_BIN:-}"

mkdir -p "$out_dir"

timestamp="$(date +%Y%m%d_%H%M%S)"
if [[ -n "$user_report_prefix" ]]; then
  report_prefix="$out_dir/$user_report_prefix"
else
  report_prefix="$out_dir/bench_job${jobid}_${timestamp}"
fi

if [[ "$profile_mode" == "none" ]]; then
  exec srun \
    --jobid "$jobid" \
    --nodes 1 \
    --ntasks 1 \
    --cpus-per-task "$cpus_per_task" \
    --gres "$gres" \
    --exclusive \
    "$SCRIPT_DIR/run_bench.sh" "$@"
fi

export RUN_BENCH_SCRIPT="$SCRIPT_DIR/run_bench.sh"
export NSIGHT_REPORT_PREFIX="$report_prefix"
export NSIGHT_TRACE="$trace_set"
export NSYS_BIN_HINT="$nsys_bin_hint"
export NSIGHT_CUDA_MEMORY_USAGE="$cuda_memory_usage"
export NSIGHT_GPU_METRICS_DEVICES="$gpu_metrics_devices"

exec srun \
  --jobid "$jobid" \
  --nodes 1 \
  --ntasks 1 \
  --cpus-per-task "$cpus_per_task" \
  --gres "$gres" \
  --exclusive \
  /usr/bin/bash -lc '
    set -euo pipefail

    nsys_bin="${NSYS_BIN_HINT:-}"

    # 1) Keep user override highest priority.
    if [[ -z "$nsys_bin" ]] && command -v nsys >/dev/null 2>&1; then
      nsys_bin="$(command -v nsys)"
    fi

    # 2) Check known user installs first.
    for cand in \
      "$nsys_bin" \
      "$HOME/tools/nsight-systems/2026.1.1/pkg/bin/nsys" \
      "$HOME/nsight-systems-2026.1.1/bin/nsys" \
      /usr/local/cuda/bin/nsys \
      /usr/local/nsight-systems/bin/nsys \
      /opt/nvidia/nsight-systems/bin/nsys; do
      if [[ -n "$cand" && -x "$cand" ]]; then
        nsys_bin="$cand"
        break
      fi
    done

    # 3) Last-resort glob search for versioned user installs.
    if [[ -z "${nsys_bin:-}" || ! -x "$nsys_bin" ]]; then
      shopt -s nullglob
      dynamic_candidates=(
        "$HOME"/tools/nsight-systems/*/pkg/bin/nsys
        "$HOME"/nsight-systems-*/bin/nsys
      )
      shopt -u nullglob
      for cand in "${dynamic_candidates[@]}"; do
        if [[ -x "$cand" ]]; then
          nsys_bin="$cand"
          break
        fi
      done
    fi

    if [[ -z "${nsys_bin:-}" || ! -x "$nsys_bin" ]]; then
      echo "ERROR: nsys binary not found on compute node." >&2
      echo "Set NSYS_BIN to full path if nsys is installed in a non-standard location." >&2
      exit 127
    fi

    cuda_mem_usage="${NSIGHT_CUDA_MEMORY_USAGE:-false}"
    gpu_metrics_devices="${NSIGHT_GPU_METRICS_DEVICES:-}"
    strict_gpu_metrics="${NSIGHT_STRICT_GPU_METRICS:-0}"

    mkdir -p "$(dirname -- "$NSIGHT_REPORT_PREFIX")"
    echo "[run_bench_slurm] host: $(hostname)"
    echo "[run_bench_slurm] nsys: $nsys_bin"
    echo "[run_bench_slurm] report: ${NSIGHT_REPORT_PREFIX}.nsys-rep"
    echo "[run_bench_slurm] cuda-memory-usage: $cuda_mem_usage"

    profile_common=(
      profile
      --force-overwrite=true
      --trace="$NSIGHT_TRACE"
      --cuda-memory-usage="$cuda_mem_usage"
      -o "$NSIGHT_REPORT_PREFIX"
    )

    if [[ -n "$gpu_metrics_devices" && "$gpu_metrics_devices" != "none" ]]; then
      echo "[run_bench_slurm] gpu-metrics-devices: $gpu_metrics_devices"
      set +e
      "$nsys_bin" "${profile_common[@]}" \
        --gpu-metrics-devices="$gpu_metrics_devices" \
        "$RUN_BENCH_SCRIPT" "$@"
      rc=$?
      set -e
      if [[ $rc -eq 0 ]]; then
        exit 0
      fi
      if [[ "$strict_gpu_metrics" == "1" ]]; then
        echo "ERROR: profiling with gpu metrics failed (strict mode enabled)." >&2
        exit "$rc"
      fi
      echo "[run_bench_slurm] WARNING: profiling with gpu metrics failed (rc=$rc). Retrying without gpu metrics." >&2
    fi

    exec "$nsys_bin" "${profile_common[@]}" "$RUN_BENCH_SCRIPT" "$@"
  ' _ "$@"
