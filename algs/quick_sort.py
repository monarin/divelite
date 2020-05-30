a = [4, 2, 5, 1, 3]

def partition(a, st, en):
    print()
    print(f'Partition a={a[st:en+1]} st={st} en={en}')
    i_sel = en 
    pivot = a[i_sel]
    i = st - 1
    for j in range(st, en):
        if a[j] < pivot:
            i += 1
            tmp = a[i]
            a[i] = a[j]
            a[j] = tmp
            print(f'  pivot={pivot} a={a}')
    tmp = a[i+1]
    a[i+1] = pivot
    a[en] = tmp
    print(f'swap pivot at i={i} a={a}')

    if (i+1 - st) > 1:
        print(f'call partition i+1={i+1} st={st}')
        partition(a, st, i)

    if (en - (i+1)) > 1:
        print(f'call partition en={en} i+1={i+1}')
        partition(a, i + 2, en)


partition(a, 0, len(a)-1)
