import matplotlib.pyplot as plt

import numpy as np
import sklearn
from scipy.io import wavfile
from scipy.fftpack import fft, ifft

from sklearn.decomposition import PCA, KernelPCA, FastICA

rate, data = wavfile.read("amelie.wav")
# rate2, data2 = wavfile.read("ed_sheeren.wav")

# data = np.concatenate((data, data2))

print data
print data.shape

# print data[0].shape

# print fft(data)

chunk_size = 512 * 16 * 8
output = []

ffts = []
right_ffts = []

for i in range(len(data) / chunk_size):
	print i
	segment = data[i*chunk_size:(i+1) * chunk_size]
	# print segment.shape
	segment = segment.T
	[left, right] = fft(segment)
	ffts.append(np.concatenate((left, right)))
	# segment = ifft(transform)
	# data[i*chunk_size:(i+1) * chunk_size] = segment.T



ffts = np.asarray(ffts)

# pca.fit(ffts)

nearest_neighbors = sklearn.neighbors.NearestNeighbors(n_neighbors = 2)
nearest_neighbors.fit(ffts)

print "finishing fitting pca"


rate, data = wavfile.read("amelie.wav")

for i in range(len(data) / chunk_size):
	print i
	segment = data[i*chunk_size:(i+1) * chunk_size]
	# print segment.shape
	[left, right] = fft(segment.T)
	transform = np.concatenate((left, right))
	_, indices = nearest_neighbors.kneighbors(transform)

	transform = np.mean(ffts[indices], axis = 1)
	transform = transform.reshape(-1, 1)
	print transform.shape
	transform = transform.reshape(2, -1)
	# transform = pca.inverse_transform(pca.transform(transform))
	
	data[i*chunk_size:(i+1) * chunk_size] = ifft(transform).T
	# print transform.shape



wavfile.write("song2.wav", rate, data)