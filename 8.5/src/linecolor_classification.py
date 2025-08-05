# 실습 - 차선 색상 분류
# - 시각적 결과: 원본이미지 
# - 색상 팔레트: 추출된 3가지 대표 색상
# - 분포 차트: 각 색상이 차지하는 비율

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

def extract_line_colors(image_path, k=3):
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

    # 2. K-Means로 색상 클러스터링
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(reshaped_image)
    cluster_centers = kmeans.cluster_centers_.astype(int)
    labels = kmeans.labels_

    # 3. 각 클러스터 비율 계산
    _, counts = np.unique(labels, return_counts=True)
    ratios = counts / counts.sum()

    # 4. 시각화
    fig, axs = plt.subplots(1, 3, figsize=(18, 5))

    # 4.1 원본 이미지
    axs[0].imshow(image_rgb)
    axs[0].set_title("원본 이미지")
    axs[0].axis("off")

    # 4.2 색상 팔레트 (대표 색상)
    palette = np.zeros((50, 300, 3), dtype=np.uint8)
    start = 0
    for i, (color, ratio) in enumerate(zip(cluster_centers, ratios)):
        end = start + int(ratio * 300)
        palette[:, start:end] = color
        start = end
    axs[1].imshow(cv2.cvtColor(palette, cv2.COLOR_BGR2RGB))
    axs[1].set_title("색상 팔레트 (KMeans)")
    axs[1].axis("off")

    # 4.3 색상 분포 차트
    axs[2].bar(range(k), ratios, color=[color/255 for color in cluster_centers])
    axs[2].set_title("색상 분포 차트")
    axs[2].set_xlabel("클러스터 인덱스")
    axs[2].set_ylabel("비율")

    plt.tight_layout()
    plt.show()

    # 5. 상세 분석 출력
    print("상세 분석 결과")
    for i, (color, count, ratio) in enumerate(zip(cluster_centers, counts, ratios)):
        b, g, r = color
        print(f"클러스터 {i}: BGR=({b}, {g}, {r}), 픽셀 수={count}, 비율={ratio:.2%}")

# 사용 예시
if __name__ == "__main__":
    extract_line_colors()