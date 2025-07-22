import turtle
import math
# 시작점과 종점을 정해놓고, 종점에 거북이가 도착하게끔
# 시작점: 좌측 하단, 종점: 우측 상단

# 스크린 생성 / 이동거리 변수 초기화
s = turtle.getscreen()
s.title("거북이 이동")
s.setup(500, 500)
total_distance = 0

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
t.setheading(t.towards(end_pos)) # 종점 방향으로 머리돌림
t.speed(5)

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
obs.goto(0, 0)
obs.penup()

# 생성한 장애물을 리스트에 추가
obstacles.append(obs)

# 충돌 검사 함수
def is_collision(turtle_obj, obstacle):
    # 각 요소의 위치
    tx, ty = turtle_obj.pos()
    ox, oy = obstacle.pos()
    # 장애물의 실제 넓이 추정
    obstacle_half_width = 60
    obstacle_half_height = 60

    # 충돌 판정 (사각형 범위 내 거북이 좌표가 들어오는지)
    if (ox - obstacle_half_width < tx < ox + obstacle_half_width and
        oy - obstacle_half_height < ty < oy + obstacle_half_height):
        return True
    return False

# 메시지 출력용 터틀
msg_writer = turtle.Turtle()
msg_writer.hideturtle()
msg_writer.penup()
msg_writer.goto(-200, 220)

# 이동 및 충돌 회피 로직
def move_turtle(turtle_obj, end_pos):
    global total_distance
    prev_pos = turtle_obj.pos()
    current_message = None  # 현재 표시 중인 메시지를 추적
    
    while turtle_obj.distance(end_pos) > 10:
        if any(is_collision(turtle_obj, obs) for obs in obstacles):
            if current_message != "collision":
                msg_writer.clear()
                msg_writer.goto(-200, 220)
                msg_writer.write("충돌 감지! 경로 변경 중...", font=("Malgun Gothic", 14, "bold"))
                current_message = "collision"
                
            turtle_obj.right(90)
            turtle_obj.forward(30)
            turtle_obj.left(90)
        else:
            if current_message != "moving":
                msg_writer.clear()
                msg_writer.goto(-200, 220)
                msg_writer.write("이동 중...", font=("Malgun Gothic", 14, "bold"))
                current_message = "moving"
                
            turtle_obj.setheading(turtle_obj.towards(end_pos))
            turtle_obj.forward(5)
            
        # 거리 계산
        new_pos = turtle_obj.pos()
        step = math.dist(prev_pos, new_pos)  # 이동 거리 계산
        total_distance += step
        prev_pos = new_pos

# 위치 이동(정중앙 -> 시작점)후 거북이 보이게 함
t.showturtle()
t.pendown()
move_turtle(t, end_pos)

# 총 이동 거리 출력
msg_writer.clear()
msg_writer.goto(-200, 200)
msg_writer.write(f"총 이동 거리: {total_distance:.2f} 픽셀", font=("Malgun Gothic", 14, "bold"))

# 거북이의 상태(도착여부 체크) 출력
if t.distance(end_pos) < 10: # 도착했다고 판단
    msg_writer.goto(-200, 150)
    msg_writer.write("목표 지점에 도착하였습니다.", font=("Malgun Gothic", 14, "bold"))
else:
    msg_writer.goto(-200, 150)
    msg_writer.write("이동 중...", font=("Malgun Gothic", 14, "bold"))

# 창을 닫지 않도록 대기
turtle.done()
