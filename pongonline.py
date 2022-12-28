import socket
import pickle
import pygame

ClientSocket = socket.socket()
host = input("IP: ")
port = int(input("PORT: "))
num_client = None

try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

dat = ClientSocket.recv(4096)
if dat.decode("utf-8") == "1":
    num_client = 1
elif dat.decode("utf-8") == "2":
    num_client = 2
pygame.init()
data = ClientSocket.recv(4096)
data_arr = pickle.loads(data)
width, height = data_arr[0], data_arr[1]
radius = 10
width_w, height_h = data_arr[17], data_arr[18]

fps = 120
speed = 5
speed_ball = 2.5

rect1 = pygame.Rect(width // 2, height // 2 - 100, width_w, height_h)
rect2 = pygame.Rect(width // 2, height // 2 - 100, width_w, height_h)
color_ball = data_arr[8]
color_player_one = data_arr[9]
color_player_two = data_arr[10]
ball_rect = data_arr[11]
ball = pygame.Rect(data_arr[12])
sc = pygame.display.set_mode([width, height])
clock = pygame.time.Clock()
rect1.x = data_arr[4]
rect2.x = data_arr[5]
rect1.y = data_arr[6]
rect2.y = data_arr[7]
ball.x = data_arr[15]
ball.y = data_arr[16]
font = pygame.font.SysFont('Arial', 30, bold=True)
font1 = pygame.font.SysFont('Arial', 15, bold=True)
pygame.display.set_caption("PONG")
running = True

while running:
    dx, dy = data_arr[13], data_arr[14]
    score1, score2 = data_arr[2], data_arr[3]
    fps_int = int(clock.get_fps())
    render1 = font.render(str(score1), False, pygame.Color("white"))
    render2 = font.render(str(score2), False, pygame.Color("white"))
    render_fps = font1.render(f"FPS: {str(fps_int)}", False, pygame.Color("white"))
    sc.fill('black')
    player_one = pygame.draw.rect(sc, color_player_one, rect1)
    player_two = pygame.draw.rect(sc, color_player_two, rect2)
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    ball.x += speed_ball * dx
    ball.y += speed_ball * dy
    if ball.y <= 0:
        ClientSocket.send("dy1".encode("utf-8"))
    elif ball.y >= height:
        ClientSocket.send("dy-1".encode("utf-8"))
    elif ball.colliderect(rect1):
        ClientSocket.send("dx1".encode("utf-8"))
    elif ball.colliderect(rect2):
        ClientSocket.send("dx-1".encode("utf-8"))

    elif keys[pygame.K_w] and rect1.y >= 0 and num_client == 1:
        ClientSocket.send("W".encode("utf-8"))
    elif keys[pygame.K_s] and rect1.y <= height - height_h and num_client == 1:
        ClientSocket.send("S".encode("utf-8"))
    elif keys[pygame.K_UP] and rect2.y >= 0 and num_client == 2:
        ClientSocket.send("U".encode("utf-8"))
    elif keys[pygame.K_DOWN] and rect2.y <= height - height_h and num_client == 2:
        ClientSocket.send("D".encode("utf-8"))
    elif ball.x <= 0:
        ball.x = width // 2
        ball.y = height // 2
        ClientSocket.send("score2+".encode("utf-8"))
    elif ball.x >= width:
        ball.x = width // 2
        ball.y = height // 2
        ClientSocket.send("score1+".encode("utf-8"))
    else:
        ClientSocket.send("None".encode("utf-8"))
    data = ClientSocket.recv(4096)
    data_arr = pickle.loads(data)
    width, height = data_arr[0], data_arr[1]
    score1, score2 = data_arr[2], data_arr[3]
    rect1.x = data_arr[4]
    rect2.x = data_arr[5]
    rect1.y = data_arr[6]
    rect2.y = data_arr[7]

    sc.blit(render_fps, (0, height - width_w))
    sc.blit(render1, (0, 0))
    sc.blit(render2, (width - width_w * 3, 0))
    pygame.draw.circle(sc, color_ball, ball.center, radius)
    pygame.display.flip()
    clock.tick(fps)
