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
    cv2.imshow('Image Window', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
