import numpy as np
import cv2
from contrast import increase_contrast_HSV

# demo for using contrast.py functions to create an image
filename = "sample_scene.jpg"
bg = cv2.imread(f"./img/{filename}") / 255
text = np.zeros_like(bg)
cv2.putText(text, "Sample Text", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 3, (1, 1, 1), 10, cv2.LINE_AA)

contrast_text = increase_contrast_HSV(bg)

text_matte = np.repeat(text[:, :, 0], 3).reshape(text.shape)
composite = contrast_text * text_matte + bg * (1 - text_matte)
cv2.imwrite("./results/sample_scene_contrast.jpg", (composite * 255).astype(int))
