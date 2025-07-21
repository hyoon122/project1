# 장애물 피하기 게임

import turtle
import random
import time

# 화면 설정
screen = turtle.Screen()
screen.title("장애물 피하기 게임")
screen.bgcolor("black")
screen.setup(width=600, height=600)
screen.tracer(0)  # 애니메이션 꺼서 직접 update

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
num_obstacles = 5

for _ in range(num_obstacles):
    obs = turtle.Turtle()
    obs.shape("square")
    obs.color("red")
    obs.shapesize(stretch_wid=1, stretch_len=2)
    obs.penup()
    obs.speed(0)
    obs.goto(random.randint(-280, 280), random.randint(100, 400))
    obstacles.append(obs)

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
speed = 2

while not game_over:
    screen.update()
    time.sleep(0.02)

    for obs in obstacles:
        obs.sety(obs.ycor() - speed)

        # 바닥에 닿으면 위로 리셋
        if obs.ycor() < -300:
            obs.goto(random.randint(-280, 280), random.randint(300, 400))
            score += 1
            pen.clear()
            pen.write(f"점수: {score}", align="center", font=("Arial", 16, "bold"))

        # 충돌 감지
        if player.distance(obs) < 20:
            game_over = True
            pen.clear()
            pen.goto(0, 0)
            pen.write("GAMEOVER!", align="center", font=("Arial", 24, "bold"))

# 마무리
screen.mainloop()
