# 宇宙飞船

# - * - acsection general-init - * -
import pygame as pg, random

# include the work of the PyGame library
pg.init()

# Setting keyboard events - The first event is generated after
# 50ms, and every next after 25ms
pg.key.set_repeat(50, 25)

# Setting the window title
pg.display.set_caption("setanje broda")

# we open a window of a size of 400x400 pixels
(sirina, visina) = (400, 400)
prozor = pg.display.set_mode((sirina, visina))

# - * - acsection main - * -
# we load the image of a spaceship
brod = pg.image.load('../../../../assets/pygame/spaceship.png')
# we read the dimensions of the image
brod_sirina = brod.get_width()
brod_visina = brod.get_height()

# coordinates of the center of the window
(x, y) = (sirina / 2, visina / 2)
# shifts by x and y coordinates
(dx, dy) = (10, 10)

pomeraj = {pg.K_LEFT: (-dx, 0),
           pg.K_RIGHT: (dx, 0),
           pg.K_DOWN: (0, dy),
           pg.K_UP: (0, -dy)}

# In the first step, you need to draw a ball
treba_crtati = True
kraj = False
while not kraj:
    # if you need to update the image
    if treba_crtati:
        #  paint the window in white
        prozor.fill(pg.Color("black"))
        #  draw a spaceship
        prozor.blit(brod, (x - brod_sirina / 2, y - brod_visina / 2))
        #  update the contents of the window
        pg.display.update()
        treba_crtati = False

    #  process the first event that happens
    dogadjaj = pg.event.wait()
    # window exclusion
    if dogadjaj.type == pg.QUIT:
        kraj = True
    # keypress key press
    if dogadjaj.type == pg.KEYDOWN:
        if dogadjaj.key in pomeraj:
            #  move the center of the boat for the appropriate shift
            (DX, DY) = pomeraj[dogadjaj.key]
            x += DX
            y += DY
            # Since the ship is moved,  will recreate the scene again
            treba_crtati = True

# - * - acsection after-main - * -
# exclude the work of the PyGame library
pg.quit()
