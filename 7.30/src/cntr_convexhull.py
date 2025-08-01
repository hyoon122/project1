# 볼록 선체 (cntr_convexhull.py)

import os
import cv2
import numpy as np

script_dir = os.path.dirname(os.path.abspath(__file__))  # 현재 파일의 위치
img_path = os.path.join(script_dir, '..', 'img', 'hand.jpg')
img = cv2.imread(os.path.normpath(img_path))
if img is None:
    raise FileNotFoundError("이미지를 불러올 수 없습니다. 경로를 확인하세요.")
img2 = img.copy()

# 그레이 스케일 및 바이너리 스케일 변환
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, th = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

# 컨투어 찾기와 그리기
temp = th.copy()
contours, heiarchy = cv2.findContours(temp, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cntr = contours[0]
cv2.drawContours(img, [cntr], -1, (0, 255,0), 1)

# 볼록 선체 찾기(좌표 기준)와 그리기
hull = cv2.convexHull(cntr)
cv2.drawContours(img2, [hull], -1, (0,255,0), 1)

# 볼록 선체 만족 여부 확인
print(cv2.isContourConvex(cntr), cv2.isContourConvex(hull))

# 볼록 선체 찾기(인덱스 기준)
hull2 = cv2.convexHull(cntr, returnPoints=False)

# 볼록 선체 결함 찾기
defects = cv2.convexityDefects(cntr, hull2)

# 볼록 선체 결함 순회
for i in range(defects.shape[0]):
    # 시작, 종료, 가장 먼 지점, 거리
    startP, endP, farthestP, distance = defects[i, 0]
    # 가장 먼 지점의 좌표 구하기
    farthest = tuple(cntr[farthestP][0])
    # 거리를 부동 소수점으로 변환
    dist = distance/256.0
    # 거리가 1보다 큰 경우
    if dist > 1 :
        # 빨강색 점 표시 
        cv2.circle(img2, farthest, 3, (0,0,255), -1)
        
# 결과 이미지 표시
cv2.imshow('contour', img)
cv2.imshow('convex hull', img2)
cv2.waitKey(0)
cv2.destroyAllWindows()
