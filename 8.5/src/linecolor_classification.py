# 실습 - 차선 색상 분류
# - 시각적 결과: 원본이미지 
# - 색상 팔레트: 추출된 3가지 대표 색상
# - 분포 차트: 각 색상이 차지하는 비율

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

def extract_lane_colors(image_path, k=3):
    # 1. 이미지 로드 (BGR)
    # 이미지 불러오기
    script_dir = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(script_dir, '..', 'img', 'load_line.jpg')
    img_path = os.path.normpath(img_path)

    # 경로 확인용
    print(f"이미지 경로 확인: {img_path}")
    print(f"존재 여부: {os.path.exists(img_path)}")

    image = cv2.imread(img_path)
    if image is None:
        print(f"이미지를 읽을 수 없습니다: {img_path}")
        exit()
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    reshaped_image = image.reshape((-1, 3))

    