import sys

fname = sys.argv[1]

perf_events = ['stalled-cycles-backend:u', 
        'stalled-cycles-frontend:u',
        'ls_l1_d_tlb_miss.all:u',
        'l1_dtlb_misses:u',
        'l1_data_cache_fills_all:u',
        'bp_l1_tlb_miss_l2_tlb_miss.if2m:u',
        'bp_l1_tlb_miss_l2_tlb_miss:u',
        'l2_dtlb_misses:u',
        'l2_itlb_misses:u',
        ]
results = {}
with open(fname, 'r') as f:
    for line in f:
        for perf_event in perf_events:
            if line.find(perf_event) > -1:
                cols = line.split()
                #val = int(cols[0].replace(',',''))
                results[perf_event] = cols[0]
                break

tbl_txt = ''
hdr_txt = ''
for perf_event in perf_events:
    hdr_txt += perf_event + ' '
    tbl_txt += results[perf_event] + ' '
print(hdr_txt)
print(tbl_txt)



