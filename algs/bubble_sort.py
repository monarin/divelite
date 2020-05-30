# Use bubble sort to find the k smallest number
# in an n-length array.


# Bruteforce bubble sort
def bruteforce(a):
    tmp = 0
    still_swap = True

    while still_swap:
        still_swap = False
        for i in range(len(a)-1):
            if a[i+1] < a[i]:
               tmp = a[i]
               a[i] = int(a[i+1])
               a[i+1] = tmp
               still_swap = True
        print(a)

def swap_me(a):
    for i in range(len(a)-1):
        if a[i+1] < a[i]:
            tmp = a[i]
            a[i] = int(a[i+1])
            a[i+1] = tmp
            print(f'a={a} swap_me({a[i+1:]})')
            swap_me(a)
    print(a)
    return a

a = [4,1,3,2,5]
print(f'original a={a}')
print('bruteforce')
bruteforce(a[:])
print()
print('recursive')
swap_me(a[:])
            


