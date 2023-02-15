import numpy as np
import cv2
from skimage import io, color

'''
Increases the contrast using HSV color space, inverting L value and using constant H and S
'''
def increase_contrast_HSV(bg, text, hue=0.33, sat=0.8):
    matte = np.repeat(text[:, :, 0], 3).reshape(text.shape)

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
    bg_rgb = cv2.GaussianBlur(bg_rgb,(35,35), 10)
    return bg_rgb * matte

'''
Increases contrast using LAB color space, inverting the L value and keeping other values the same
'''
def increase_contrast_LAB(bg, text):
    matte = np.repeat(text[:, :, 0], 3).reshape(text.shape)

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
    
    # blur so it isn't so sudden of a transition
    bg_lab = cv2.GaussianBlur(bg_lab,(85,85), cv2.BORDER_DEFAULT)
    
    bg_inverted_rgb = color.lab2rgb(bg_lab)

    return bg_inverted_rgb * matte