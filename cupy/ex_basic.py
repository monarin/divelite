from numba import cuda
import numpy as np
import time
import cupy as cp

@cuda.jit
def increment_by_one(an_array):
    ## Identifying pos using thread/ block id
    ## Thread id in a 1D block
    #tx = cuda.threadIdx.x
    ## Block id in a 1D grid
    #ty = cuda.blockIdx.x
    ## Block width, i.e. number of threds per block
    #bw = cuda.blockDim.x
    ## Compute flattened index inside the array
    #pos = tx + ty * bw
    ## Identifying pos using standard grid
    pos = cuda.grid(1)
    if pos < an_array.size:
        an_array[pos] += 1

def increment_by_one_cpu(an_array):
    for i in range(an_array.size):
        an_array[i] += 1

def increment_by_one_cupy(an_array):
    # Transfer data to device
    x_gpu = cp.asarray(an_array)
    x_gpu += 1
    an_array[:] = cp.asnumpy(x_gpu)


if __name__ == "__main__":
    size = 1000000
    an_array = np.zeros(size)
    print(f'{an_array[:3]=}')
    st = time.monotonic()
    threadsperblock = 32
    blockspergrid = (an_array.size + (threadsperblock - 1)) # threadsperblock
    increment_by_one[blockspergrid, threadsperblock](an_array)
    en = time.monotonic()
    print(f'{an_array[:3]=} t:{en-st:.2f}s.')
    st = time.monotonic()
    increment_by_one_cpu(an_array)
    en = time.monotonic()
    print(f'{an_array[:3]=} t:{en-st:.2f}s.')
    st = time.monotonic()
    increment_by_one_cupy(an_array)
    en = time.monotonic()
    print(f'{an_array[:3]=} t:{en-st:.2f}s.')
