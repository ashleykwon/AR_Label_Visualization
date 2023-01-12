import numpy as np
from PIL import Image
from matplotlib import pyplot as pt
import cv2
import math
import palette_based_color_assignment as pbca

'''
Generate a label color based on one of the 2 methods using the HSV color space
'''
def invert_hsv(background_hsv, value_variance, value_variance_average):
    # Method 1: Saturation-based color assignment
    # new_h = 0
    # new_v = 1
    # new_s = abs(1 - background_hsv[1])
    # # If a background pixel has a saturation value that is larger than 0.5, then use hue to assign label pixel colors
    # if background_hsv[1] >= 0.5:
    #     new_h = (background_hsv[0] + 180)%360 
    # # Else, use value to assign label pixel colors
    # else:
    #     new_v = 1-background_hsv[2]

    # Method 2: Value based
    new_h = 0
    new_s = 0
    new_v = 1
   
    # # If at a pixel location, variance is more than other pixels', 
    # then modify the hue and saturation instead
    if value_variance > value_variance_average:
        new_h = (background_hsv[0] + 180)%360 
        new_s = 1-background_hsv[1]

    # Else, take the opposite of the value and make that the new color
    else: 
        if background_hsv[2] > 0.5:
            new_v = 0
        else:
            new_v = 1

    return [new_h, new_s, new_v]



