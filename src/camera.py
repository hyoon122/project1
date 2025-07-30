import os
import cv2
import time

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