#贪吃蛇

import pygame as pg
from random import randint
#启动pygame
pg.init()
#设置画板单位
side = 30
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
#设置初始蛇的坐标
snake = [(7, 3), (7, 4)]
#初始方向设为向右
direction = 0

#随机放置苹果
def place_apple():
    #在画板范围内取随机横纵坐标
    a = (randint(0, w - 1), randint(0, h - 1))
    #防止苹果出现在蛇的覆盖范围内
    while a in snake:
        a = (randint(0, w - 1), randint(0, h - 1))
    return a

#初始调用函数，放置第一个苹果
apple = place_apple()

#检查是否发生碰撞
def check_collisions():
    #定义头是蛇的坐标数组中的最后一个元素
    head = snake[-1]
    #检查头是否碰到身体
    for i in range(len(snake) - 1):
        if head == snake[i]:
            return 2
    #检查头是否碰到边界
    if head[0] >= w or head[0] < 0:
        return 3
    if head[1] >= h or head[1] < 0:
        return 3
    #检查头是否碰到苹果
    if head == apple:
        return 1
    #没有发生任何碰撞
    return 0


clock = pg.time.Clock()
f = pg.font.SysFont('console', 24, True)

while True:
    #程序运行速度
    clock.tick(5)
    #获得事件
    for e in pg.event.get():
        if e.type == pg.QUIT:
            #按下esc停止游戏
            pg.quit()
            break
        if e.type == pg.KEYDOWN:
            #按下任何按键启动游戏
            if game_running == 0:
                game_runnig = 1
            #按下空格重置游戏
            if e.key == pg.K_SPACE:
                game_running = 0
                snake = [(7, 3), (7, 4)]
                direction = 0
                apple = place_apple()
            #通过循环判断是否按下了4个方向键中的一个
            for i in range(4):
                if e.key == dirs[i] and direction != (i + 2) % 4:
                    direction = i
    #游戏运行状态为2，game over
    if game_running == 2:
        disp.fill(pg.Color("black"))
        disp.blit(f.render("Game over!", False, pg.Color("blue")), (3 * side, 3 * side))
        pg.display.update()
        game_running = 3
    #游戏运行状态为3，跳出循环结束游戏
    if game_running == 3:
        continue
    #蛇的坐标数组根据移动的方向增加一个元素（在头部）
    snake.append((snake[-1][0] + dx[direction], snake[-1][1] + dy[direction]))
    #得到 检查碰撞 的返回状态
    coll = check_collisions()
    #出现错误碰撞 设置游戏状态
    if coll >= 2:
        game_running = 2
        pass
    #吃到苹果，放置新的苹果
    elif coll == 1:
        apple = place_apple()
        #由于之前在蛇的头部增加了一个元素，没有删除尾部的元素，因此蛇的长度增加
        pass
    #没吃到苹果
    elif coll == 0:
        #删除尾部的元素，蛇的长度不变
        snake.pop(0)
    #背景填充黑色
    disp.fill(pg.Color("black"))
    #根据蛇的坐标画蛇
    for i in range(len(snake)):
        pg.draw.rect(disp, pg.Color("green"), pg.Rect(snake[i][0] * side, snake[i][1] * side, side, side))
    #根据苹果的坐标画苹果
    pg.draw.rect(disp, pg.Color("red"), pg.Rect(apple[0] * side, apple[1] * side, side, side))
    #刷新画板
    pg.display.update()
