import numpy as np
from PIL import Image
from matplotlib import pyplot as pt
from color_labels import invert_hsv, rgb_to_hsv,hsv_to_rgb
from os import listdir
from os.path import isfile, join

def read_video_frames(filepath):
    files = [f for f in listdir(filepath) if isfile(join(filepath, f))]
    return files

def apply_hsv_transfer(file_names, label_file_name):
    # Load the label file
    label_image = np.asarray(Image.open('./img/' + label_file_name))[:,:,0]
    coordinates = np.mgrid[:label_image.shape[0], :label_image.shape[1]]
    label_pixels = label_image==255
    label_coordinates = coordinates[:, label_pixels]
    label_coordinates = np.array(list(zip(label_coordinates[0,:], label_coordinates[1,:])))
    
    for i in range(len(file_names)):
        background = np.asarray(Image.open('/Users/ashleykwon/Desktop/Color_Labels/video_frames/'+ file_names[i]))[:,:,:3]
        background_hsv = np.apply_along_axis(rgb_to_hsv, 2, background)
        background_hsv = [background_hsv[coord[0], coord[1], :] for coord in label_coordinates]
        label_hsv = [invert_hsv(val) for val in background_hsv]
        background_image2 = background.copy()[:,:,:3]
        for j in range(len(label_coordinates)):
            coord = label_coordinates[j]
            label_rgb = hsv_to_rgb(label_hsv[j])
            background_image2[coord[0], coord[1],:] = label_rgb
        pt.imsave("./results/"+file_names[i], background_image2)
    return('done')




file_names = read_video_frames('/Users/ashleykwon/Desktop/Color_Labels/video_frames')
result = apply_hsv_transfer(file_names, 'sample_text_video.png')

