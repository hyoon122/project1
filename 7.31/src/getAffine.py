# 어핀 변환 (getAffine.py)
import os
import cv2
import numpy as np
from matplotlib import pyplot as plt

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

rows, cols = img.shape[:2]

# ---① 변환 전, 후 각 3개의 좌표 생성
pts1 = np.float32([[100, 50], [200, 50], [100, 200]])
pts2 = np.float32([[80, 70], [210, 60], [250, 120]])

# ---② 변환 전 좌표를 이미지에 표시
cv2.circle(img, (100,50), 5, (255,0), -1)
cv2.circle(img, (200,50), 5, (0,255,0), -1)
cv2.circle(img, (100,200), 5, (0,0,255), -1)

#---③ 짝지은 3개의 좌표로 변환 행렬 계산
mtrx = cv2.getAffineTransform(pts1, pts2)
#---④ 어핀 변환 적용
dst = cv2.warpAffine(img, mtrx, (int(cols*1.5), rows))

#---⑤ 결과 출력
cv2.imshow('origin',img)
cv2.imshow('affin', dst)
cv2.waitKey(0)
cv2.destroyAllWindows()