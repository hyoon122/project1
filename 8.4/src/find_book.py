# 초기 설정 및 매칭기 생성
import cv2 , glob, numpy as np
import os

# 현재 스크립트 파일 기준으로 img/books 폴더 경로 생성
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # find_book.py가 있는 폴더 (src)
IMG_DIR = os.path.join(BASE_DIR, '..', 'img', 'books')
cover_paths = glob.glob(os.path.join(IMG_DIR, '*.*'))

# 검색 설정 변수

ratio = 0.7          # 좋은 매칭 선별 비율 (낮을수록 엄격)
MIN_MATCH = 10       # 최소 매칭점 개수 (적을수록 관대)

# ORB 특징 검출기 생성

detector = cv2.ORB_create()

# Flann 매칭기 객체 생성
FLANN_INDEX_LSH = 6  # LSH(Locality Sensitive Hashing) 알고리즘
index_params= dict(algorithm = FLANN_INDEX_LSH,
                   table_number = 6,        # 해시 테이블 개수
                   key_size = 12,          # 해시 키 크기
                   multi_probe_level = 1)   # 검색 레벨

search_params=dict(checks=32)  # 검색 시 확인할 리프 노드 수
matcher = cv2.FlannBasedMatcher(index_params, search_params)

# 책 표지 검색 함수 구현
def serch(img):

    # 쿼리 이미지(카메라로 촬영한 책) 전처리
    gray1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kp1, desc1 = detector.detectAndCompute(gray1, None)
    results = {}

    if len(cover_paths) == 0:
        print("책 커버 이미지가 없습니다. '../img/books/' 경로를 확인하세요.")
        return []
    
    for cover_path in cover_paths:
        cover = cv2.imread(cover_path)
        cv2.imshow('Searching...', cover) # 검색 중인 책 표지 표시
        cv2.waitKey(5)  # 짧은 대기로 화면 업데이트

        # 데이터베이스 이미지 전처리 및 특징점 검출
        gray2 = cv2.cvtColor(cover, cv2.COLOR_BGR2GRAY)
        kp2, desc2 = detector.detectAndCompute(gray2, None)

        # KNN 매칭 (k=2: 가장 가까운 2개 매칭점 반환)
        matches = matcher.knnMatch(desc1, desc2, 2)

        # Lowe's 비율 테스트로 좋은 매칭 선별
        good_matches = [m[0] for m in matches \
                    if len(m) == 2 and m[0].distance < m[1].distance * ratio]
                    
        if len(good_matches) > MIN_MATCH: 
            # 매칭점들의 좌표 추출
            src_pts = np.float32([ kp1[m.queryIdx].pt for m in good_matches ])
            dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good_matches ])
            
            # RANSAC으로 호모그래피 행렬 계산
            mtrx, mask = cv2.findHomography(src_pts, dst_pts, 
                                          cv2.RANSAC, 5.0)
            
            # 정상치(inlier) 비율로 매칭 정확도 계산
            accuracy = float(mask.sum()) / mask.size
            results[cover_path] = accuracy
    cv2.destroyAllWindows()

    # 정확도 기준으로 결과 정렬
    if len(results) > 0:
        results = sorted([(v,k) for (k,v) in results.items() \
                    if v > 0], reverse=True)
    return results

# 실시간 카메라 입력 및 사용자 인터페이스
cap = cv2.VideoCapture(0)
qImg = None

while cap.isOpened():

    ret, frame = cap.read()
    if not ret:
        print('No Frame!')
        break
 
    h, w = frame.shape[:2]

    # 책 인식 영역을 화면 중앙에 표시

    left = w // 3
    right = (w // 3) * 2
    top = (h // 2) - (h // 3)
    bottom = (h // 2) + (h // 3)

    cv2.rectangle(frame, (left,top), (right,bottom), (255,255,255), 3)


    # 거울 효과로 사용자 편의성 향상

    flip = cv2.flip(frame, 1)
    cv2.imshow('Book Searcher', flip)
    key = cv2.waitKey(10)

    if key == ord(' '):  # 스페이스바로 캡처
        qImg = frame[top:bottom, left:right]  # ROI 영역만 추출
        cv2.imshow('query', qImg)
        break
    elif key == 27:  # ESC키로 종료
        break
else:
    print('No Camera!!')
cap.release()

# 검색 실행 및 결과 표시
if qImg is not None:
    results = serch(qImg)  

    if len(results) == 0:
        print("No matched book cover found.")
    else:
        for(i, (accuracy, cover_path)) in enumerate(results):
            print(f"{i}: {cover_path} - 정확도: {accuracy:.2%}")
            if i == 0:  # 가장 높은 정확도의 결과 표시
                cover = cv2.imread(cover_path)
                cv2.putText(cover, f"Accuracy: {accuracy*100:.2f}%", 
                           (10,100), cv2.FONT_HERSHEY_SIMPLEX, 1, 
                           (0,255,0), 2, cv2.LINE_AA)
                cv2.imshow('Result', cover)

cv2.waitKey()
cv2.destroyAllWindows()
