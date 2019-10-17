import numpy as np
import matplotlib.pyplot as plt
plot = False

import math, random

def fibonacci_sphere(samples=1,randomize=False):
    rnd = 1.
    if randomize:
        rnd = random.random() * samples

    points = np.zeros((samples,3))
    offset = 2./samples
    increment = math.pi * (3. - math.sqrt(5.));

    for i in range(samples):
        y = ((i * offset) - 1) + (offset / 2);
        r = math.sqrt(1 - pow(y,2))

        phi = ((i + rnd) % samples) * increment
        
        x = math.cos(phi) * r
        z = math.sin(phi) * r

        if z > 0:
            points[i,0] = -x
            points[i,1] = y
            points[i,2] = -z          
        else:
            points[i,0] = x
            points[i,1] = y
            points[i,2] = z

    return points



# 1) Get a list of peaks and asic position translators
# peaks.npy contains 17 variables - only take x,y,z which are in row 0,1,2
peaks = np.array(np.load('cxitut13_peaks233.npy'), dtype=np.int64) 
n_peaks = peaks.shape[0]
trans_x_list = np.load('cxitut13_iX.npy') # Asic position translator for x
trans_y_list = np.load('cxitut13_iY.npy') # Asic position translator for y

# Get a list of true coordinates for all the peaks
det_x_list = trans_x_list[peaks[:,0], peaks[:,1], peaks[:,2]] + 0.5 # shift to centre of a pixel
det_y_list = trans_y_list[peaks[:,0], peaks[:,1], peaks[:,2]] + 0.5

# 2) Converts true coodinates to pixel positions (m) in real space with (0,0) at the center
center_x = 877
center_y = 864
pixel_size = 110e-6 # (m)
det_shift_x_list = (det_x_list - center_x) * pixel_size
det_shift_y_list = (det_y_list - center_y) * pixel_size

# Check real positions
if plot:
    plt.plot(det_shift_x_list, det_shift_y_list, 'o')
    plt.plot(det_shift_x_list[108], det_shift_y_list[108], 's')
    plt.plot(0,0,'rx')
    plt.axis('scaled')
    plt.show()

# 3) Convert real to reciprocal coordinates (s vector)
# e.g. rec_x = det_shift_x_list / lambda * sqrt(det_shift_x_list^2 + det_shift_y_list^2 + D^2)
photon_energy = 8.06 # keV
wavelength = 12.407002 / float(photon_energy) * 1e-10  # (m)
D = 0.158 # detector distance (m)
#r = wavelength * np.sqrt(det_shift_x_list**2 + det_shift_y_list**2 + D**2)
r = np.sqrt(det_shift_x_list**2 + det_shift_y_list**2 + D**2)
s_vec_list = np.array([D/r-1, det_shift_x_list/r, det_shift_y_list/r]) / wavelength

# Generate list of t vectors
n_ts = 15000
fibo_t_list = fibonacci_sphere(samples=n_ts)
tx_list = fibo_t_list[:,1]
ty_list = fibo_t_list[:,2]
tz_list = fibo_t_list[:,0]

for i in range(n_ts):    
    # For every randomly chosen t vector, calculate a projection
    # of each rec_vec
    t = np.array([tx_list[i], ty_list[i], tz_list[i]])
    n_bins = 2800
    p_list = np.dot(t, s_vec_list) # p = q . t where q is each vector in s_vec_list

    # Bin p
    max_p = np.max(p_list)
    bins = np.linspace(0, max_p, n_bins) # create an equal size binning for value from 0 to max(p)
    digitized = np.digitize(p_list, bins) # find the location where each p belongs in the 'bins'.
    f_p = np.zeros((n_bins, ))
    #f_p, _ = np.histogram(p_list, bins=bins)

    for i_d in digitized:
        f_p[i_d-1] += 1

    # Take the fourier transform on frequency of p and chop off the left half.
    f_j = np.fft.fftshift(np.fft.fft(f_p))[int(n_bins/2):]

    # Start checking distance between peaks
    thres_f_j = 50
    f_j_peak_locs = np.where(f_j > thres_f_j)

    if len(f_j_peak_locs) > 1:
        plt.subplot(2,1,1)
        plt.plot(f_p)
        plt.subplot(2,1,2)
        plt.plot(f_j)
        plt.show()




from IPython import embed
embed()

