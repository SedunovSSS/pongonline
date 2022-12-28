import pygame
from random import randrange

pygame.init()

width, height = 820, 640
radius = 10
width_w = 20
height_h = 200
fps = 120
dx, dy = 1, -1
speed = 5
speed_ball = 2.5
score1, score2 = 0, 0
rect1 = pygame.Rect(width // 2, height // 2 - 100, width_w, height_h)
rect2 = pygame.Rect(width // 2, height // 2 - 100, width_w, height_h)
color_ball = randrange(0, 256), randrange(0, 256), randrange(0, 256)
color_player_one = randrange(0, 256), randrange(0, 256), randrange(0, 256)
color_player_two = randrange(0, 256), randrange(0, 256), randrange(0, 256)
ball_rect = int(radius * 2 ** 0.5)
ball = pygame.Rect(randrange(ball_rect, width - ball_rect), height // 2, ball_rect, ball_rect)
print(ball)
sc = pygame.display.set_mode([width, height])
clock = pygame.time.Clock()
rect1.x = 0
rect1.y = height_h
rect2.x = width - width_w
rect2.y = height_h
ball.x = width // 2
ball.y = height // 2
font = pygame.font.SysFont('Arial', 30, bold=True)
font1 = pygame.font.SysFont('Arial', 15, bold=True)
pygame.display.set_caption("PONG")
running = True

while running:
    fps_int = int(clock.get_fps())
    render1 = font.render(str(score1), False, pygame.Color("white"))
    render2 = font.render(str(score2), False, pygame.Color("white"))
    render_fps = font1.render(f"FPS: {str(fps_int)}", False, pygame.Color("white"))
    sc.fill('black')
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            running = False
    ball.x += speed_ball * dx
    ball.y += speed_ball * dy
    if ball.y <= 0:
        dy = 1
    if ball.y >= height:
        dy = -1
    if ball.colliderect(rect1):
        dx = 1
    if ball.colliderect(rect2):
        dx = -1

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and rect1.y >= 0:
        rect1.y -= speed 
    if keys[pygame.K_s] and rect1.y <= height - height_h:
        rect1.y += speed 

    if keys[pygame.K_UP] and rect2.y >= 0:
        rect2.y -= speed 
    if keys[pygame.K_DOWN] and rect2.y <= height - height_h:
        rect2.y += speed

    if ball.x <= 0:
        score2 += 1
        ball.x = width // 2
        ball.y = height // 2
        dx, dy = randrange(-1, 2, 1), randrange(-1, 2, 2)

    if ball.x >= width:
        score1 += 1
        ball.x = width // 2
        ball.y = height // 2
        dx, dy = randrange(-1, 2, 1), randrange(-1, 2, 2)

    if dx == 0 or dy == 0:
        dx, dy = randrange(-1, 2, 1), randrange(-1, 2, 2)

    player_one = pygame.draw.rect(sc, color_player_one, rect1)
    player_two = pygame.draw.rect(sc, color_player_two, rect2)
    sc.blit(render_fps, (0, height - width_w))
    sc.blit(render1, (0, 0))
    sc.blit(render2, (width - width_w * 3, 0))
    pygame.draw.circle(sc, color_ball, ball.center, radius)
    pygame.display.flip()
    clock.tick(fps)

