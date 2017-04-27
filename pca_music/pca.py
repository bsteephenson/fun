import matplotlib.pyplot as plt

import numpy as np
from scipy.io import wavfile
from scipy.fftpack import fft, ifft

from sklearn.decomposition import PCA, KernelPCA, FastICA

rate, data = wavfile.read("adele.wav")

print data
print data.shape

# print data[0].shape

# print fft(data)

chunk_size = 512 * 16 * 16
output = []

left_ffts = []
right_ffts = []

for i in range(len(data) / chunk_size):
	print i
	segment = data[i*chunk_size:(i+1) * chunk_size]
	# print segment.shape
	segment = segment.T
	[left, right] = fft(segment)
	left_ffts.append(left)
	right_ffts.append(right)
	# segment = ifft(transform)
	# data[i*chunk_size:(i+1) * chunk_size] = segment.T

left_ffts = np.asarray(left_ffts)
right_ffts = np.asarray(right_ffts)
print left_ffts.shape
print right_ffts.shape

pca = PCA(n_components = 300)

all_ffts = np.vstack((left_ffts, right_ffts))
np.random.shuffle(all_ffts)

pca.fit(all_ffts[0:int(len(all_ffts) * .999)])
print "finishing fitting pca"
left_ffts = pca.inverse_transform(pca.transform(left_ffts))
right_ffts = pca.inverse_transform(pca.transform(right_ffts))
print left_ffts.shape
print "finishing dim reduction"

for i in range(len(data) / chunk_size):
	print i
	segment = ifft([left_ffts[i], right_ffts[i]])
	data[i*chunk_size:(i+1) * chunk_size] = segment.T


wavfile.write("song2.wav", rate, data)