'''
Generate a map showing value variances throughout different neighborhoods of the input image
'''
def sample_pixels(background_image_hsv, sample_size):
    value_variance_map = np.zeros((background_image_hsv.shape[0], background_image_hsv.shape[1]))
    square = np.ones((sample_size, sample_size))
    for i in range(background_image_hsv.shape[0]//sample_size):
        for j in range(background_image_hsv.shape[1] // sample_size):
            value_variance_map[i*sample_size:i*sample_size+sample_size, j*sample_size:j*sample_size+sample_size] = np.var(background_image_hsv[:,:,2][i*sample_size:i*sample_size+sample_size, j*sample_size:j*sample_size+sample_size])*square
    pt.imsave("value_variance_map_" + str(sample_size) + ".png", value_variance_map, cmap = "gray")
    return value_variance_map



'''
Generate a label color based on inversions in the HSL color space
'''
def invert_hsl(background_hsl):
    new_h =  (background_hsl[0] + 180)%360 
    new_s = abs(1 - background_hsl[1])
    new_l = abs(1 - background_hsl[2])
    return [new_h, new_s, new_l]


'''
Convert an rgb pixel value to an hsv pixel value
'''
def rgb_to_hsv(rgb):
    r = rgb[0]/255
    g = rgb[1]/255
    b = rgb[2]/255

    h=0
    s=0
    v=0
    
    max_rgb = max(r,g,b)
    min_rgb = min(r,g,b)
    min_max_diff = max_rgb-min_rgb

    # Set hue
    if min_max_diff == 0:
        h =0
    elif max_rgb == r:
        h = 60*(((g-r)/min_max_diff)%6)
    elif max_rgb == g:
        h = 60*(((b-r)/min_max_diff) + 2)
    elif max_rgb == b:
        h = 60*(((r-g)/min_max_diff) + 4)

    # Set saturation
    if max_rgb == 0:
        s = 0
    else:
        s = min_max_diff/max_rgb

    # Set value
    v = max_rgb

    return np.asarray([h,s,v])



'''
Convert an hsv pixel value to an rgb pixel value
'''
def hsv_to_rgb(hsv):
    h = hsv[0]
    s = hsv[1]
    v = hsv[2]

    C = v*s
    X = C*(1 - abs((h/60)%2 -1))
    m = v-C

    rgb_prime = np.asarray([0,0,0])

    if 0 <= h < 60:
        rgb_prime = np.asarray([C, X, 0])
    elif 60 <= h < 120: 
        rgb_prime = np.asarray([X, C, 0])
    elif 120 <= h < 180:
        rgb_prime = np.asarray([0, C, X])
    elif 180 <= h < 240: 
        rgb_prime = np.asarray([0, X, C])
    elif 240 <= h < 300:
        rgb_prime = np.asarray([X, 0, C])
    elif 300 <= h < 360:
        rgb_prime = np.asarray([C, 0, X])

    rgb = np.asarray([(rgb_prime[0]+m)*255, (rgb_prime[1]+m)*255, (rgb_prime[2]+m)*255])
    return rgb


'''
Convert an rgb pixel value to an hsl pixel value
'''
def rgb_to_hsl(rgb):
    r = rgb[0]/255
    g = rgb[1]/255
    b = rgb[2]/255

    h=0
    s=0
    l=0
    
    max_rgb = max(r,g,b)
    min_rgb = min(r,g,b)
    min_max_diff = max_rgb-min_rgb

    # Set hue
    if min_max_diff == 0:
        h =0
    elif max_rgb == r:
        h = 60*(((g-r)/min_max_diff)%6)
    elif max_rgb == g:
        h = 60*(((b-r)/min_max_diff) + 2)
    elif max_rgb == b:
        h = 60*(((r-g)/min_max_diff) + 4)

    # Set saturation
    if max_rgb == 0:
        s = 0
    else:
        s = min_max_diff/max_rgb

    # Set lightness
    l = (max_rgb + min_rgb)/2
    return np.asarray([h,s,l])

'''
Convert an hsl pixel value to an rgb pixel value
'''
def hsl_to_rgb(hsl):
    h = hsl[0]
    s = hsl[1]
    l = hsl[2]

    r = 0
    g = 0
    b = 0

    C = (1 - abs(2*l - 1))*s
    H_prime = h/60
    X = C*(1 - abs(H_prime%2 -1))
    if 0 <= H_prime <1:
        r = C
        g = X
        b = 0
    elif 1 <= H_prime < 2:
        r = X
        g = C
        b = 0
    elif 2 <= H_prime < 3:
        r = 0
        g = C
        b = X
    elif 3 <= H_prime < 4:
        r = 0
        g = X
        b = C
    elif 4 <= H_prime < 5:
        r = X
        g = 0
        b = C
    elif 5 <= H_prime < 6:
        r = C
        g = 0
        b = X
    
    m = l - C/2
    return np.asarray([r+m, g+m, b+m])

'''
Convert RGB (0-255) to CIEXYZ
'''
def rgb_to_ciexyz(rgb):
    rgbLinear = rgb_linear(rgb)
    return np.array([
        [0.4124, 0.3576, 0.1805], 
        [0.2126, 0.7157, 0.0722], 
        [0.0193, 0.1192, 0.9505]])@rgbLinear


'''
Helper function for rgb_to_ciexyz that determines which C_linear value to use 
where C is R, G, or B
Derived from this article: https://en.wikipedia.org/wiki/SRGB#From_sRGB_to_CIE_XYZ
'''
def rgb_linear(rgb):
    val_to_return = np.zeros((3))
    for i in range(3):
        normalized_rgb = rgb[i]/255
        if normalized_rgb <= 0.04045:
            val_to_return[i] = normalized_rgb/12.92
        else:
            val_to_return[i] = ((normalized_rgb + 0.055)/1.055)**2.4
    return val_to_return

'''
Convert CIEXYZ to RGB
'''
def ciexyz_to_rgb(ciexyz):
    rgb_linear = np.array([
    [3.2406, -1.5372, -0.4986], 
    [-0.9689, 1.8758, 0.0415], 
    [0.0557, -0.2040, 1.0570]])@ciexyz
    return rgb_srgb(rgb_linear)

'''
Helper function for rgb_linear to srgb conversion 
'''
def rgb_srgb(rgb_linear):
    val_to_return = np.zeros((3))
    for i in range(3):
        if rgb_linear[i] <= 0.0031308:
            val_to_return[i] = rgb_linear[i]*12.92
        else:
            val_to_return[i] = 1.055*(rgb_linear[i]**(1/2.4)) - 0.055
    return val_to_return


# Load the background image 
background_name = "sample_scene.jpg"
background_image = np.asarray(Image.open('./img/'+background_name))[:,:,:3]

# Convert background image to hsv
background_image_hsv = np.apply_along_axis(rgb_to_hsv, 2, background_image)

# Convert background image to hsl
# background_image_hsl = np.apply_along_axis(rgb_to_hsl, 2, background_image)


# # Testing the hsv to rgb conversion, and vice versa. The conversion works well.
# background_image_rgb =  np.apply_along_axis(ciexyz_to_rgb, 2, background_image_hsv)
# pt.imshow(background_image_rgb.astype('uint8'))

# # Load the label image (white label on a black background)
label_name = "sample_text_video.png"
label_image = np.asarray(Image.open('./img/'+ label_name))[:,:,0]
# pt.imshow(label_image)
# pt.show()

# # Get the coordinates of pixels that belong to the label
coordinates = np.mgrid[:label_image.shape[0], :label_image.shape[1]]
label_pixels = label_image==255
label_coordinates = coordinates[:, label_pixels]
label_coordinates = np.array(list(zip(label_coordinates[0,:], label_coordinates[1,:])))

# Derive variance map
value_variance_map = sample_pixels(background_image_hsv, 50)
# pt.imshow(value_variance_map, cmap = "gray")


# # Get hsv values of pixels at the corresponding coordinates from the background image
background_hsv = [background_image_hsv[coord[0], coord[1], :] for coord in label_coordinates]

selected_value_variances = [value_variance_map[coord[0], coord[1]] for coord in label_coordinates]


# Get hsl values of pixels at the corresponding coordinates from the background image
# background_hsl = [background_image_hsl[coord[0], coord[1], :] for coord in label_coordinates]

# Generate inverse HSV values of extracted pixel values
label_hsv = [invert_hsv(background_hsv[i], selected_value_variances[i], np.percentile(value_variance_map, 95)) for i in range(len(background_hsv))]

# Generate inverse HSL values of extracted pixel values
# label_hsl = [invert_hsl(val) for val in background_hsl]

# Generate a palette and assign label pixel values based on distances between colors in the palette and sampled background pixels
# Please note that I used a hard-coded palette here. I have yet to debug the palette generator function in palette_based_color_assignment.py
palette = [[0,0,0], [255,0,0], [0,255,0], [255,255,0], [0,0,255],[255,0,255],[0,255,255],[255,255,255]]
labelColors = []
for i in range(len(label_coordinates)):
    neighboringPixelCoordinates= pbca.sample_pixels(label_coordinates[i])
    labelColors.append(pbca.find_maximum_distance(background_image, neighboringPixelCoordinates, palette))

# Color each pixel in the label text with the inverse HSV values
background_image2 = np.dstack((background_image.copy()[:,:,:3], 255*np.ones((background_image.shape[0], background_image.shape[1]))))
for i in range(len(label_coordinates)):
    coord = label_coordinates[i]
    # label_rgb = hsv_to_rgb(label_hsv[i])
    label_rgb = labelColors[i]
    # background_image2[coord[0], coord[1],:3] = np.asarray([0,0,0]) #set all label pixel colors to black (for testing only)
    background_image2[coord[0], coord[1],0] = label_rgb[0]
    background_image2[coord[0], coord[1],1] = label_rgb[1]
    background_image2[coord[0], coord[1],2] = label_rgb[2]

# Blur borders between color patches
# blurred_image = cv2.blur(background_image2, (5, 5))
# for i in range(len(label_coordinates)):
#     coord = label_coordinates[i]
#     label_blurred = blurred_image[coord[0], coord[1],:]
#     background_image2[coord[0], coord[1],:] = label_blurred

background_image2 = background_image2/255
#Check that label colors are assigned correctly when all label pixel colors are set to black
for j in range(len(label_coordinates)):
    coord = label_coordinates[j]
    if (background_image2[coord[0], coord[1],0] != 0) or (background_image2[coord[0], coord[1],1] != 0) or (background_image2[coord[0], coord[1],2] != 0) or (background_image2[coord[0], coord[1],3] != 1):
        print(background_image2[coord[0], coord[1],:])
pt.imsave("./results/"+background_name+"_palette_based.jpg", background_image2)
# # pt.show()


