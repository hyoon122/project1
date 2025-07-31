# 자동차 번호판 추출 실습 가이드
import os
import cv2
import numpy as np

win_name = "License Plate Scanner"
save_dir = "extracted_plates"
os.makedirs(save_dir, exist_ok=True)

# 이미지 불러오기
script_dir = os.path.dirname(os.path.abspath(__file__))
img_path = os.path.join(script_dir, '..', 'img', 'car_01.png')
img_path = os.path.normpath(img_path)

# 경로 확인용
print(f"이미지 경로 확인: {img_path}")
print(f"존재 여부: {os.path.exists(img_path)}")

img = cv2.imread(img_path)
if img is None:
    print(f"이미지를 읽을 수 없습니다: {img_path}")
    exit()

draw = img.copy()
pts = np.zeros((4, 2), dtype=np.float32)
pts_cnt = 0

# 번호판 영역 기준, 좌상단-> 우상단-> 우하단-> 좌하단 모서리 클릭

def onMouse(event, x, y, flags, param):
    global pts_cnt, pts

    if event == cv2.EVENT_LBUTTONDOWN and pts_cnt < 4:
        cv2.circle(draw, (x, y), 5, (0, 255, 0), -1)
        cv2.imshow(win_name, draw)

        pts[pts_cnt] = [x, y]
        pts_cnt += 1

        if pts_cnt == 4:
            # 1. 좌표 정렬
            sm = pts.sum(axis=1)                # x + y 값 계산
            diff = np.diff(pts, axis=1)         # x - y 값 계산
            topLeft = pts[np.argmin(sm)]        # x+y가 최소 → 좌상단
            bottomRight = pts[np.argmax(sm)]    # x+y가 최대 → 우하단
            topRight = pts[np.argmin(diff)]     # x-y가 최소 → 우상단
            bottomLeft = pts[np.argmax(diff)]   # x-y가 최대 → 좌하단

            # 좌상단 -> 우상단 -> 우하단 -> 좌하단
            pts1 = np.float32([topLeft, topRight, bottomRight, bottomLeft])
            
            # 2. 표준 번호판 크기 지정
            width, height = 300, 150
            pts2 = np.float32([[0,0], [width-1,0], [width-1,height-1], [0,height-1]])

            # 3. 원근 변환
            mtrx = cv2.getPerspectiveTransform(pts1, pts2)
            result = cv2.warpPerspective(img, mtrx, (int(width), int(height)))
            # width, height를 int형으로 전환

            # 4. 파일 이름 생성 (순번 방식 채택)
            existing_files = len(os.listdir("extracted_plates"))
            filename = f"extracted_plates/plate_{existing_files+1:03d}.png"
            # 파일 저장
            success = cv2.imwrite(filename, result)
            
            if success:
                print(f"번호판 저장 완료: {filename}")
                cv2.imshow('Extracted Plate', result)
            else:
                print("저장 실패!")

# 저장 폴더가 없으면 생성
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

cv2.imshow(win_name, img)
cv2.setMouseCallback(win_name, onMouse)
cv2.waitKey(0)
cv2.destroyAllWindows()