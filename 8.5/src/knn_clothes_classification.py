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


# 2-1. 분류할 옷 색상 정의 및 라벨 매핑
color_labels = {
    1: 'Red',
    2: 'Blue',
    3: 'Green',
    4: 'Yellow',
    5: 'Black',
    6: 'White',
    7: 'Gray'
}

# CSV 저장 경로
csv_file = "color_dataset.csv"

# 샘플 데이터 저장 리스트 (RGB + label)
samples = []

# 2-2. 클릭한 위치의 픽셀 RGB값 추출용 이벤트 핸들러
def mouse_callback(event, x, y, flags, param):
    global frame, current_label, samples
    
    if event == cv2.EVENT_LBUTTONDOWN:
        # BGR to RGB 변환
        bgr = frame[y, x]
        rgb = bgr[::-1]  # BGR -> RGB
        
        hsv = cv2.cvtColor(np.uint8([[bgr]]), cv2.COLOR_BGR2HSV)[0][0]

        print(f"픽셀 위치: ({x}, {y}), RGB: {rgb}, HSV: {hsv}, 현재 라벨: {current_label} - {color_labels.get(current_label, 'None')}")
        
        if current_label in color_labels:
            samples.append([rgb[0], rgb[1], rgb[2], current_label])
            print(f"샘플 수집 완료 - 총 샘플 수: {len(samples)}")

# 2-3. 샘플 저장 함수
def save_samples():
    # CSV 파일로 저장
    header = ['R', 'G', 'B', 'Label']
    if os.path.exists(csv_file):
        mode = 'a'
        write_header = False
    else:
        mode = 'w'
        write_header = True
    
    with open(csv_file, mode, newline='') as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(header)
        writer.writerows(samples)
    print(f"{len(samples)}개의 샘플을 '{csv_file}' 파일에 저장했습니다.")

# 2-4. 색 읽기 함수
def collect_color_samples():
    global frame, current_label, samples
    current_label = None
    
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("웹캠을 열 수 없습니다.")
        return
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    cv2.namedWindow("Color Sample Collection")
    cv2.setMouseCallback("Color Sample Collection", mouse_callback)

    print("숫자 키 1~7로 라벨 선택 (1:Red, 2:Blue, 3:Green, 4:Yellow, 5:Black, 6:White, 7:Gray)")
    print("ESC 키로 종료, S 키로 샘플 저장")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("프레임을 읽을 수 없습니다.")
            break
        
        # 화면에 현재 라벨 및 샘플 개수 표시
        label_text = f"Current Label: {color_labels.get(current_label, 'None')}"
        cv2.putText(frame, label_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                    1, (0, 255, 0), 2)
        cv2.putText(frame, f"Samples Collected: {len(samples)}", (10, 70), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        
        cv2.imshow("Color Sample Collection", frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC
            break
        elif key in [ord(str(i)) for i in range(1, 8)]:
            current_label = int(chr(key))
            print(f"라벨이 {color_labels[current_label]}(으)로 설정되었습니다.")
        elif key == ord('s') or key == ord('S'):
            save_samples()
            samples.clear()  # 저장 후 리스트 비우기
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    collect_color_samples()