import serial
import time
import turtle
import threading

# 전역 변수
connection = None
current_distance = 0
t = turtle.Turtle()

# 스크린 생성
s = turtle.getscreen()
s.title("초음파 센서를 활용한 거북이 이동")
s.setup(500, 500)

# 메시지 출력용 터틀
msg_writer = turtle.Turtle()
msg_writer.hideturtle()
msg_writer.penup()
msg_writer.goto(-200, 220)

# 거북이 초기 설정
t.shape("turtle")
t.color("green")

# 초음파 센서 연결 함수
def connect_sensor(port='COM3'):
    global connection
    try:
        connection = serial.Serial(port, 9600)
        time.sleep(2)
        print("연결 성공")
        return True
    except:
        print("연결 실패")
        return False

# 초음파 거리 읽기
def read_distance():
    global connection, current_distance
    if connection and connection.in_waiting > 0:
        data = connection.readline().decode().strip()
        print(f"수신된 데이터: {data}")  # 디버그 출력
        # 'Distance: ' 부분 제거
        data = data.replace("Distance:", "").strip()
        if not data:
            return None
        try:
            distance = float(data)
            current_distance = distance
            return distance
        except ValueError:
            return None
    return None

# 거북이 움직이기 함수
def move_turtle():
    if current_distance:
        if current_distance > 20:  # 거리가 20cm 이상이면 전진
            msg_writer.goto(-200, 200)
            msg_writer.write("이동 중...", font=("Malgun Gothic", 14, "bold"))
            t.forward(25)
            t.left(15)
            msg_writer.clear()
        elif current_distance < 10:  # 거리가 10cm 이하이면 멈춤 (뒤로 가기)
            msg_writer.goto(-200, 200)
            msg_writer.write("장애물 감지! 뒤로 이동합니다.", font=("Malgun Gothic", 14, "bold"))
            t.right(15)
            t.backward(25)
            msg_writer.clear()
        print(f"감지 거리: {current_distance}cm")

# 메인 로직
def main():
    if connect_sensor():
        # turtle 화면 설정
        screen = turtle.Screen()
        screen.setup(width=600, height=600)
        
        while True:
            dist = read_distance()
            if dist:
                move_turtle()
            time.sleep(1)

# 프로그램 실행
if __name__ == "__main__":
    main()
