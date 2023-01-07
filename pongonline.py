import socket
import pickle
import pygame
from menu import main

ClientSocket = socket.socket()
pygame.init()
host, port, name = main()
num_client = None
port = int(port)
pygame.quit()

try:
    ClientSocket.connect((host, port))
    print("Connected")
except socket.error as e:
    print(str(e))

ClientSocket.send(name.encode("utf-8"))
dat = ClientSocket.recv(4096)
if dat.decode("utf-8") == "1":
    num_client = 1
elif dat.decode("utf-8") == "2":
    num_client = 2

data = ClientSocket.recv(4096)
data_arr = pickle.loads(data)
pygame.init()
width, height = data_arr[0], data_arr[1]
radius = 10
width_w, height_h = data_arr[17], data_arr[18]

name1, name2 = data_arr[19], data_arr[20]
name1, name2 = name1.decode("utf-8"), name2.decode("utf-8")

fps = data_arr[21]
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
pygame.display.set_caption(data_arr[22])
img = pygame.image.load("img/space.jpg")
sound = pygame.mixer.Sound("sounds/blast.mp3")
running = True

while running:
    dx, dy = data_arr[13], data_arr[14]
    score1, score2 = data_arr[2], data_arr[3]
    fps_int = int(clock.get_fps())
    render1 = font.render(f"{name1.upper()}: {str(score1)}", False, pygame.Color("white"))
    render2 = font.render(f"{name2.upper()}: {str(score2)}", False, pygame.Color("white"))
    render_fps = font1.render(f"FPS: {str(fps_int)}", False, pygame.Color("white"))
    sc.fill('black')
    sc.blit(img, (0, 0))
    player_one = pygame.draw.rect(sc, color_player_one, rect1)
    player_two = pygame.draw.rect(sc, color_player_two, rect2)
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    ball.x += speed_ball * dx
    ball.y += speed_ball * dy
    if ball.y <= 0 and not ball.colliderect(rect1):
        ClientSocket.send("dy1".encode("utf-8"))
    elif ball.y >= height and not ball.colliderect(rect2):
        ClientSocket.send("dy-1".encode("utf-8"))
    elif ball.colliderect(rect1) and (ball.bottom > rect1.y or ball.y < rect1.bottom):
        ClientSocket.send("dx1".encode("utf-8"))
        sound.play()
    elif ball.colliderect(rect2) and (ball.bottom > rect2.y or ball.y < rect2.bottom):
        ClientSocket.send("dx-1".encode("utf-8"))
        sound.play()

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
    sc.blit(render2, (width - width_w * len(str(score2))-len(name2)*15-50, 0))
    pygame.draw.circle(sc, color_ball, ball.center, radius)
    pygame.display.flip()
    clock.tick(fps)
