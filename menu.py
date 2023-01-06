import pygame as pg


def main():
    width, height = 480, 480
    screen = pg.display.set_mode((width, height))
    font = pg.font.Font(None, 32)
    clock = pg.time.Clock()
    ip_box = pg.Rect(width//2-100, 100, 100, 30)
    port_box = pg.Rect(width//2-100, 200, 200, 30)
    name_box = pg.Rect(width//2-100, 300, 200, 30)
    button_box = pg.Rect(width//2-100, 400, 200, 50)
    color_inactive = pg.Color('lightskyblue3')
    color_active = pg.Color('dodgerblue2')
    color = color_inactive
    color1 = color_active
    color2 = color_inactive
    color3 = color_inactive
    pg.display.set_caption("CONNECT")
    active = False
    active1 = False
    active2 = False
    text = ''
    text1 = ''
    text2 = ''
    done = False
    txt_button = 'CONNECT'
    ip_render = pg.font.SysFont('Arial', 50, bold=True).render("IP: ", False, (255, 255, 255))
    port_render = pg.font.SysFont('Arial', 50, bold=True).render("PORT: ", False, (255, 255, 255))
    name_render = pg.font.SysFont('Arial', 50, bold=True).render("NAME: ", False, (255, 255, 255))

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.MOUSEBUTTONDOWN:
                if ip_box.collidepoint(event.pos):
                    active = not active
                    active1 = False
                    active2 = False
                elif port_box.collidepoint(event.pos):
                    active1 = not active1
                    active = False
                    active2 = False
                elif name_box.collidepoint(event.pos):
                    active2 = not active2
                    active = False
                    active1 = False
                elif button_box.collidepoint(event.pos):
                    return text, text1, text2
                else:
                    active = False
                color = color_active if active else color_inactive
                color2 = color_active if active1 else color_inactive
                color3 = color_active if active2 else color_inactive
            if event.type == pg.KEYDOWN:
                if active:
                    if event.key == pg.K_RETURN:
                        return text, text1, text2
                    elif event.key == pg.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
                elif active1:
                    if event.key == pg.K_RETURN:
                        return text, text1, text2
                    elif event.key == pg.K_BACKSPACE:
                        text1 = text1[:-1]
                    else:
                        text1 += event.unicode
                elif active2:
                    if event.key == pg.K_RETURN:
                        return text, text1, text2
                    elif event.key == pg.K_BACKSPACE:
                        text2 = text2[:-1]
                    else:
                        text2 += event.unicode

        screen.fill((70, 70, 70))
        txt_surface = font.render(text, True, color)
        txt_surface1 = font.render(text1, True, color2)
        txt_surface2 = font.render(text2, True, color3)
        width = max(200, txt_surface.get_width()+10)
        ip_box.w = width
        port_box.w = width
        name_box.w = width
        screen.blit(ip_render, (width//2+40, 50))
        screen.blit(port_render, (width//2+40, 150))
        screen.blit(name_render, (width//2+40, 250))
        screen.blit(txt_surface, (ip_box.x+5, ip_box.y+5))
        screen.blit(txt_surface1, (port_box.x+5, port_box.y+5))
        screen.blit(txt_surface2, (name_box.x+5, name_box.y+5))
        pg.draw.rect(screen, color, ip_box, 2)
        pg.draw.rect(screen, color2, port_box, 2)
        pg.draw.rect(screen, color3, name_box, 2)
        pg.draw.rect(screen, color1, button_box)
        button_surface = font.render(txt_button, True, color_inactive)
        screen.blit(button_surface, (width // 2 + 80, 410))
        pg.display.flip()
        clock.tick(30)
