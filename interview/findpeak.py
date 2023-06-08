import numpy as np
import time

def findPeakUtil(arr, low, hi, n):
    mid = low + (hi-low)/2
    mid = int(mid)

    # If mid is the first or last or its value is not
    # lower than its neighbor
    if (mid == 0 or arr[mid-1] <= arr[mid]) and     \
            (mid == n-1 or arr[mid+1] <= arr[mid]):
        return mid
    # If mid is not the peak and the left side is more
    elif (mid > 0 and arr[mid-1] > arr[mid]):
        return findPeakUtil(arr, low, mid-1, n)
    else:
        return findPeakUtil(arr, mid+1, hi, n)

def findPeak2(arr):
    n = len(arr)
    if n == 0:
        return -1
    return findPeakUtil(arr, 0, n-1, n)

def findPeak(arr):
    """Returns index of a peak element.
    A peak is an elemeent where its value is not smaller than the values of
    its neighbors.
    """
    n = len(arr)
    if n == 0:
        return -1
    if n == 1:
        return 0
    if arr[0] >= arr[1]:
        return 0
    if arr[n-1] > arr[n-2]:
        return n-1

    for i in range(1, n-1):
        if arr[i] >= arr[i+1] and arr[i] >= arr[i-1]:
            return i

examples = [[ 1, 3, 20, 4, 1, 0 ],
        [], 
        [2,4],
        [4,2],
        [4,4]]

rng = np.random.default_rng(12345)
ex2 = [rng.integers(low=0, high=1e6, size=2000), ]

for arr in ex2:
    t0 = time.monotonic()
    index = findPeak(arr)
    t1 = time.monotonic()
    index2 = findPeak2(arr)
    t2 = time.monotonic()
    print(f"index of the peak in {arr[:3]} (size:len(arr)) is {index} t: {t1-t0:.2f}s (findPeak2: {index2}) t: {t2-t1:.2f}s.")

