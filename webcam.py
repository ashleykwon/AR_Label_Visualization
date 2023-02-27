import cv2
import numpy as np
import contrast
  
"""
Demo for creating visible text against video from the webcam
"""

TEXT_SCALE = 5
TEXT_THICKNESS = 20

vid = cv2.VideoCapture(0)
blur_amt = 85
goal_color = np.array([.25, .52, .96])
interp = 0.5

while(True):
    ret, frame = vid.read()

    if frame is None:
        print("frame not available")
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        continue
    
    frame = frame.astype(np.float32) / 255 # ensure values are between 0 and 1

    # create a new blank image and add our text
    text = np.zeros_like(frame)
    cv2.putText(img=text, 
                text="Sample Text", 
                org=(50, 200), 
                fontFace=cv2.FONT_HERSHEY_SIMPLEX, 
                fontScale=TEXT_SCALE, 
                color=(1, 1, 1), 
                thickness=TEXT_THICKNESS)
    
    # use red channel as alpha matte
    text_matte = np.repeat(text[:, :, 0], 3).reshape(text.shape)

    # use our custom function to increase contrast of text pixels
    contrast_bg = contrast.maximize_contrast_CIELAB(frame, scale=0.2, goal=goal_color, interp=interp)
    contrast_bg = cv2.GaussianBlur(contrast_bg, (blur_amt, blur_amt), 10)

    # add text on top of image using alpha matte
    composite = contrast_bg * text_matte + frame * (1 - text_matte)   
    cv2.imshow('frame', composite)

    # press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()