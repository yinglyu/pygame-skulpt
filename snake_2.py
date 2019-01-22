# 贪吃蛇 2
# !/usr/bin/env python

import pygame
import sys
import time
import random

FPS = 5
#Pygame库启动
pygame.init()
fpsClock = pygame.time.Clock()
# 设置屏幕的高度和宽度
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
surface = pygame.Surface(screen.get_size())
surface = surface.convert()
surface.fill((255, 255, 255))
clock = pygame.time.Clock()

pygame.key.set_repeat(1, 40)

# 设置单位距离
# 根据屏幕的高度和宽度得到宽高的单位个数
GRIDSIZE = 10
GRID_WIDTH = SCREEN_WIDTH / GRIDSIZE
GRID_HEIGHT = SCREEN_HEIGHT / GRIDSIZE
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# 显示背景
screen.blit(surface, (0, 0))

# 画出一个像素格
def draw_box(surf, color, pos):
    r = pygame.Rect((pos[0], pos[1]), (GRIDSIZE, GRIDSIZE))
    pygame.draw.rect(surf, color, r)

# 定义 蛇类
class Snake(object):
    #定义 蛇的初始化函数
    def __init__(self):
        self.lose()
        self.color = (0, 0, 0)
    #定义 得到头的位置函数
    def get_head_position(self):
        return self.positions[0]

    def lose(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    
    def point(self, pt):
        if self.length > 1 and (pt[0] * -1, pt[1] * -1) == self.direction:
            return
        else:
            self.direction = pt

    # 定义移动函数
    def move(self):
        cur = self.positions[0]
        x, y = self.direction
        #根据身体的位置在头部增加一格，在尾部减少一格
        new = (((cur[0] + (x * GRIDSIZE)) % SCREEN_WIDTH), (cur[1] + (y * GRIDSIZE)) % SCREEN_HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.lose()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
    # 绘制
    def draw(self, surf):
        for p in self.positions:
            draw_box(surf, self.color, p)

# 定义 苹果类
class Apple(object):
    # 定义 初始化函数
    def __init__(self):
        self.position = (0, 0)
        self.color = (255, 0, 0)
        self.randomize()
    # 定义 随机生成位置函数
    def randomize(self):
        self.position = (random.randint(0, GRID_WIDTH - 1) * GRIDSIZE, random.randint(0, GRID_HEIGHT - 1) * GRIDSIZE)
    # 定义 绘制函数
    def draw(self, surf):
        draw_box(surf, self.color, self.position)

#定义 检查吃苹果情况函数
def check_eat(snake, apple):
    if snake.get_head_position() == apple.position:
        snake.length += 1
        apple.randomize()

# 主程序
if __name__ == '__main__':
    # 生成蛇和苹果
    snake = Snake()
    apple = Apple()
    # 循环
    while True:
        #判断事件
        for event in pygame.event.get():
            # 退出屏幕
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # 按下键盘
            elif event.type == pygame.KEYDOWN:
                #判断移动方向，并设置蛇的属性
                if event.key == pygame.K_UP:
                    snake.point(UP)
                elif event.key == pygame.K_DOWN:
                    snake.point(DOWN)
                elif event.key == pygame.K_LEFT:
                    snake.point(LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake.point(RIGHT)
        # 填充背景
        surface.fill((255, 255, 255))
        snake.move()
        check_eat(snake, apple)
        # 绘制图形
        snake.draw(surface)
        apple.draw(surface)
        # 输出信息
        font = pygame.font.Font(None, 36)
        text = font.render(str(snake.length), 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = 20
        #surface.blit(text, textpos)
        screen.blit(surface, (0, 0))
        # 更新屏幕
        pygame.display.flip()
        pygame.display.update()
        fpsClock.tick(FPS + snake.length / 3)

