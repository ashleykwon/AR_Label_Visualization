"""
Goal: Maxmize color distance in CIELAB space
Idea: 
- The distance to a given point in CIELAB will be on the boundary of the space.
- We can determine the boundary of CIELAB based on the error of converting to RGB and back
  (may be a better approach?)
- Then find the point on this boundary that maximizes the distance

"""
import numpy as np
from skimage import color
from matplotlib import pyplot as plt
from matplotlib import cm
from scipy.ndimage import sobel

error_threshold = 1e-6
res = 10 # resolution of points from CIELAB space

# start with all possible values in the space (+10 padding just in case)
grid = np.mgrid[-10:110:res, -110:110:res, -110:110:res].T.astype(float)
# convert to RGB and back
grid_conv = color.rgb2lab(color.lab2rgb(grid))
# find square error of conversion
diff = np.sum((grid_conv - grid)**2, axis=3)
# threshold the error
thresh = (diff < error_threshold).astype(float)

# use sobel filter to find boundary of acceptable error
sobel_x = sobel(thresh, axis=0)
sobel_y = sobel(thresh, axis=0)
sobel_z = sobel(thresh, axis=0)
sobel_magsq = sobel_x ** 2 + sobel_y ** 2 + sobel_z ** 2
boundary = grid[sobel_magsq > 0]

# find point on boundary with maximum distance from a single color
def max_dist(col):
    distsq = np.sum((boundary - col) ** 2, axis=1)
    index = np.argmax(distsq)
    return boundary[index]

# equivilant to previous function but applies max distance to each pixel in an RGB image
def maximize_contrast(img, goal=None, thresh=500):
    
    candidates = boundary
    if goal is not None:
        goal = color.rgb2lab(goal)
        candidates = candidates[np.sum((goal - candidates) ** 2, axis=1) < thresh * thresh]

    # vectorize computation of subtracting each element
    repeated = candidates.repeat((img.shape[0] * img.shape[1])).reshape((*candidates.shape, img.shape[1], img.shape[0]))
    distsq = np.sum((img.T - repeated)**2, axis=1)
    index = np.argmax(distsq, axis=0)
    contrast_bg = candidates[index.T]

    return contrast_bg

# Code for plotting the boundary, was useful in verifying that 
# convolution method was working:
if __name__ == '__main__':
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')

    colors = color.lab2rgb(boundary)

    ax.scatter(boundary[:, 0], boundary[:, 1], boundary[:, 2], marker='.', s=50, color=colors)
    
    red = color.rgb2lab([1., 0., 0.])
    green = color.rgb2lab([0., 1., 0.])
    blue = color.rgb2lab([0., 0., 1.])

    ax.scatter([red[0], green[0], blue[0]], [red[1], green[1], blue[1]], [red[2], green[2], blue[2]], color=["red", "green", "blue"], s=200)
    
    ax.set_title("Boundary of LAB colorspace")
    ax.set_xlabel('L*')
    ax.set_ylabel('a*')
    ax.set_ylabel('b*')
    
    # displaying plot
    plt.show()