import os
import cv2
import time
import matplotlib.pylab as plt

# 웹캠 열기 (기본 카메라: 0번)
cap = cv2.VideoCapture(0)

# 해상도 설정 (640x480)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# 카메라 열렸는지 확인
if not cap.isOpened():
    print("카메라를 열 수 없습니다.")
    exit()

print("카메라가 열렸습니다. 'q' 키를 누르면 종료 / 's' 키로 촬영.")
photo_count = 0  # 사진 저장용 번호

while True:
    ret, frame = cap.read()
    if not ret:
        print("프레임을 읽을 수 없습니다.")
        break

    cv2.imshow('Webcam 640x480', frame)
    
    key = cv2.waitKey(1) & 0xFF

    # 'q' 키를 누르면 종료, 's' 키를 누르면 촬영
    if key == ord('q'):
        print("종료 키 'q' 입력됨.")
        break
    elif key == ord('s'):
        # 폴더가 없으면 자동 생성
        os.makedirs("photos", exist_ok=True)
        filename = f"photos/capture_{photo_count}.png"
        cv2.imwrite(filename, frame)
        
        print(f"{filename} 저장 완료.")
        photo_count += 1

# 자원 해제
cap.release()
cv2.destroyAllWindows()

# 이미지 불러오기
script_dir = os.path.dirname(os.path.abspath(__file__))
img_path = os.path.join(script_dir, '..', '..', 'photos', 'capture_0.png')
img_path = os.path.normpath(img_path)

img = cv2.imread(img_path)
if img is None:
    print(f"이미지를 읽을 수 없습니다: {img_path}")
    exit()

# 관심영역 선택 기능
roi = cv2.selectROI("Select ROI(Press Enter Key after Drag.)", img, showCrosshair=True)
cv2.destroyAllWindows()

x, y, w, h = roi
if w == 0 or h == 0:
    print("관심영역이 선택되지 않았습니다.")
    exit()

roi_img = img[y:y+h, x:x+w]

# 선택한 영역 보여주기
cv2.imshow("Selected ROI", roi_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 현재 스크립트 위치 기준 경로 구하기
script_dir = os.path.dirname(os.path.abspath(__file__))
img_path = os.path.join(script_dir, '..', '..', 'photos', 'capture_0.png')
img_path = os.path.normpath(img_path)

# 이미지 로드
img = cv2.imread(img_path)
if img is None:
    print(f"이미지를 읽을 수 없습니다: {img_path}")
    exit()

# 히스토그램 계산 및 그리기
channels = cv2.split(img)
colors = ('b', 'g', 'r')
for (ch, color) in zip (channels, colors):
    hist = cv2.calcHist([ch], [0], None, [256], [0, 256])
    plt.plot(hist, color = color)

plt.title("ROI RGB 히스토그램")
plt.xlabel("Pixel Value")
plt.ylabel("Frequency")
plt.grid(True)
plt.show()