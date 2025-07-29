import cv2
import numpy as np

img = cv2.imread('../img/color_like_lenna.png')

img2 = img.astype(np.uint16)
b,g,r = cv2.split(img2) # 채널별로 분류
gray1 = ((b + g + r) / 3).astype(np.uint8) # 평균값을 연산 후 dtype 변경

cv2.imshow('original', img)
cv2.imshow('gray1', gray1)

cv2.waitKey(0)
cv2.destroyAllWindows()