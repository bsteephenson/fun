from PIL import Image 

import sklearn
import sklearn.cluster

im = Image.open("cat2.jpg")
im = im.convert("RGB")

print(im.load()[0, 0])

(Xs, Ys, Xf, Yf) = im.getbbox()

height = Yf - Ys
width = Xf - Xs
num_pixels = height * width

# downsample
rate = 1
im = im.resize((int(width / rate), int(height / rate)))
im.show()

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



labels = sklearn.cluster.KMeans(n_clusters = clusters).fit(data).predict(data)




avg_colors = np.zeros((clusters, 3))
counts = np.zeros(clusters)
for i in range(clusters):
    count = 0
    for j in range((num_pixels)):
        if (labels[j] == i):
            count = count + 1
            [x, y, r, g, b] = data[j]
            avg_colors[i] = avg_colors[i] + [r, g, b]
    avg_colors[i] = (avg_colors[i] / count)
print(avg_colors[0])

# # replace each pixel in the image with the avg of its cluster

b = im.load()

for i in range(num_pixels):
    x = int(i / height)
    y = int(i % height)
    [r, g, b] = avg_colors[labels[i]]
    print((int(r), int(g), int(b)))
#     im[(x, y)] = (int(r), int(g), int(b))
    im.putpixel((x, y), (int(r), int(g), int(b)))

im.show()