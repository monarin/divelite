import numpy as np
import matplotlib.pyplot as plt

#a = np.array([1,2,3])
#v = np.array([0,1,.5])
a = np.array([0,1,.5])
v = np.array([0,1,.5])

plt.plot(a, label='a')
plt.plot(v, label='v')

modes = ['valid', 'same', 'full']
for mode in modes:
    result = np.correlate(a, v, mode=mode)
    plt.plot(result, label=f'result mode={mode}')
plt.legend()
plt.show()
