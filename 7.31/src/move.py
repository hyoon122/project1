# 평행 이동
import os
import cv2
import numpy as np

# 이미지 불러오기
script_dir = os.path.dirname(os.path.abspath(__file__))
img_path = os.path.join(script_dir, '..', 'img', 'fish.jpg')
img_path = os.path.normpath(img_path)

# 경로 확인용
print(f"이미지 경로 확인: {img_path}")
print(f"존재 여부: {os.path.exists(img_path)}")

img = cv2.imread(img_path)
if img is None:
    print(f"이미지를 읽을 수 없습니다: {img_path}")
    exit()

rows, cols = img.shape[0:2] # 영상의 크기

dx, dy = 100, 50 # 이동할 픽셀 거리

# 변환 행렬
mtrx = np.float32([[1, 0, dx], [0, 1, dy]])

# 단순 이동
dst = cv2.warpAffine(img, mtrx, (cols + dx, rows + dy))

# 탈락된 외각 픽셀을 파랑색으로 보정
dst2 = cv2.warpAffine(img, mtrx, (cols + dx, rows + dy), None, cv2.INTER_LINEAR, cv2.BORDER_CONSTANT, (255, 0, 0))

# 탈락된 외각 픽셀을 원본으로 반사시켜서 보정
dst3 = cv2.warpAffine(img, mtrx, (cols + dx, rows + dy), None, cv2.INTER_LINEAR, cv2.BORDER_REFLECT)

cv2.imshow('original',img)
cv2.imshow('trains',dst)
cv2.imshow('BORDER_CONSTANT',dst2)
cv2.imshow('BORDER_REFLECT',dst3)
cv2.waitKey(0)
cv2.destroyAllWindows()