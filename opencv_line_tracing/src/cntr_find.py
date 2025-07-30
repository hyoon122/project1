# 컨투어 찾기와 그리기 (cntr_find.py)

import os
import cv2
import numpy as np

script_dir = os.path.dirname(os.path.abspath(__file__))  # 현재 파일의 위치
img_path = os.path.join(script_dir, '..', 'img', 'shapes.png')
img = cv2.imread(os.path.normpath(img_path))
if img is None:
    raise FileNotFoundError("이미지를 불러올 수 없습니다. 경로를 확인하세요.")
img2 = img.copy()

# 그레이 스케일
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 스레시홀드로 바이너리 이미지를 만들어서 검은배경에 흰색전경으로 반전
ret, imthres = cv2.threshold(imgray, 127, 255, cv2.THRESH_BINARY_INV)

# 가장 바깥쪽 컨투어에 대해 모든 좌표 변환
im2 = imthres.copy()
contours, hierarchy = cv2.findContours(im2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 가장 바깥쪽 컨투어에 대해 꼭지점 좌표만 반환
im2 = imthres.copy()
contour2, hierarchy = cv2.findContours(im2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# 각각의 컨투의 갯수 출력 ---⑤
print('도형의 갯수: %d(%d)'% (len(contours), len(contour2)))

# 모든 좌표를 갖는 컨투어 그리기, 초록색
cv2.drawContours(img, contours, -1, (0,255,0), 4)
# 꼭지점 좌표만을 갖는 컨투어 그리기, 초록색
cv2.drawContours(img2, contour2, -1, (0,255,0), 4)

# 컨투어 모든 좌표를 작은 파랑색 점(원)으로 표시
for i in contours:
    for j in i:
        cv2.circle(img, tuple(j[0]), 1, (255,0,0), -1) 

# 컨투어 꼭지점 좌표를 작은 파랑색 점(원)으로 표시
for i in contour2:
    for j in i:
        cv2.circle(img2, tuple(j[0]), 1, (255,0,0), -1) 

# 결과 출력
cv2.imshow('CHAIN_APPROX_NONE', img)
cv2.imshow('CHAIN_APPROX_SIMPLE', img2)

cv2.waitKey(0)
cv2.destroyAllWindows()