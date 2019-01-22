#数字时钟
import pygame

# 定义一些颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.init()

# 设置屏幕的高度和宽度
size = [700, 500]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")

# 循环直到用户单击关闭按钮。
done = False

# 用于管理屏幕更新的速度
clock = pygame.time.Clock()

font = pygame.font.Font(None, 25)

frame_count = 0
frame_rate = 60
start_time = 90

# --------主程序循环-----------
while not done:
    for event in pygame.event.get():  # 用户做了一些事
        if event.type == pygame.QUIT:  # 如果用户点击关闭
            done = True  # 标记已完成，因此退出此循环

    # 设置屏幕背景
    screen.fill(WHITE)

    # 要绘制的所有代码应该在此注释下方

    # ---计时器增长---
    # 计算总秒数
    total_seconds = frame_count // frame_rate

    # 除以60得到总分钟数
    minutes = total_seconds // 60

    # 使用模数（余数）来获得秒数
    seconds = total_seconds % 60

    # 使用python字符串格式化以前导零格式化
    output_string = "Time: {0:02}:{1:02}".format(minutes, seconds)

    # Blit到屏幕
    text = font.render(output_string, True, BLACK)
    screen.blit(text, [250, 250])

    # ---计时器终止---
    # ---计时器增长---
    # 计算总秒数
    total_seconds = start_time - (frame_count // frame_rate)
    if total_seconds < 0:
        total_seconds = 0

    # 除以60得到总分钟数
    minutes = total_seconds // 60

    # 使用模数（余数）来获得秒数
    seconds = total_seconds % 60

    # 使用python字符串格式化以前导零格式化
    output_string = "Time left: {0:02}:{1:02}".format(minutes, seconds)

    # Blit到屏幕
    text = font.render(output_string, True, BLACK)

    screen.blit(text, [250, 280])

    # 要绘制的所有代码都应该在这个评论上方
    frame_count += 1

    # 限制每秒帧数
    clock.tick(frame_rate)

    # 继续使用绘制的内容更新屏幕。
    pygame.display.flip()

# 请保持无操作友好。如果缺少这一行，该程序将“挂起”
# 退出。
pygame.quit()