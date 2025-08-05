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

