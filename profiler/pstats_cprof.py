import pstats
import sys

if len(sys.argv) == 1:
    print("Usage: run python -m cProfile -o restats python_script.py args")
    print("then python pstats_cprof.py restats col_name(ncalls  tottime  percall  cumtime  percall)")
    exit()

restats_file=sys.argv[1]
sort_col=sys.argv[2]

p = pstats.Stats(restats_file)
p.strip_dirs().sort_stats(sort_col).print_stats()
#p.print_callees('__cinit__')

