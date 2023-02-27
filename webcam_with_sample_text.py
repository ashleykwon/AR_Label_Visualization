import cv2
import numpy as np
import cielab_contrast_gen
from PIL import Image
from skimage import io, color

  
"""
Demo for creating visible text against video from the webcam
"""

vid = cv2.VideoCapture(0)
goal_color = color.rgb2lab(np.array([.25, .52, .96]))
interp = 0.5

label_name = "sample_text_2.png"
label_image = np.asarray(Image.open('./labels/'+ label_name))[:,:,0]
img_size = label_image.shape
coordinates = np.mgrid[:label_image.shape[0], :label_image.shape[1]]
label_pixels = label_image==255
label_coordinates = coordinates[:, label_pixels]
label_coordinates = np.array(list(zip(label_coordinates[0,:], label_coordinates[1,:])))

vid.set(cv2.CAP_PROP_FRAME_WIDTH, img_size[1])
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, img_size[0])

while(True):
    ret, frame = vid.read()

    if frame is None:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        continue
    
    frame = frame.astype(np.float32) / 255 # ensure values are between 0 and 1
    as_lab = color.rgb2lab(frame) 
    blurred_image = cv2.blur(as_lab, (5, 5))
    #background_image2 = np.dstack((frame.copy()[:,:,:3], np.ones((frame.shape[0], frame.shape[1]))))

    for coord in label_coordinates:
        sampled_color = as_lab[coord[0], coord[1]]
        contrast_cielab = cielab_contrast_gen.pick_lightness(sampled_color[0], goal_color[1], -goal_color[2])
        #contrast_cielab = cielab_contrast_gen.get_contrast(sampled_color)
        as_lab[coord[0], coord[1], :3] = contrast_cielab
    

    cv2.imshow('frame', color.lab2rgb(as_lab))

    # press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()