#!/bin/bash
source $HOME/lcls2/setup_env.sh
conda activate ps-1.0.3
python $HOME/lcls2/psana/psana/tests/dev_eventbuilder.py
#python test_mpi.py
