import numpy as np
import cv2
import contrast
from skimage import color

# demo for using contrast.py functions to create an image
filename = "sample_scene.jpg"
blur_amt = 35

bg = cv2.imread(f"./img/{filename}") / 255
text = np.zeros_like(bg)

cv2.putText(text, "Sample Text", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 3, (1, 1, 1), 10, cv2.LINE_AA)

text_matte = np.repeat(text[:, :, 0], 3).reshape(text.shape)
# contrast_HSV = contrast.increase_contrast_HSV(bg)
# contrast_CIELAB = contrast.increase_contrast_CIELAB_naive(bg)
contrast_LAB = contrast.increase_contrast_CIELAB(bg, scale=0.2, goal=np.array([.25, .52, .96]), interp=0.5)
contrast_LAB = cv2.GaussianBlur(contrast_LAB, (blur_amt, blur_amt), 10)

composite_LAB = contrast_LAB * text_matte + bg * (1 - text_matte)
# cv2.imwrite("./results/sample_scene_contrast_HSV.jpg", (composite_HSV * 255).astype(int))
# cv2.imwrite("./results/sample_scene_contrast_CIELAB.jpg", (composite_CIELAB * 255).astype(int))
cv2.imwrite("./results/max_contrast_LAB.jpg", (composite_LAB * 255).astype(int))
