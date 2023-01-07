import socket, pickle
from random import randrange
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
HOST = s.getsockname()[0]
PORT = int(input("PORT: "))
print(f"Server running in {HOST}:{PORT}")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
name1 = conn.recv(4096)
print('Connected by', addr)
conn.send("1".encode("utf-8"))
conn1, addr1 = s.accept()
name2 = conn1.recv(4096)
print('Connected by', addr1)
conn1.send("2".encode("utf-8"))
width, height = 820, 640
width_w = 20
height_h = 200
score1, score2 = 0, 0
rect1_x = 0
rect1_y = height_h
rect2_x = width - width_w
rect2_y = height_h
speed = 5
speed_ball = 2.5
radius = 10
color_ball = randrange(0, 256), randrange(0, 256), randrange(0, 256)
color_player_one = randrange(0, 256), randrange(0, 256), randrange(0, 256)
color_player_two = randrange(0, 256), randrange(0, 256), randrange(0, 256)
ball_rect = int(radius * 2 ** 0.5)
ball = randrange(ball_rect, width - ball_rect), height // 2, ball_rect, ball_rect
dx, dy = 1, -1
ball_x = width // 2
ball_y = height // 2
fps = 120
caption = "PONG"

while True:
    arr = ([width, height, score1, score2, rect1_x, rect2_x, rect1_y, rect2_y, color_ball, color_player_one, color_player_two, ball_rect, ball, dx, dy, ball_x, ball_y, width_w, height_h, name1, name2, fps, caption, speed_ball])
    data_string = pickle.dumps(arr)
    conn.send(data_string)
    conn1.send(data_string)
    data = conn.recv(2048*2048)
    data1 = conn1.recv(2048*2048)
    if data.decode("utf-8") == "W" or data1.decode("utf-8") == "W":
        rect1_y -= speed
    if data.decode("utf-8") == "S" or data1.decode("utf-8") == "S":
        rect1_y += speed
    if data.decode("utf-8") == "U" or data1.decode("utf-8") == "U":
        rect2_y -= speed
    if data.decode("utf-8") == "D" or data1.decode("utf-8") == "D":
        rect2_y += speed
    if data.decode("utf-8") == "score1+" or data1.decode("utf-8") == "score1+":
        dx, dy = randrange(-1, 2, 1), randrange(-1, 2, 2)
        score1 += 1
    if data.decode("utf-8") == "score2+" or data1.decode("utf-8") == "score2+":
        dx, dy = randrange(-1, 2, 1), randrange(-1, 2, 2)
        score2 += 1

    if dx == 0 or dy == 0:
        dx, dy = randrange(-1, 2, 1), randrange(-1, 2, 2)

    if data.decode("utf-8") == "dx1" or data1.decode("utf-8") == "dx1":
        dx = 1
    if data.decode("utf-8") == "dx-1" or data1.decode("utf-8") == "dx-1":
        dx = -1
    if data.decode("utf-8") == "dy1" or data1.decode("utf-8") == "dy1":
        dy = 1
    if data.decode("utf-8") == "dy-1" or data1.decode("utf-8") == "dy-1":
        dy = -1
