# 자동차 번호판 추출 실습 가이드
import os
import cv2
import numpy as np


# 번호판 영역 기준, 좌상단-> 우상단-> 우하단-> 좌하단 모서리 클릭
sm = pts.sum(axis=1)           # x + y 값 계산
diff = np.diff(pts, axis=1)    # x - y 값 계산
topLeft = pts[np.argmin(sm)]        # x+y가 최소 → 좌상단
bottomRight = pts[np.argmax(sm)]    # x+y가 최대 → 우하단
topRight = pts[np.argmin(diff)]     # x-y가 최소 → 우상단
bottomLeft = pts[np.argmax(diff)]   # x-y가 최대 → 좌하단

# 표준 번호판 크기로 고정

width = 300
height = 150
pts2 = np.float32([[0,0], [width-1,0], [width-1,height-1], [0,height-1]])


# # 방식 1: 타임스탬프 기반
# import datetime
# timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
# filename = f"extracted_plates/plate_{timestamp}.jpg"

# 방식 2: 순번 기반 (해당 방식을 채택, import os 필요)

existing_files = len(os.listdir("extracted_plates"))
filename = f"extracted_plates/plate_{existing_files+1:03d}.jpg"

# < 저장 코드 구현 단계 >
# 원근변환 완료 후 자동 저장

# float형으로 입력되어 있을 경우, int형으로 변환해서 출력
result = cv2.warpPerspective(img, mtrx, (int(width), int(height)))

# 파일 저장
success = cv2.imwrite(filename, result)

if success:
    print(f"번호판 저장 완료: {filename}")
    cv2.imshow('Extracted Plate', result)
else:
    print("저장 실패!")

# 저장 폴더가 없으면 생성
save_dir = "extracted_plates"

if not os.path.exists(save_dir):
    os.makedirs(save_dir)
