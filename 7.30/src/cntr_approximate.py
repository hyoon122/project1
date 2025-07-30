# 근사 컨투어 (cntr_approximate.py)

import os
import cv2
import numpy as np

script_dir = os.path.dirname(os.path.abspath(__file__))  # 현재 파일의 위치
img_path = os.path.join(script_dir, '..', 'img', 'bad_rect.png')
img = cv2.imread(os.path.normpath(img_path))
if img is None:
    raise FileNotFoundError("이미지를 불러올 수 없습니다. 경로를 확인하세요.")
img2 = img.copy()


# 그레이 스케일과 바이너리 스케일 변환
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
ret, th = cv2.threshold(imgray, 127, 255, cv2.THRESH_BINARY)

# 컨투어 찾기
temp = th.copy()
contours, hierachy = cv2.findContours(temp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contour = contours[0]

# 전체 둘레의 0.05로 오차 범위 지정
epsilon = 0.05 * cv2.arcLength(contour, True)

# 근사 컨투어 계산
approx = cv2.approxPolyDP(contour, epsilon, True)

# 각각 컨투어 선 그리기
cv2.drawContours(img, [contour], -1, (0,255,0), 3)
cv2.drawContours(img2, [approx], -1, (0,255,0), 3)

# 결과 출력
cv2.imshow('contour', img)
cv2.imshow('approx', img2)
cv2.waitKey()
cv2.destroyAllWindows()