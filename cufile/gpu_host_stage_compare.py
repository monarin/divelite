#!/usr/bin/env python3
"""
Run a consistent comparison matrix for file->GPU paths:
  1) host/pageable (pattern 4)
  2) host/pinned   (pattern 4)
  3) cufile        (pattern 3)

This script calls psana.debugtools.gpu_host_stage_bench and collects JSON outputs.
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
from typing import Dict, List, Optional, Sequence, Tuple


def _positive_int(value: str) -> int:
    out = int(value)
    if out <= 0:
        raise argparse.ArgumentTypeError(f"{value} is not a positive integer")
    return out


def _positive_float(value: str) -> float:
    out = float(value)
    if out <= 0:
        raise argparse.ArgumentTypeError(f"{value} is not a positive float")
    return out


def _parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run pageable/pinned/cuFile benchmark scenarios with matched parameters."
    )
    parser.add_argument(
        "--path",
        default="/sdf/data/lcls/ds/mfx/mfx101344525/xtc/mfx101344525-r0125-s007-c000.xtc2",
        help="Path to the input file.",
    )
    parser.add_argument("--chunk-mb", type=_positive_float, default=64.0)
    parser.add_argument("--max-gb", type=_positive_float, default=8.0)
    parser.add_argument("--passes", type=_positive_int, default=1)
    parser.add_argument("--warmup-chunks", type=int, default=2)
    parser.add_argument("--gpu", type=int, default=0)
    parser.add_argument(
        "--backend",
        choices=("auto", "cupy", "torch"),
        default="auto",
        help="Backend used for host mode runs.",
    )
    parser.add_argument(
        "--cufile-compat-mode",
        choices=("auto", "on", "off"),
        default="off",
        help="KVIKIO_COMPAT_MODE used for cuFile run.",
    )
    parser.add_argument(
        "--cufile-require-gds",
        action="store_true",
        help="Fail cuFile run if KvikIO reports compatibility mode ON.",
    )
    parser.add_argument(
        "--skip-cufile",
        action="store_true",
        help="Run only host pageable/pinned scenarios.",
    )
    parser.add_argument(
        "--outdir",
        default="",
        help=(
            "Optional output directory for JSON artifacts. "
            "If omitted, a temporary directory is used."
        ),
    )
    parser.add_argument(
        "--keep-going",
        action="store_true",
        help="Continue remaining scenarios if one fails.",
    )
    return parser.parse_args(argv)


def _read_json(path: str) -> Optional[Dict]:
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as fobj:
        return json.load(fobj)


def _scenario_cmd(
    args: argparse.Namespace,
    mode: str,
    json_path: str,
    host_mem: str = "",
) -> List[str]:
    cmd = [
        sys.executable,
        "-m",
        "psana.debugtools.gpu_host_stage_bench",
        "--mode",
        mode,
        "--path",
        args.path,
        "--chunk-mb",
        str(args.chunk_mb),
        "--max-gb",
        str(args.max_gb),
        "--passes",
        str(args.passes),
        "--warmup-chunks",
        str(args.warmup_chunks),
        "--gpu",
        str(args.gpu),
        "--json-out",
        json_path,
    ]
    if mode == "host":
        cmd.extend(["--backend", args.backend, "--host-mem", host_mem])
    else:
        cmd.extend(["--cufile-compat-mode", args.cufile_compat_mode])
        if args.cufile_require_gds:
            cmd.append("--cufile-require-gds")
    return cmd


def _run_one(name: str, cmd: List[str]) -> Tuple[int, str, str]:
    proc = subprocess.run(cmd, text=True, capture_output=True)
    return proc.returncode, proc.stdout, proc.stderr


def _print_summary(rows: List[Tuple[str, int, Optional[Dict]]]) -> None:
    print("\nSummary")
    print("  scenario        rc   end_to_end GiB/s   details")
    for name, rc, payload in rows:
        e2e = "-"
        details = "-"
        if payload:
            val = payload.get("end_to_end_gib_s")
            if isinstance(val, (int, float)):
                e2e = f"{val:.2f}"
            if name == "cufile":
                details = (
                    f"compat={payload.get('cufile_compat')} "
                    f"gds={payload.get('gds_available')} "
                    f"libcufile={payload.get('libcufile')}"
                )
            else:
                details = f"backend={payload.get('backend')} host_mem={payload.get('host_mem')}"
        print(f"  {name:<14} {rc:<4} {e2e:<16} {details}")


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = _parse_args(argv)
    outdir = args.outdir or tempfile.mkdtemp(prefix="gpu_host_stage_compare_")
    os.makedirs(outdir, exist_ok=True)

    scenarios = [("host_pageable", "host", "pageable")]
    scenarios.append(("host_pinned", "host", "pinned"))
    if not args.skip_cufile:
        scenarios.append(("cufile", "cufile", ""))

    print("gpu_host_stage_compare")
    print(f"  outdir          : {outdir}")
    print(f"  path            : {args.path}")
    print(f"  chunk_mb        : {args.chunk_mb}")
    print(f"  max_gb          : {args.max_gb}")
    print(f"  passes          : {args.passes}")
    print(f"  warmup_chunks   : {args.warmup_chunks}")
    print(f"  gpu             : {args.gpu}")
    print()

    summary_rows: List[Tuple[str, int, Optional[Dict]]] = []
    overall_rc = 0
    for name, mode, host_mem in scenarios:
        json_path = os.path.join(outdir, f"{name}.json")
        cmd = _scenario_cmd(args, mode=mode, json_path=json_path, host_mem=host_mem)
        print(f"=== {name} ===")
        print("cmd:", " ".join(cmd))
        rc, stdout, stderr = _run_one(name, cmd)
        if stdout:
            print(stdout.rstrip())
        if stderr:
            print(stderr.rstrip(), file=sys.stderr)
        payload = _read_json(json_path)
        summary_rows.append((name, rc, payload))
        if rc != 0:
            overall_rc = rc
            if not args.keep_going:
                break

    _print_summary(summary_rows)
    print(f"\nArtifacts: {outdir}")
    return overall_rc


if __name__ == "__main__":
    raise SystemExit(main())
