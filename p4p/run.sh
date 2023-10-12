#!/bin/bash
set -x
set -e
for i in $(seq 0 10)
do
    python monitor_with_threads_safely.py
done
