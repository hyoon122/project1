# 자동차 번호판 추출 실습 가이드


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
