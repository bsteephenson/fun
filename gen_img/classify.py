from PIL import Image 

import sklearn
import sklearn.cluster
import sklearn.svm
import sklearn.neighbors
from sklearn.neighbors import KNeighborsClassifier as KNN
import sklearn.neural_network

im = Image.open("cat.jpg")
im = im.convert("RGB")

print(im.load()[0, 0])

(Xs, Ys, Xf, Yf) = im.getbbox()

height = Yf - Ys
width = Xf - Xs
num_pixels = height * width

im.show()

# downsample
rate = 2
im = im.resize((int(width / rate), int(height / rate)))

(Xs, Ys, Xf, Yf) = im.getbbox()

height = Yf - Ys
width = Xf - Xs
num_pixels = height * width


# Turn this into data in R^5
# [x, y, r, g, b]

import numpy as np

pixels = im.load()


data = []
for x in range(Xs, Xf):
    for y in range(Ys, Yf):
        r, g, b = pixels[x, y]
        data.append([x, y, r, g, b])

data = np.array(data)

print(data.shape)

clusters = 8

colors = data[:, 2:]

color_labels = sklearn.cluster.KMeans(n_clusters = clusters).fit(data).predict(data)

# learner = sklearn.cluster.SpectralClustering(n_clusters = clusters, affinity="rbf", gamma = .001, assign_labels = "kmeans")
# labels = learner.fit_predict(data)



avg_colors = np.zeros((clusters, 3))
counts = np.zeros(clusters)
for i in range(clusters):
    count = 0
    for j in range((num_pixels)):
        if (color_labels[j] == i):
            count = count + 1
            [x, y, r, g, b] = data[j]
            avg_colors[i] = avg_colors[i] + [r, g, b]
    avg_colors[i] = (avg_colors[i] / count)
print(avg_colors[0])


points = data[:, :2]

print points
print color_labels

# point_labels = sklearn.neural_network.MLPClassifier(activation = "tanh", hidden_layer_sizes = (20, 20), verbose = True).fit(points, color_labels).predict(points)

# create a subset to learn from

TRAIN_PERCENT = 1.00

indices = np.random.permutation(len(points))[:int(len(points) * TRAIN_PERCENT)]
train_points = points[indices]
train_color_labels = color_labels[indices]

print train_points.shape

point_labels = sklearn.neural_network.MLPClassifier(hidden_layer_sizes = (200, 200, 200), activation = "logistic", verbose = True).fit(train_points, train_color_labels).predict_proba(points)
# point_labels = sklearn.neighbors.KNeighborsClassifier(n_neighbors = 3).fit(train_points, train_color_labels).predict_proba(points)



# # replace each pixel in the image with the avg of its cluster

b = im.load()

for i in range(num_pixels):
    x = int(i / height)
    y = int(i % height)
    # [r, g, b] = avg_colors[point_labels[i]]
    weights = point_labels[i]
    weights = weights ** 10
    weights = weights / np.sum(weights)
    [r, g, b] = np.dot(weights, avg_colors)
    print((int(r), int(g), int(b)))
#     im[(x, y)] = (int(r), int(g), int(b))
    im.putpixel((x, y), (int(r), int(g), int(b)))

im = im.resize((int(width * rate), int(height * rate)))

im.show()