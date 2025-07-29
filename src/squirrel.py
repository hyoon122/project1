# 해당 이미지의 원하는 곳을 반복 캡쳐할 수 있는 알고리즘
# 사용법: 이미지가 켜진 후, 좌상단 -> 우하단 방향으로
# 원하는 이미지의 부분을 드래그하면 해당 부분의 캡처본을 띄움.

# 주의사항: 해당 알고리즘 파일은 'jpg' 기준으로 작성되었습니다.
# 만약 이미지 확장자명이 다를 시, 하나로 통일시켜 사용해야 합니다.

import cv2
import numpy as np
import os

isDragging = False                      # 마우스 드래그 상태 저장 
x0, y0, w, h = -1,-1,-1,-1              # 영역 선택 좌표 저장
blue, red = (255,0,0),(0,0,255)         # 색상 값 

def onMouse(event,x,y,flags,param):     # 마우스 이벤트 핸들 함수
    global isDragging, x0, y0, image    # 전역변수 참조
    if event == cv2.EVENT_LBUTTONDOWN:  # 왼쪽 마우스 버튼 다운, 드래그 시작
        isDragging = True
        x0 = x
        y0 = y
    elif event == cv2.EVENT_MOUSEMOVE:  # 마우스 움직임
        if isDragging:                  # 드래그 진행 중
            img_draw = image.copy()     # 사각형 그림 표현을 위한 이미지 복제
            cv2.rectangle(img_draw, (x0, y0), (x, y), blue, 2) # 드래그 진행 영역 표시
            cv2.imshow('img', img_draw) # 사각형 표시된 그림 화면 출력
    elif event == cv2.EVENT_LBUTTONUP:  # 왼쪽 마우스 버튼 업
        if isDragging:                  # 드래그 중지
            isDragging = False          
            w = x - x0                  # 드래그 영역 폭 계산
            h = y - y0                  # 드래그 영역 높이 계산
            print("x:%d, y:%d, w:%d, h:%d" % (x0, y0, w, h))
            if w > 0 and h > 0:         # 폭과 높이가 양수이면 드래그 방향이 옳음
                img_draw = image.copy() # 선택 영역에 사각형 그림을 표시할 이미지 복제
                
                # 선택 영역에 빨간 사각형 표시
                cv2.rectangle(img_draw, (x0, y0), (x, y), red, 2) 
                cv2.imshow('img', img_draw)           # 빨간 사각형 그려진 이미지 화면 출력
                roi = image[y0:y0+h, x0:x0+w]         # 원본 이미지에서 선택 영영만 ROI로 지정
                cv2.imshow('Capture', roi)            # ROI 지정 영역을 새창으로 표시
                cv2.moveWindow('Capture', 0, 0)       # 새창을 화면 좌측 상단에 이동
                cv2.imwrite('./Captured Screen.jpg', roi)   # ROI 영역만 파일로 저장
                print("Screen Capture is Completed.") # 캡처 완료 시, 터미널에 완료문구를 띄움
                print() # 공백
            else:
                cv2.imshow('img', image) # 드래그 방향이 잘못된 경우, 사각형 그림이 없는 원본 이미지 출력
                print("좌측 상단에서 우측 하단으로 영역을 드래그 하세요.")

# 현재 스크립트 파일 기준으로 이미지 경로 생성
script_dir = os.path.dirname(os.path.abspath(__file__))  # squirrel.py의 위치
img_path = os.path.join(script_dir, '../img/Squirrel.jpg')
img_path = os.path.normpath(img_path)  # 경로 정리

print("이미지 경로:", img_path)  # 경로 출력 확인

image = cv2.imread(img_path)

if image is None:
    print("이미지를 불러오지 못했습니다.")
else:
    cv2.imshow('img', image)
    # 마우스 이벤트 등록
    cv2.setMouseCallback('img', onMouse) 
    cv2.waitKey(0)
    cv2.destroyAllWindows()
