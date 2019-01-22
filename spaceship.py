# 宇宙飞船

#  -*-  acsection general-init  -*- 
import pygame as pg, random

# PyGame库初始化
pg.init()

# 设置键盘事件 - 之后生成第一个事件
# 50ms，以及25ms后的每一次
pg.key.set_repeat(50, 25)

# 设置窗口标题
pg.display.set_caption("setanje broda")

# 打开一个大小为400x400像素的窗口
(sirina, visina) = (400, 400)
prozor = pg.display.set_mode((sirina, visina))

#  -*-  acsection main  -*- 
# 加载宇宙飞船的图像
brod = pg.image.load('../../../../assets/pygame/spaceship.png')
# 读取图像的尺寸
brod_sirina = brod.get_width()
brod_visina = brod.get_height()

# 窗口中心的坐标
(x, y) = (sirina / 2, visina / 2)
# 按x和y坐标移动
(dx, dy) = (10, 10)

pomeraj = {pg.K_LEFT: (-dx, 0),
           pg.K_RIGHT: (dx, 0),
           pg.K_DOWN: (0, dy),
           pg.K_UP: (0, -dy)}

# 在第一步中，需要画一个球
treba_crtati = True
kraj = False
while not kraj:
    # 如果需要更新图像
    if treba_crtati:
        # 把窗户涂成白色
        prozor.fill(pg.Color("black"))
        # 画一艘宇宙飞船
        prozor.blit(brod, (x - brod_sirina / 2, y - brod_visina / 2))
        # 更新窗口的内容
        pg.display.update()
        treba_crtati = False

    # 处理发生的第一个事件
    dogadjaj = pg.event.wait()
    # 推出窗口
    if dogadjaj.type == pg.QUIT:
        kraj = True
    # 按下按键
    if dogadjaj.type == pg.KEYDOWN:
        if dogadjaj.key in pomeraj:
            # 移动船的中心进行适当的变化
            (DX, DY) = pomeraj[dogadjaj.key]
            x += DX
            y += DY
            # 飞船移动后，将再次重建场景
            treba_crtati = True

#  -*-  acsection after-main  -*- 
# 退出PyGame库
pg.quit()
