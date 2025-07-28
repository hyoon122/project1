import cv2
import os

# 현재 스크립트 파일 기준으로 이미지 경로 생성
script_dir = os.path.dirname(os.path.abspath(__file__))  # test.py의 위치
img_path = os.path.join(script_dir, '../img/like_lenna224.png')
img_path = os.path.normpath(img_path)  # 경로 정리

print("이미지 경로:", img_path)  # 경로 출력 확인

image = cv2.imread(img_path)

if image is None:
    print("이미지를 불러오지 못했습니다.")
else:
    # 원하는 부분만 자르기 (예: y=50~150, x=100~200)
    #cropped_image = image[50:150, 100:200]  # [y1:y2, x1:x2]
    #cropped_image = image[50:150,50:150]
    #cropped_image[:] = 200
    
    # 사각형 그리기: (x1, y1) ~ (x2, y2) / 사각형 2개와 선 1개를 활용하여 안경 만들기
    start_point = (120, 70)   # 왼쪽 위(좌상단) 좌표
    end_point = (150, 90)     # 오른쪽 아래(우하단) 좌표
    color = (0, 255, 0)       # BGR 색상: 초록색
    thickness = 2             # 선 두께

    start_point2 = (160, 70)   # 왼쪽 위(좌상단) 좌표
    end_point2 = (190, 90)     # 오른쪽 아래(우하단) 좌표
    color2 = (0, 255, 0)       # BGR 색상: 초록색
    thickness2 = 2             # 선 두께

    cv2.line(image, (150,80), (160, 80), (0,255,0), 5)  # 초록색 5픽셀 선
    cv2.rectangle(image, start_point, end_point, color, thickness)
    cv2.rectangle(image, start_point2, end_point2, color2, thickness2)

    # 이미지 크기 2배로 확대
    scale = 2  # 원하는 배율
    resized_image = cv2.resize(image, (0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)
    cv2.imshow('Image Window', resized_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
