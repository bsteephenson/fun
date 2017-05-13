import gizeh
import moviepy.editor as mpy

import numpy as np
import scipy
import colorsys


def num_to_rgb(num):
    num = min(1, num)
    num = max(0, num)

    it = colorsys.hsv_to_rgb(.2 * num + .35, .75, .9)
    return (it[0], it[1], it[2], num)

W,H = 640,640 # width, height, in pixels
duration = 15 # duration of the clip, in seconds

points_x, points_y = 10, 10

num_points = points_x * points_y

# init state
# state = np.asarray([1, 0, 0, 0]).reshape((points_x * points_y))

state = np.zeros((points_x, points_y))
state[points_x /2, points_y / 2] = 10

state = state.reshape((points_x * points_y))

# transition matrix
# mat = np.asarray([
#         [0, .75, .25, 0], 
#         [0, 0, 1, 0],
#         [0, 0, 0, 1],
#         [1, 0, 0, 0]
#         ]).T.reshape((points_x * points_y, points_x * points_y))

# mat = np.random.randint(2, size = (points_x * points_y, points_x * points_y)).astype(float)
# mat = mat / np.sum(mat, axis = 0)
# print mat
# print np.sum(mat, axis = 0)
# exit()

mat = np.zeros((points_x * points_y, points_x * points_y))

rand = np.random.choice(num_points, num_points, replace = False)

ratio = 1 - .5

for i in range(num_points):
    mat[i, rand[i]] = ratio
    mat[i, i] = 1 - ratio


def make_frame(t):

    global state;

    surface = gizeh.Surface(W,H, bg_color = (.1, .1, .1))
    # radius = W*(1+ (t*(duration-t))**2 )/6
    radius = min(W / points_x, H / points_y) / 3

    state = np.matmul(mat, state)
    print state

    for i in range(points_x):
        for j in range(points_y):
            x = W / (points_x) * (i + .5)
            y = W / (points_y) * (j + .5)
            circle = gizeh.circle(radius, xy = (x, y), fill=num_to_rgb(state[i + j * points_x]))
            circle.draw(surface)
    return surface.get_npimage()

clip = mpy.VideoClip(make_frame, duration=duration)
clip.write_gif("animation.gif",fps=15, opt="OptimizePlus", fuzz=10)

clip.preview()