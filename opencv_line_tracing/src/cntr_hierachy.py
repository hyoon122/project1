# 컨투어 계층 트리 (cntr_hierachy.py)

import os
import cv2
import numpy as np

# 영상 읽기
script_dir = os.path.dirname(os.path.abspath(__file__))  # 현재 파일의 위치
img_path = os.path.join(script_dir, '..', 'img', 'shapes_donut.png')
img = cv2.imread(os.path.normpath(img_path))
if img is None:
    raise FileNotFoundError("이미지를 불러올 수 없습니다. 경로를 확인하세요.")
img2 = img.copy()

# 바이너리 이미지로 변환
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, imthres = cv2.threshold(imgray, 127, 255, cv2.THRESH_BINARY_INV)

# 가장 바깥 컨투어만 수집
im2 = imthres.copy()
contour, hierarchy = cv2.findContours(im2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# 컨투어 갯수와 계층 트리 출력
print(len(contour), hierarchy)

# 모든 컨투어를 트리 계층 으로 수집
im2 = imthres.copy()
contour2, hierarchy = cv2.findContours(im2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# 컨투어 갯수와 계층 트리 출력
print(len(contour2), hierarchy)

# 가장 바깥 컨투어만 그리기
cv2.drawContours(img, contour, -1, (0,255,0), 3)

# 모든 컨투어 그리기
for idx, cont in enumerate(contour2): 
    # 랜덤한 컬러 추출
    color = [int(i) for i in np.random.randint(0,255, 3)]
    # 컨투어 인덱스 마다 랜덤한 색상으로 그리기
    cv2.drawContours(img2, contour2, idx, color, 3)
    # 컨투어 첫 좌표에 인덱스 숫자 표시
    cv2.putText(img2, str(idx), tuple(cont[0][0]), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255))

# 화면 출력
cv2.imshow('RETR_EXTERNAL', img)
cv2.imshow('RETR_TREE', img2)
cv2.waitKey(0)
cv2.destroyAllWindows()