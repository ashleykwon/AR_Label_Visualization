import numpy as np
import cv2
from contrast import increase_contrast

# demo for using contrast.py functions to create an image
 
bg = cv2.imread("./img/sample_scene.jpg")
text = np.zeros_like(bg)
cv2.putText(text, "Sample Text", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 10, cv2.LINE_AA)

contrast_text = increase_contrast(bg, text)

text_matte = np.repeat(text[:, :, 0] / 255, 3).reshape(text.shape)
composite = contrast_text * text_matte + bg * (1 - text_matte)
cv2.imwrite("./results/sample_scene_contrast.jpg", composite)
