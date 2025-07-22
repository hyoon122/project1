import turtle
# 시작점과 종점을 정해놓고, 종점에 거북이가 도착하게끔
# 시작점: 좌측 하단, 종점: 우측 상단

# 스크린 생성
s = turtle.getscreen()
s.title("거북이 이동")
s.setup(500, 500)
# 시작점과 종점 좌표 설정
start_pos = (-200, -200)
end_pos = (200, 200)

# 시작점 표시
marker_start = turtle.Turtle()
marker_start.hideturtle()
marker_start.penup()
marker_start.goto(start_pos)
marker_start.dot(10, "blue")  # 파란 점으로 시작 위치 표시

# 종점 표시
marker_end = turtle.Turtle()
marker_end.hideturtle()
marker_end.penup()
marker_end.goto(end_pos)
marker_end.dot(10, "red")  # 빨간 점으로 끝 위치 표시

# 거북이 변수 지정 / 시작점으로 이동(숨겨서)
t = turtle.Turtle()
turtle.setheading(45)
t.setheading(45)
t.speed(1)

# 거북이 숨김 상태로 시작 (중앙에서 시작하기 때문)
t.hideturtle()
t.shape("turtle")
t.color("green")
t.penup()
t.goto(start_pos)

# 장애물 설정
obstacles = []
num_obstacles = 1
obs = turtle.Turtle()
obs.shape("square")
obs.color("black")
obs.shapesize(stretch_wid=5, stretch_len=5)
obs.penup()

# 생성한 장애물을 리스트에 추가
obstacles.append(obs)

# 위치 이동(정중앙 -> 시작점)후 거북이 보이게 함
t.showturtle()
t.pendown()

# 거북이를 종점으로 이동
t.goto(end_pos)

# 창을 닫지 않도록 대기
turtle.done()
