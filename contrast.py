import numpy as np
import cv2
from skimage import color
import cielab_boundary
'''
Increases the contrast using HSV color space, inverting L value and using constant H and S
'''
def increase_contrast_HSV(bg, hue=0.33, sat=0.8):
    bg_hsv = color.rgb2hsv(bg)
    v = bg_hsv[:, :, -1].copy()
    v = np.round(v)
    # invert V channel and set rest to constant values
    v = 0.2 * v + 0.8 * (1 - v)
    bg_hsv[:, :, -1] = v
    bg_hsv[:, :, 0] = hue
    bg_hsv[:, :, 1] = sat

    # convert back and blur it
    bg_rgb = color.hsv2rgb(bg_hsv)
    return bg_rgb

'''
Increases contrast using LAB color space, inverting the L value and keeping other values the same
'''
def increase_contrast_CIELAB(bg, hue=0.33, sat=0.8):
    desired_col = color.rgb2lab(color.hsv2rgb([hue, sat, 1])) # convert desired color to CIELAB

    bg_lab = color.rgb2lab(bg)
    bg_lab[:, :, 1:] *= -1

    L = bg_lab[:, :, 0]

    # try to find lightness values that are very different from the original
    new_L = np.zeros_like(L)
    new_L[L > 75] = 100 - L[L > 75]
    new_L[L < 25] = 100 - L[L < 25]
    new_L[(L > 25) & (L < 50)] = (100 - L[(L > 25) & (L < 50)]) + 25
    new_L[(L > 50) & (L < 75)] = (100 - L[(L > 50) & (L < 75)]) - 25
    bg_lab[:, :, 0] = new_L

    bg_lab[:, :, 1] = desired_col[1]
    bg_lab[:, :, 2] = desired_col[2]
    
    bg_inverted_rgb = color.lab2rgb(bg_lab)

    return bg_inverted_rgb

"""
Tries to find the furthest possible color in CIELAB space from each pixel in the image
"""
def maximize_contrast_CIELAB(bg, scale=0.1):
    # convert to LAB space
    bg_lab = color.rgb2lab(bg)
    
    # finding opposite of every color is slow so reduce resolution by some scale factor
    bg_lab = cv2.resize(bg_lab, (int(bg.shape[0] * scale), int(bg.shape[1] * scale)))
    contrast_bg = cielab_boundary.maximize_contrast(bg_lab)
    contrast_bg = cv2.resize(contrast_bg, (bg.shape[1], bg.shape[0]))

    bg_rgb = color.lab2rgb(contrast_bg)
 
    return bg_rgb