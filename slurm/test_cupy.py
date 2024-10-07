import cupy as cp

x_gpu = cp.array([1, 2, 3])
x_cpu = cp.asnumpy(x_gpu)

print(f'{x_cpu=}')
