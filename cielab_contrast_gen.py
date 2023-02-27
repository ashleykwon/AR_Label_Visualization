import numpy as np
from matplotlib import pyplot as pt
import cv2
import math
from skimage import io, color
from PIL import Image
#import palette_based_color_assignment as pbca

'''
Goals: 
- Use L*a*b* to generate a label that maximally contrasts with it's background (no set hue at the moment) 
- Include blur accross the label color for readability
'''


'''
sample_pixel takes a labelPixelCoordinate and returns the pixel values of it's 14 neighbors
'''
def sample_pixels(labelPixelCoordinate, background_img):
    neighboringPixelCoordinates = []
    for i in range(labelPixelCoordinate[0]-2, labelPixelCoordinate[0]+3):
        for j in range(labelPixelCoordinate[1]-2, labelPixelCoordinate[1]+3):
            neighboringPixelCoordinates.append(background_img[i][j].tolist())
    return np.asarray(neighboringPixelCoordinates)


'''
get_contrast calculates a contrasting color given a color in CIELAB
'''
def get_contrast(my_color):
    ## Lightness contrast
    L = my_color[0]
    if L > 55:
        new_L = L - 30
    elif L <= 55:
        new_L = L + 40

    ## Color contrast
    rg_opp = -my_color[1]
    yb_opp = -my_color[2]
    return [new_L, rg_opp, yb_opp]

'''
pick_lightness modifies lightness to enhance contrast, and applies the given color
(small thing to be debugged: only works if the input colors are negated, so just take that into account)
'''
def pick_lightness(orig_lightness, given_rg, given_by):
    ## Lightness contrast
    new_L = 0
    if orig_lightness > 55:
        new_L = 30
    elif orig_lightness <= 55:
        new_L = 70

    ## Color contrast
    return np.asarray([new_L, given_rg, given_by])


def final_computation(goal_color, background_image, label_image):

    # Load the background image 
    '''
    background_name = "sample_scene.jpeg"
    background_image = np.asarray(Image.open('./bgs/'+background_name))[:,:,:3]
    label_name = "sample_text_2.png"
    label_image = np.asarray(Image.open('./labels/'+ label_name))[:,:,0]
    '''

    # Get the coordinates of pixels that belong to the label
    coordinates = np.mgrid[:label_image.shape[0], :label_image.shape[1]]
    label_pixels = label_image==255
    label_coordinates = coordinates[:, label_pixels]
    label_coordinates = np.array(list(zip(label_coordinates[0,:], label_coordinates[1,:])))

    # labelColors will store (for each pixel in the label) the color it should be!!

    # given_color is the color of the label in cielab
    given_color = color.rgb2lab(goal_color)
    as_lab = color.rgb2lab(background_image) 

    for coord in label_coordinates:
        sampled_color = as_lab[coord[0], coord[1]]
        contrast_cielab = pick_lightness(sampled_color[0], given_color[1], -given_color[2])
        #contrast_cielab = cielab_contrast_gen.get_contrast(sampled_color)
        as_lab[coord[0], coord[1], :3] = contrast_cielab
    
    background_image = color.lab2rgb(as_lab)

    blurred_image = cv2.blur(background_image, (3, 3))
    for i in range(len(label_coordinates)):
        coord = label_coordinates[i]
        label_blurred = blurred_image[coord[0], coord[1],:]
        background_image[coord[0], coord[1],:] = label_blurred.clip(0,1)

    pt.imsave("./results/color_contrast_test.png", background_image)
    pt.show()

background_name = "sample_scene.jpeg"
background_image = np.asarray(Image.open('./bgs/'+background_name))[:,:,:3]
label_name = "sample_text_2.png"
label_image = np.asarray(Image.open('./labels/'+ label_name))[:,:,0]
final_computation([0.9, 0.2, 0.2], background_image, label_image)

