import numpy as np
import cv2
import contrast

# demo for using contrast.py functions to create an image
filename = "sample_scene.jpg"
blur_amt = 85

bg = cv2.imread(f"./img/{filename}") / 255
text = np.zeros_like(bg)

cv2.putText(text, "Sample Text", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 3, (1, 1, 1), 10, cv2.LINE_AA)
text_matte = np.repeat(text[:, :, 0], 3).reshape(text.shape)
# contrast_text_HSV = contrast.increase_contrast_HSV(bg)
# contrast_text_CIELAB = contrast.increase_contrast_CIELAB(bg)
max_contrast_text_CIELAB = contrast.maximize_contrast_CIELAB(bg)
max_contrast_text_CIELAB = cv2.GaussianBlur(max_contrast_text_CIELAB, (blur_amt, blur_amt), 10)
# max_contrast_text_CIELAB


# composite_HSV = contrast_text_HSV * text_matte + bg * (1 - text_matte)
# composite_CIELAB = contrast_text_CIELAB * text_matte + bg * (1 - text_matte)
composite_CIELAB2 = max_contrast_text_CIELAB * text_matte + bg * (1 - text_matte)
# cv2.imwrite("./results/sample_scene_contrast_HSV.jpg", (composite_HSV * 255).astype(int))
# cv2.imwrite("./results/sample_scene_contrast_CIELAB.jpg", (composite_CIELAB * 255).astype(int))
cv2.imwrite("./results/max_contrast_LAB.jpg", (composite_CIELAB2 * 255).astype(int))
