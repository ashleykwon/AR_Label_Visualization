import numpy as np
from PIL import Image
from matplotlib import pyplot as pt
import cv2
import math
from skimage import io, color
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
    new_L = 0
    if L > 75 or L < 25:
        new_L = 100 - L
    elif L > 25 and L < 50:
        new_L = (100 - L) + 25
    else:
        new_L = (100 - L) - 25

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
    L = orig_lightness
    new_L = 0
    if L > 55:
        new_L = 50
    elif L <= 55:
        new_L = 70

    ## Color contrast
    return [new_L, given_rg, given_by]



# Load the background image 
background_name = "sample_scene.jpeg"
background_image = np.asarray(Image.open('./bgs/'+background_name))[:,:,:3]

# Convert background image to CIELAB
# THIS LINE IS VERY VERY SLOW
#background_image_cielab = np.apply_along_axis(color.rgb2lab, 2, background_image)

# # Load the label image (white label on a black background)
label_name = "sample_text_2.png"
label_image = np.asarray(Image.open('./labels/'+ label_name))[:,:,0]

# # Get the coordinates of pixels that belong to the label
coordinates = np.mgrid[:label_image.shape[0], :label_image.shape[1]]
label_pixels = label_image==255
label_coordinates = coordinates[:, label_pixels]
label_coordinates = np.array(list(zip(label_coordinates[0,:], label_coordinates[1,:])))

# labelColors will store (for each pixel in the label) the color it should be!!
labelColors = []
# given_color is the color of the label in cielab
given_color = color.rgb2lab([0.3, 0.8, 0])
for i in range(len(label_coordinates)):

    '''
    Sampling option one: sample 14 pixels and take average
    '''
    #neighboringPixels = sample_pixels(label_coordinates[i], background_image_cielab)
    #sampled_color = np.mean(neighboringPixels, axis=0)

    '''
    Sampling option two: sample pixel in background image
    '''
    coord = label_coordinates[i]
    
    sampled_color = color.rgb2lab(background_image[coord[0], coord[1]])

    '''
    Coloring option one: use get_contrast to calculate specific color with given pixel
    '''
    contrast_cielab = get_contrast(sampled_color)

    '''
    Coloring option two: use pick_lightness and a given text color
    Note: right now there's a bug I don't understand that insists on negating the color for the blue-yellow term... makes no sense
    '''
    contrast_cielab = pick_lightness(sampled_color[0], given_color[1], -given_color[2])
    

    # convert back to rgb
    contrast_rgb = color.lab2rgb(contrast_cielab) * 255

    '''
    for npix in neighboringPixels:
        avg_rgb += npix
    avg_rgb[0] /= len(neighboringPixels)
    '''
    labelColors.append(contrast_rgb)

# Color each pixel in the label text with contrasting color values
background_image2 = np.dstack((background_image.copy()[:,:,:3], 255*np.ones((background_image.shape[0], background_image.shape[1]))))

for i in range(len(label_coordinates)):
    coord = label_coordinates[i]
    label_rgb = labelColors[i]
    background_image2[coord[0], coord[1],0] = label_rgb[0]
    background_image2[coord[0], coord[1],1] = label_rgb[1]
    background_image2[coord[0], coord[1],2] = label_rgb[2]
    
background_image2 = background_image2/255

# Blur borders between color patches

blurred_image = cv2.blur(background_image2, (3, 3))
for i in range(len(label_coordinates)):
     coord = label_coordinates[i]
     label_blurred = blurred_image[coord[0], coord[1],:]
     background_image2[coord[0], coord[1],:] = label_blurred.clip(0,1)
pt.imsave("./results/color_contrast_test.png", .999*background_image2)
# # pt.show()

