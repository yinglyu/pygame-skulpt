#万花尺

import math
import pygame as pg


pg.init()

pg.display.set_caption("Spirograph")
(width, height) = (400, 400)
pg_window = pg.display.set_mode((width, height))

(cx, cy) = (width // 2, height // 2)
R = min(width//2, height//2)
k = 0.67
l = 0.67
r = round(k * R)
alpha = 0

kriva = pg.Surface((width, height))
kriva.fill(pg.Color("white"))

pg.time.set_timer(pg.USEREVENT, 1000 // 50)

end_flag = False
treba_crtati = True
while not end_flag:
    if treba_crtati:
        pg_window.fill(pg.Color("white"))
        pg_window.blit(kriva, (0, 0))
        pg.draw.circle(pg_window, pg.Color("black"), (cx, cy), R, 3)
        pg.draw.circle(pg_window, pg.Color("red"), (round(cx + R * math.cos(alpha)), round(cy - R * math.sin(alpha))), 5)
        (mx, my) = (round(cx + (R-r)*math.cos(alpha)), round(cy - (R-r)*math.sin(alpha)))
        pg.draw.circle(pg_window, pg.Color("blue"), (mx, my), r, 3)
        beta = - (R - r)/r*alpha
        (Ax, Ay) = (round(mx + l*r*math.cos(beta)), round(my - l*r*math.sin(beta)))
        pg.draw.circle(pg_window, pg.Color("red"), (Ax, Ay), 5)

        hue = round(((alpha + math.pi) % (2*math.pi)) / (2*math.pi) * 360)
        boja = pg.Color("black")
        boja.hsva = (hue, 100, 100, 1)
        pg.draw.circle(kriva, boja, (Ax, Ay), 2)
        
        pg.display.update()
        treba_crtati = False
    pg_event = pg.event.wait()
    if pg_event.type == pg.QUIT:
        end_flag = True
    elif pg_event.type == pg.USEREVENT:
        alpha += math.pi / 90
        treba_crtati = True
    elif pg_event.type == pg.MOUSEMOTION:
        (x, y) = pg_event.pos
        phi0 = (alpha + math.pi) % (2*math.pi) - math.pi
        phi = math.atan2(cy - y, x - cx)
        d_phi = phi - phi0
        if d_phi > math.pi:
            d_phi -= 2*math.pi
        if d_phi < -math.pi:
            d_phi += 2*math.pi
        alpha += d_phi
        treba_crtati = True
        
pg.quit()
