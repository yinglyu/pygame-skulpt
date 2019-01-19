#Flappy Bird

import pygame as pg
from random import randint

pg.init()
side = 32
w = 17
h = 15
disp = pg.display.set_mode((w * side, h * side))

game_running = 0

#设置方向对应的反应

dirs = [pg.K_RIGHT, pg.K_DOWN, pg.K_LEFT, pg.K_UP]
dx = [1, 0, -1, 0]
dy = [0, 1, 0, -1]

bird = [(3,4), (2,4), (2,5), (3,5)]
pillar_c = []
pillar_y = []
pillar_x = []


direction = 0
free_time = 0
point = 0


def place_pillar(crack_h):
    #crack_h = randint(0, h - 1 - 5)
    pillar = []

    for i in range (0, crack_h):
        pillar.append(i)
    for i in range (crack_h + 5, 16):
        pillar.append(i)
    return pillar



pillar_c.append(randint(0, h - 1 - 5))
pillar_y.append(place_pillar(pillar_c[-1]))
pillar_x.append(16)


def check_collisions(): 
#检查是否发生碰撞

    for i in range(len(pillar_x)):

        if pillar_x[i] == bird[0][0] or pillar_x[i] == bird[1][0]:
            if bird[0][1] < pillar_c[i] :  
                print ("too high")
                return 3
            if bird[3][1] > pillar_c[i] + 4 :
                print ("too low")
                return 3
    return 0

clock = pg.time.Clock()
f = pg.font.SysFont('console', 24, True)

while True:
    clock.tick(5)
    bird_dirs = 0
    for e in pg.event.get():
        if e.type == pg.QUIT:#按下esc停止
            pg.quit()
            break
        if e.type == pg.KEYDOWN:
            if game_running == 0:
                game_runnig = 1
            if e.key == pg.K_SPACE:
                bird_dirs = 3
            
            for i in range(4):#按下方向键，可旋转90度
                if e.key == dirs[i] :
                    if (i % 2) == 1:
                        bird_dirs = i
                    if direction != (i + 2) % 4:
                        direction = i


    if game_running == 2:
        #disp.fill(pg.Color("black"))
        disp.blit(f.render("Game over!", False, pg.Color("blue")), (3 * side, 3 * side))
        disp.blit(f.render(str(point), False, pg.Color("green")), (13 * side, 3 * side))
        pg.display.update()
        game_running = 3
    if game_running == 3:
        continue
    if bird_dirs != 0:
        if bird_dirs == 3:
            free_time = 0
        for j in range(4):
            bird.append((bird[j][0] + dx[bird_dirs], bird[j][1] + dy[bird_dirs]))
        #print (bird)
        for j in range(4):
            bird.pop(0)  
        #print (bird)
    free_time = free_time + 1
    for j in range(4):
        bird.append((bird[j][0] , bird[j][1] + free_time * 0.25 - 0.125))
    for j in range(4):
        bird.pop(0)  
    #print (bird)
    for i in range(len(pillar_x)):
        if pillar_x[i] > 0:
            pillar_x[i] = pillar_x[i] - 1
        else:
            pillar_c.pop(0)
            pillar_x.pop(0)
            pillar_y.pop(0)
            pillar_c.append(randint(0, h - 1 - 5))
            pillar_y.append(place_pillar(pillar_c[-1]))
            pillar_x.append(16)
            point = point + 1
        #print (pillar_y)
        #print (pillar_x) 
    '''          
    coll = check_collisions()
    if coll >= 2:
        game_running = 2
        pass
    '''
    disp.fill(pg.Color("black"))


    for i in range(len(bird)):
        pg.draw.rect(disp, pg.Color("yellow"), pg.Rect(bird[i][0] * side, bird[i][1] * side, side, side))
    for j in range(len(pillar_x)):
        if pillar_x[j] > 0:
            for i in range(len(pillar_y[j])):
                pg.draw.rect(disp, pg.Color("blue"), pg.Rect(pillar_x[j] * side, pillar_y[j][i] * side, side, side))
    coll = check_collisions()
    if coll >= 2:
        game_running = 2
    else:
        
        disp.blit(f.render(str(point), False, pg.Color("green")), (13 * side, 3 * side))
        pg.display.update()
