# Tip) threshold()의 밝기 기준 (50) 을 조정하면 더 밝거나 어두운 물체를 추적 가능
# area < 100 으로 노이즈 제거, 필요 시 더 큰 값으로

import cv2
import numpy as np


# 카메라 열기
cap = cv2.VideoCapture(0)

# 해상도 설정
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap.isOpened():
    print("카메라를 열 수 없습니다.")
    exit()

print("카메라가 열렸습니다. 'q' 키를 누르면 종료됩니다.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("프레임을 읽을 수 없습니다.")
        break

    # 1.그레이스케일 변환
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 2.어두운 픽셀만 추출 (검은색 탐지)
    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)

    # 3.윤곽선 찾기
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    output = frame.copy()

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 100:  # 작은 노이즈 무시
            continue

        # 윤곽선 그리기
        cv2.drawContours(output, [cnt], -1, (0, 255, 0), 2)

        # 중심점 계산
        M = cv2.moments(cnt)
        if M['m00'] != 0:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            cv2.circle(output, (cx, cy), 5, (0, 0, 255), -1)
            cv2.putText(output, f'({cx},{cy})', (cx + 10, cy),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    # 결과 영상 출력
    cv2.imshow('Real-time Contour Tracking', output)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("종료 키 'q' 입력됨.")
        break

# 자원 해제
cap.release()
cv2.destroyAllWindows()