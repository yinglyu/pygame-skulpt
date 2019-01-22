#反弹球
import pygame
import random

# 定义一些颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500
BALL_SIZE = 25


class Ball:
    """
    Class to keep track of a ball's location and vector.
    """
    def __init__(self):
        self.x = 0
        self.y = 0
        self.change_x = 0
        self.change_y = 0


def make_ball():
    """
    Function to make a new, random ball.
    """
    ball = Ball()
    # 球的起始位置。
    # 考虑到球的大小，所以我们不会在边缘放球。
    ball.x = random.randrange(BALL_SIZE, SCREEN_WIDTH - BALL_SIZE)
    ball.y = random.randrange(BALL_SIZE, SCREEN_HEIGHT - BALL_SIZE)

    #矩形的速度和方向
    ball.change_x = random.randrange(-2, 3)
    ball.change_y = random.randrange(-2, 3)

    return ball


def main():
    """
    This is our main program.
    """
    pygame.init()

    # 设置屏幕的高度和宽度
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Bouncing Balls")

    # 循环直到用户单击关闭按钮。
    done = False

    # 用于管理屏幕更新的速度
    clock = pygame.time.Clock()

    ball_list = []

    ball = make_ball()
    ball_list.append(ball)

    # -------- 主程序循环 -----------
    while not done:
        # --- 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                # 空格键！产生一个新球。
                if event.key == pygame.K_SPACE:
                    ball = make_ball()
                    ball_list.append(ball)

        # --- 逻辑
        for ball in ball_list:
            # 移动球的中心
            ball.x += ball.change_x
            ball.y += ball.change_y

            # 如果需要，可以弹球
            if ball.y > SCREEN_HEIGHT - BALL_SIZE or ball.y < BALL_SIZE:
                ball.change_y *= -1
            if ball.x > SCREEN_WIDTH - BALL_SIZE or ball.x < BALL_SIZE:
                ball.change_x *= -1

        #  --- 绘制
        # 设置屏幕背景
        screen.fill(BLACK)

        # 画球
        for ball in ball_list:
            pygame.draw.circle(screen, WHITE, [ball.x, ball.y], BALL_SIZE)

        # --- 封装
        # 限制为每秒60帧
        clock.tick(60)

        # 继续使用我们绘制的内容更新屏幕。
        pygame.display.flip()

    # 关闭所有内容
    pygame.quit()

if __name__ == "__main__":
    main()
