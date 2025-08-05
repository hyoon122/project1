# 실습 - 옷 색상 K-NN 분류

# 1. 개발 환경 준비
# 1-1. 필수 라이브러리 임포트
import cv2
import numpy as np
import matplotlib.pyplot as plt
import csv
import os

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