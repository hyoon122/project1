# 실습 - 옷 색상 K-NN 분류

# 1. 개발 환경 준비
# 1-1. 필수 라이브러리 임포트
import cv2
import numpy as np
import csv
import os
from collections import Counter

# 1-2. 웹캠 연결 테스트 및 영상 출력
def webcam_test():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("웹캠을 열 수 없습니다.")
        return
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    print("웹캠 테스트 시작 - ESC 키를 눌러 종료하세요.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("프레임을 읽을 수 없습니다.")
            break
        
        cv2.imshow("Webcam Test", frame)
        key = cv2.waitKey(1)
        if key == 27:  # ESC 키
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    webcam_test()


# 2. 분류할 옷 색상 정의 및 라벨 매핑
color_labels = {
    1: 'Red',
    2: 'Blue',
    3: 'Green',
    4: 'Yellow',
    5: 'Black',
    6: 'White',
    7: 'Gray'
}

# 색상 데이터 저장 - CSV 저장 경로
csv_file = "color_dataset.csv"

# 함수 구상: K-NN 알고리즘 구현, CSV에서 데이터 파일을 읽고 저장하는 함수, 데이터셋 리셋 함수,
# 학습/테스트 데이터 분할 함수, 정확도 계산 함수, 마우스 이벤트 콜백 함수, ROI 영역의 평균 RGB 추출 함수,
# 아따 드럽게많네

# 3. K-NN 알고리즘 직접 구현
class KNNClassifier:
    def __init__(self, k=3):
        self.k = k  # 최근접 이웃 개수 설정
    
    def fit(self, X_train, y_train):
        # 학습 데이터 저장 (K-NN은 비모수 학습이라 별도 학습 과정 없음)
        self.X_train = X_train
        self.y_train = y_train
    
    def _euclidean_distance(self, x1, x2):
        # 유클리드 거리 계산 함수
        return np.linalg.norm(x1 - x2)
    
    def predict(self, X_test):
        # 다수의 테스트 샘플에 대해 예측 수행
        predictions = []
        for test_point in X_test:
            # 각 학습 데이터와 거리 계산
            distances = [self._euclidean_distance(test_point, x) for x in self.X_train]
            # 거리 기준 상위 k개 인덱스 추출
            k_indices = np.argsort(distances)[:self.k]
            k_labels = self.y_train[k_indices]
            # 가장 빈도 높은 라벨을 예측값으로 선택
            most_common = Counter(k_labels).most_common(1)[0][0]
            predictions.append(most_common)
        return np.array(predictions)
    
    def predict_proba(self, X_test):
        # 각 테스트 샘플에 대해 확률(비율) 계산
        prob_list = []
        for test_point in X_test:
            distances = [self._euclidean_distance(test_point, x) for x in self.X_train]
            k_indices = np.argsort(distances)[:self.k]
            k_labels = self.y_train[k_indices]
            count = Counter(k_labels)
            probs = {label: count[label]/self.k for label in count}  # 각 라벨의 비율
            prob_list.append(probs)
        return prob_list
    