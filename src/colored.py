import os
print("현재 작업 디렉토리:", os.getcwd())

import cv2
import numpy as np

# 기본값
img = cv2.imread('../img/color_like_lenna.png')

# BGR
bgr = cv2.imread('../img/color_like_lenna.png', cv2.IMREAD_COLOR)

# a
bgra = cv2.imread('../img/color_like_lenna.png', cv2.IMREAD_UNCHANGED)

# shape
print("default", img.shape, "color", bgr.shape, "unchanged", bgra.shape)

cv2.imshow('img', img)
cv2.imshow('bgr', bgr)
cv2.imshow('alphpa', bgra[:, :, 3])

cv2.waitKey(0)
cv2.destroyAllWindows()
