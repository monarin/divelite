import numpy as np
from scipy.linalg import toeplitz
from scipy.linalg import inv
import matplotlib.pyplot as plt

"""
Calculate filter weights for tmo timetool
detail: https://confluence.slac.stanford.edu/display/PSDM/TimeTool
"""

bgs = np.array([[0,1,0.5], \
        [0.25,0.75,0.4], \
        [.5,1.5,0.6],])
# Step 3 normalize backgrounds
bg_avg = np.average(bgs[:])
bgs /= bg_avg

results = np.zeros(bgs.shape)
for i, bg in enumerate(bgs):
    plt.subplot(3,3,i+1)
    plt.title(f'bg {i}')
    plt.plot(bg, label=f'normalized bg {i}')
    result  = np.correlate(bg, bg, mode='full') 
    # Auto correlation is the second half in 'full mode' for np.correlate. 
    # See https://stackoverflow.com/questions/643699/how-can-i-use-numpy-correlate-to-do-autocorrelation
    results[i] = result[int(result.size/2):]
    plt.plot(results[i], label=f'autocorr {i}')
    plt.ylim(0,7)
    plt.legend()

# Step 4: auto-correlation function (acf) is the average of all those products
acf = np.average(results, axis=0)
plt.subplot(3,3,4)
plt.title('auto-correlation fn (acf)')
plt.plot(acf)

# Step 5: Collect your best averaged ratio (signal divided by averaged background) with signal; this averaging smooths out any non-physics features
signal = np.array([1, .5, 0])
plt.subplot(3,3,5)
plt.title('signal')
plt.plot(signal)

acfm = toeplitz(acf)
acfm_inv = inv(acfm)
w = np.dot(acfm_inv, signal)
plt.subplot(3,3,6)
plt.title('w=signal/acf')
plt.plot(w)

weights = np.flip(w)
plt.subplot(3,3,7)
plt.title('weights=flip(w)')
plt.plot(weights)

norm = np.dot(weights, signal)
weights = weights * 1.00 / norm
plt.subplot(3,3,8)
plt.title(f'weights/norm (norm=weights*signal)')
plt.plot(weights)

w = w * 1.0 / norm
plt.subplot(3,3,9)
plt.title(f'w/norm (norm=weights*signal)')
plt.plot(w)

norm = np.dot(weights, signal)

plt.show()
