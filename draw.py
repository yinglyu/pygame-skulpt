#draw.py
#对角线圆形

import math, random
import pygame as pg

pg.init()

pg.display.set_caption("diagonal circles")
(width, height) = (400, 500)
prozor = pg.display.set_mode((width, height))


def random_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


def crtaj():
    r = d / (2 * n)
    kx = width / (2 * n)
    ky = height / (2 * n)
    prozor.fill(pg.Color("white"))
    for i in range(n):
        (cx, cy) = ((2 * i + 1) * kx, height - (2 * i + 1) * ky)
        pg.draw.circle(prozor, random_color(), (round(cx), round(cy)), round(r), 2)
    pg.display.update()


d = math.sqrt(width ** 2 + height ** 2)

n = 5
crtaj()

end_flag = False
while not end_flag:
    pg_event = pg.event.wait()
    if pg_event.type == pg.QUIT:
        end_flag = True
    elif pg_event.type == pg.MOUSEBUTTONDOWN:
        if pg_event.button == 1:
            n += 1
            crtaj()
        elif pg_event.button == 3 and n > 1:
            n -= 1
            crtaj()
    if pg_event.type == pg.KEYDOWN:
        if pg_event.key == pg.K_UP:
            n += 1
            crtaj()
        elif pg_event.key == pg.K_DOWN and n > 1:
            n -= 1
            crtaj()

pg.quit()
