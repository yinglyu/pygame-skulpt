#Flappy Bird

import pygame as pg
from random import randint

pg.init()
#设置画板单位
side = 32
#设置画板宽高
w = 17
h = 15
disp = pg.display.set_mode((w * side, h * side))
#设置运行状态
game_running = 0
#设置方向键对应的方向单位坐标
dirs = [pg.K_RIGHT, pg.K_DOWN, pg.K_LEFT, pg.K_UP]
dx = [1, 0, -1, 0]
dy = [0, 1, 0, -1]
#设置初始像素鸟占的坐标
bird = [(3,4), (2,4), (2,5), (3,5)]
#柱子的缝隙起始位置
pillar_c = []
#柱子的纵轴坐标二维数组
pillar_y = []
#柱子的横轴坐标一维数组
pillar_x = []


#自由落体时间
free_time = 0
#得分
point = 0

#生成柱子占据的纵坐标列表
def place_pillar(crack_h):
    #crack_h = randint(0, h - 1 - 5)
    pillar = []

    for i in range (0, crack_h):
        pillar.append(i)
    for i in range (crack_h + 5, 16):
        pillar.append(i)
    return pillar


#柱子缝隙的起始坐标增加新元素
pillar_c.append(randint(0, h - 1 - 5))
#柱子占据的纵坐标列表增加新元素
pillar_y.append(place_pillar(pillar_c[-1]))
#柱子的横坐标增加新元素
pillar_x.append(16)

#检查是否发生碰撞
def check_collisions(): 
    #对于每个柱子
    for i in range(len(pillar_x)):
        #判断柱子是否移动到像素小鸟的未知
        if pillar_x[i] == bird[0][0] or pillar_x[i] == bird[1][0]:
            #判断小鸟最上面的坐标是否在缝隙之上
            if bird[0][1] < pillar_c[i] :  
                print ("too high")
                return 3
            #判断小鸟最下的坐标是否在缝隙之下
            if bird[3][1] > pillar_c[i] + 4 :
                print ("too low")
                return 3
    return 0

clock = pg.time.Clock()
f = pg.font.SysFont('console', 24, True)

while True:
    #推进速度
    clock.tick(5)
    #初始化方向为0
    bird_dirs = 0
    #获得事件
    for e in pg.event.get():
        #按下esc停止游戏
        if e.type == pg.QUIT:
            pg.quit()
            break
        if e.type == pg.KEYDOWN:
            #按下按键启动游戏
            if game_running == 0:
                game_runnig = 1
            #按下空格小鸟方向向上
            if e.key == pg.K_SPACE:
                bird_dirs = 3
            
            for i in range(4):
                #当按 上或下按键时 更新鸟的方向
                if e.key == dirs[i] :
                    if (i % 2) == 1:
                        bird_dirs = i


    #游戏运行状态为2，game over
    if game_running == 2:
        #disp.fill(pg.Color("black"))
        disp.blit(f.render("Game over!", False, pg.Color("red")), (3 * side, 3 * side))
        disp.blit(f.render(str(point), False, pg.Color("green")), (13 * side, 3 * side))
        pg.display.update()
        game_running = 3
        
    #小鸟方向不为0时，进行自由落体
    if bird_dirs != 0:
        #小鸟方向3为向上
        if bird_dirs == 3:
            #将自由落体时间重置为0
            free_time = 0
        #根据选择的向上或向下移动小鸟
        for j in range(4):
            bird.append((bird[j][0] + dx[bird_dirs], bird[j][1] + dy[bird_dirs]))
        #print (bird)
        for j in range(4):
            bird.pop(0)  
        #print (bird)

    #自由落体时间增加
    free_time = free_time + 1
    
    #根据自由落体公式得到第 free_time 个单位时间内移动的距离，移动小鸟
    for j in range(4):
        bird.append((bird[j][0] , bird[j][1] + free_time * 0.25 - 0.125))
    for j in range(4):
        bird.pop(0)  

	#对于每一个柱子
    for i in range(len(pillar_x)):
        #改变柱子的横坐标，向左移动柱子
        if pillar_x[i] > 0:
            pillar_x[i] = pillar_x[i] - 1
            
        else:
            #当柱子的移除画面外时，删除柱子
            pillar_c.pop(0)
            pillar_x.pop(0)
            pillar_y.pop(0)
            #创建新的柱子
            pillar_c.append(randint(0, h - 1 - 5))
            pillar_y.append(place_pillar(pillar_c[-1]))
            pillar_x.append(16)
            #增加分数
            point = point + 1
    #背景填充
    disp.fill(pg.Color("black")) 

    # 画像素鸟
    for i in range(len(bird)): 
        pg.draw.rect(disp, pg.Color("yellow"), pg.Rect(bird[i][0] * side, bird[i][1] * side, side, side))
    # 画柱子
    for j in range(len(pillar_x)):
        if pillar_x[j] > 0:
            for i in range(len(pillar_y[j])):
                pg.draw.rect(disp, pg.Color("blue"), pg.Rect(pillar_x[j] * side, pillar_y[j][i] * side, side, side))
    # 获取撞击状态
    coll = check_collisions()
    if coll >= 2:
        game_running = 2
    else:
        #展示分数
        disp.blit(f.render(str(point), False, pg.Color("green")), (13 * side, 3 * side))
        #刷新画板
        pg.display.update()
