# 장애물 피하기 게임
# 기존의 장애물이 5개에 속도도 단조로워
# 장애물 개수와 속도가 점수에 비례해서 늘어나도록 개선함.
# 1회 충돌을 막아주는 아이템과 장애물 낙하 속도를 느려지게 해주는 아이템을 추가.

import turtle
import random
import time

# 화면 설정
screen = turtle.Screen()
screen.title("장애물 피하기 | <아이템> 초록: 슬로우, 파랑: 실드")
screen.bgcolor("black")
screen.setup(width=600, height=600)
screen.tracer(0)

# 플레이어 설정
player = turtle.Turtle()
player.shape("turtle")
player.color("white")
player.penup()
player.goto(0, -250)
player.setheading(90)

# 점수판
score = 0
pen = turtle.Turtle()
pen.hideturtle()
pen.penup()
pen.color("white")
pen.goto(0, 260)
pen.write(f"점수: {score}", align="center", font=("Arial", 16, "bold"))

# 장애물 설정
obstacles = []
initial_obstacles = 5
max_obstacles = 30
speed = 3

def create_obstacle():
    obs = turtle.Turtle()
    obs.shape("square")
    obs.color("red")
    obs.shapesize(stretch_wid=1, stretch_len=1)
    obs.penup()
    obs.speed(0)
    obs.goto(random.randint(-280, 280), random.randint(300, 500))
    obstacles.append(obs)

for _ in range(initial_obstacles):
    create_obstacle()

# 아이템 설정
items = []
item_types = ["shield", "slow"]
item_active = None
shield_active = False
slow_until = 0

def spawn_item():
    item = turtle.Turtle()
    item.penup()
    item.speed(0)
    item.goto(random.randint(-280, 280), random.randint(300, 500))
    item_type = random.choice(item_types)
    item.shape("circle")

    if item_type == "shield":
        item.color("blue")
    elif item_type == "slow":
        item.color("green")
    item.type = item_type
    items.append(item)

# 이동 함수
def go_left():
    x = player.xcor()
    if x > -270:
        player.setx(x - 30)

def go_right():
    x = player.xcor()
    if x < 270:
        player.setx(x + 30)

screen.listen()
screen.onkeypress(go_left, "Left")
screen.onkeypress(go_right, "Right")

# 게임 루프
game_over = False
frame = 0

while not game_over:
    screen.update()
    time.sleep(0.02)
    frame += 1

    current_speed = speed

    # 슬로우 지속 시간 체크
    if time.time() < slow_until:
        current_speed = speed / 2

    # 장애물 이동
    for obs in obstacles:
        obs.sety(obs.ycor() - current_speed)

        if obs.ycor() < -300:
            obs.goto(random.randint(-280, 280), random.randint(300, 500))
            score += 1

            # 점수판 갱신
            pen.clear()
            pen.goto(0, 260)
            pen.write(f"점수: {score} {'🛡️' if shield_active else ''}", align="center", font=("Arial", 16, "bold"))

            # 속도 증가
            if score % 5 == 0:
                speed += 0.5
            # 장애물 증가
            if score % 10 == 0 and len(obstacles) < max_obstacles:
                create_obstacle()

            # 아이템 등장 확률 (5%): 1/20
            if random.randint(1, 20) == 1:
                spawn_item()

        # 충돌 감지
        if player.distance(obs) < 20:
            if shield_active:
                shield_active = False  # 쉴드 소멸
                obs.goto(random.randint(-280, 280), random.randint(300, 500))
            else:
                game_over = True
                pen.clear()
                pen.goto(0, 0)
                pen.write(f"GAME OVER! 최종 점수: {score}", align="center", font=("Arial", 20, "bold"))

    # 아이템 이동
    for item in items[:]:
        item.sety(item.ycor() - current_speed)

        # 아이템 획득
        if player.distance(item) < 20:
            if item.type == "shield":
                shield_active = True
            elif item.type == "slow":
                slow_until = time.time() + 3  # 3초간 슬로우

            item.hideturtle()
            items.remove(item)

        # 바닥 아래로 떨어진 아이템 제거
        if item.ycor() < -300:
            item.hideturtle()
            items.remove(item)

# 종료 대기
screen.mainloop()
