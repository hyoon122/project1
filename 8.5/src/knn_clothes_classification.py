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
# 학습/테스트 데이터 분할 함수, 정확도 계산 함수

# 4~5단계: 마우스 이벤트 콜백 함수, ROI 영역의 평균 RGB 추출 함수
# + 메인루프 작성 필요.
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
    
# CSV 파일에서 데이터 읽기
def load_dataset(csv_path):
    data, labels = [], []
    if not os.path.exists(csv_path):
        return np.array(data), np.array(labels)
    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # 0~255 RGB 값을 0~1 범위로 정규화하여 저장
            r = float(row['R']) / 255.0
            g = float(row['G']) / 255.0
            b = float(row['B']) / 255.0
            label = int(row['Label'])
            data.append([r, g, b])
            labels.append(label)
    return np.array(data), np.array(labels)

# CSV에 데이터 샘플 저장
def save_samples(samples, filename=csv_file):
    header = ['R', 'G', 'B', 'Label']
    write_header = not os.path.exists(filename)
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(header)
        writer.writerows(samples)

# 데이터셋 리셋(삭제)
def reset_dataset(filename=csv_file):
    if os.path.exists(filename):
        os.remove(filename)
        print("데이터셋이 리셋되었습니다.")
        
# 학습/테스트 데이터 분할 함수
def train_test_split(X, y, test_ratio=0.2):
    indices = np.arange(len(X))
    np.random.shuffle(indices)
    test_size = int(len(X)*test_ratio)
    test_idx = indices[:test_size]
    train_idx = indices[test_size:]
    return X[train_idx], X[test_idx], y[train_idx], y[test_idx]

# 정확도 계산
def accuracy_score(y_true, y_pred):
    return np.sum(y_true == y_pred) / len(y_true)

# 최적 k 찾기
def find_best_k(X_train, y_train, X_test, y_test, k_values=[3,5,7,9]):
    best_k, best_acc = k_values[0], 0
    for k in k_values:
        knn = KNNClassifier(k=k)
        knn.fit(X_train, y_train)
        pred = knn.predict(X_test)
        acc = accuracy_score(y_test, pred)
        print(f"K={k}, 정확도: {acc:.3f}")
        if acc > best_acc:
            best_acc = acc
            best_k = k
    return best_k, best_acc

# 전역 변수
current_label = None  # 현재 선택된 색상 라벨
samples = []          # 학습 샘플 임시 저장소
mode = "Collect"      # 모드 상태 ("Collect" 또는 "Predict")
roi_size = 100        # ROI 크기 (100x100)
roi_x, roi_y = 270, 190  # ROI 좌상단 위치
dragging = False      # ROI 드래그 상태
offset_x, offset_y = 0, 0  # 마우스 드래그 오프셋
model = None          # K-NN 모델 객체
best_k = 3            # 최적 k값
X_train, y_train = None, None  # 학습 데이터
accuracy = 0.0        # 모델 정확도
history = []          # 최근 예측 결과 저장(최대 10개)

# 4. 마우스 이벤트 콜백 함수
def mouse_callback(event, x, y, flags, param):
    global samples, current_label, dragging, roi_x, roi_y, offset_x, offset_y
    
    if mode == "Collect":
        # 학습 모드에서는 좌클릭 시 해당 픽셀의 RGB값 저장
        if event == cv2.EVENT_LBUTTONDOWN:
            if current_label is None:
                print("먼저 숫자 키 1~7로 라벨을 선택하세요.")
                return
            frame = param
            bgr = frame[y, x]
            rgb = bgr[::-1]  # BGR -> RGB 변환
            samples.append([rgb[0], rgb[1], rgb[2], current_label])
            print(f"샘플 수집: {color_labels[current_label]} - 총 {len(samples)}개")
            
    elif mode == "Predict":
        # 예측 모드에서는 ROI 사각형 드래그 이동 가능
        if event == cv2.EVENT_LBUTTONDOWN:
            # ROI 내부에서 클릭 시 드래그 시작
            if roi_x <= x <= roi_x + roi_size and roi_y <= y <= roi_y + roi_size:
                dragging = True
                offset_x = x - roi_x
                offset_y = y - roi_y
        elif event == cv2.EVENT_MOUSEMOVE and dragging:
            # 드래그 중이면 ROI 위치 갱신
            roi_x = x - offset_x
            roi_y = y - offset_y
            # 화면 밖으로 나가지 않도록 제한
            roi_x = max(0, min(roi_x, 640 - roi_size))
            roi_y = max(0, min(roi_y, 480 - roi_size))
        elif event == cv2.EVENT_LBUTTONUP:
            dragging = False

# ROI 영역의 평균 RGB 추출 및 예측 수행
def predict_roi_color(frame):
    global model, roi_x, roi_y, roi_size
    roi = frame[roi_y:roi_y+roi_size, roi_x:roi_x+roi_size]
    mean_bgr = cv2.mean(roi)[:3]  # 평균 BGR 값
    mean_rgb = np.array([mean_bgr[2]/255.0, mean_bgr[1]/255.0, mean_bgr[0]/255.0])  # 정규화된 RGB
    pred_label = model.predict(np.array([mean_rgb]))[0]
    proba_dict = model.predict_proba(np.array([mean_rgb]))[0]
    return pred_label, proba_dict
