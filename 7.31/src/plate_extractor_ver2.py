import os
import cv2
import numpy as np

# 현재 실행 중인 스크립트 경로 기준으로 img 폴더 위치 설정
script_dir = os.path.dirname(os.path.abspath(__file__))
img_folder = os.path.normpath(os.path.join(script_dir, '..', 'img'))  # ../img
save_dir = os.path.normpath(os.path.join(script_dir, '..', 'extracted_plates'))

# 저장 폴더 생성
os.makedirs(save_dir, exist_ok=True)

# 유효성 검사
if not os.path.exists(img_folder):
    print(f"이미지 폴더를 찾을 수 없습니다: {img_folder}")
    exit()

# 이미지 목록 가져오기
img_files = sorted([
    f for f in os.listdir(img_folder)
    if f.lower().endswith(('.jpg', '.png', '.jpeg'))
])

# 마우스 이벤트용 전역 변수
pts = np.zeros((4, 2), dtype=np.float32)
pts_cnt = 0
current_img = None
draw_img = None
img_index = 0
win_name = "Select Plate Corners"

def extract_and_save(img, points, index):
    sm = points.sum(axis=1)
    diff = np.diff(points, axis=1)
    topLeft = points[np.argmin(sm)]
    bottomRight = points[np.argmax(sm)]
    topRight = points[np.argmin(diff)]
    bottomLeft = points[np.argmax(diff)]

    pts1 = np.float32([topLeft, topRight, bottomRight, bottomLeft])
    width, height = 300, 150
    pts2 = np.float32([[0,0], [width-1,0], [width-1,height-1], [0,height-1]])

    mtrx = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(img, mtrx, (width, height))

    filename = f"{save_dir}/plate_{index+1:03d}.jpg"
    cv2.imwrite(filename, result)
    print(f"[저장됨] {filename}")
    cv2.imshow("Extracted", result)

def onMouse(event, x, y, flags, param):
    global pts, pts_cnt, draw_img, img_index

    if event == cv2.EVENT_LBUTTONDOWN and pts_cnt < 4:
        pts[pts_cnt] = [x, y]
        cv2.circle(draw_img, (x, y), 5, (0, 255, 0), -1)
        cv2.imshow(win_name, draw_img)
        pts_cnt += 1

        if pts_cnt == 4:
            extract_and_save(current_img, pts, img_index)
            pts_cnt = 0
            pts[:] = 0

            img_index += 1
            if img_index >= len(img_files):
                print("모든 이미지 처리 완료!")
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                exit()
            else:
                load_next_image()

def load_next_image():
    global current_img, draw_img
    img_path = os.path.join(img_folder, img_files[img_index])
    current_img = cv2.imread(img_path)
    draw_img = current_img.copy()
    print(f"\n🔍 [{img_index+1}/{len(img_files)}] 파일: {img_files[img_index]}")
    print(" → 번호판 꼭짓점 4점을 마우스로 클릭하세요.")
    cv2.imshow(win_name, draw_img)

# 초기 실행
if len(img_files) == 0:
    print("차량 이미지가 없습니다.")
    exit()

cv2.namedWindow(win_name)
cv2.setMouseCallback(win_name, onMouse)
load_next_image()

cv2.waitKey(0)
cv2.destroyAllWindows()
