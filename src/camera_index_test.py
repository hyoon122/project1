import cv2

print("사용 가능한 카메라 인덱스 탐색 중...")

for i in range(15):
    cap = cv2.VideoCapture(i, cv2.CAP_ANY)
    if cap.isOpened():
        print(f"카메라 인덱스 {i} 사용 가능 ✅")
        cap.release()
    else:
        print(f"카메라 인덱스 {i} 사용 불가 ❌")