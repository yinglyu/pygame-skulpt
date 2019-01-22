#俄罗斯方块

import random, time, pygame


FPS = 25
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
BOXSIZE = 20
BOARDWIDTH = 10
BOARDHEIGHT = 20
BLANK = '.'

MOVESIDEWAYSFREQ = 0.15
MOVEDOWNFREQ = 0.1

XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * BOXSIZE) / 2)
TOPMARGIN = WINDOWHEIGHT - (BOARDHEIGHT * BOXSIZE) - 5

#               R    G    B
WHITE       = (255, 255, 255)
GRAY        = (185, 185, 185)
BLACK       = (  0,   0,   0)
RED         = (155,   0,   0)
LIGHTRED    = (175,  20,  20)
GREEN       = (  0, 155,   0)
LIGHTGREEN  = ( 20, 175,  20)
BLUE        = (  0,   0, 155)
LIGHTBLUE   = ( 20,  20, 175)
YELLOW      = (155, 155,   0)
LIGHTYELLOW = (175, 175,  20)

BORDERCOLOR = BLUE
BGCOLOR = BLACK
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = GRAY
COLORS      = (     BLUE,      GREEN,      RED,      YELLOW)
LIGHTCOLORS = (LIGHTBLUE, LIGHTGREEN, LIGHTRED, LIGHTYELLOW)
assert len(COLORS) == len(LIGHTCOLORS) # 每种颜色有对应的亮色

TEMPLATEWIDTH = 5
TEMPLATEHEIGHT = 5

S_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '..OO.',
                     '.OO..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '...O.',
                     '.....']]

Z_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '.O...',
                     '.....']]

I_SHAPE_TEMPLATE = [['..O..',
                     '..O..',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     'OOOO.',
                     '.....',
                     '.....']]

O_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '.OO..',
                     '.....']]

J_SHAPE_TEMPLATE = [['.....',
                     '.O...',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..OO.',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '...O.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '.OO..',
                     '.....']]

L_SHAPE_TEMPLATE = [['.....',
                     '...O.',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '.O...',
                     '.....'],
                    ['.....',
                     '.OO..',
                     '..O..',
                     '..O..',
                     '.....']]

T_SHAPE_TEMPLATE = [['.....',
                     '..O..',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '..O..',
                     '.....']]

PIECES = {'S': S_SHAPE_TEMPLATE,
          'Z': Z_SHAPE_TEMPLATE,
          'J': J_SHAPE_TEMPLATE,
          'L': L_SHAPE_TEMPLATE,
          'I': I_SHAPE_TEMPLATE,
          'O': O_SHAPE_TEMPLATE,
          'T': T_SHAPE_TEMPLATE}


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
    pygame.display.set_caption('Tetromino')

    showTextScreen('Tetromino')
    
    while True: # game loop
        '''
        if random.randint(0, 1) == 0:
            pygame.mixer.music.load('tetrisb.mid')
        else:
            pygame.mixer.music.load('tetrisc.mid')
        pygame.mixer.music.play(-1, 0.0)
        '''
        runGame()
        '''
        pygame.mixer.music.stop()
        '''
        showTextScreen('Game Over')


def runGame():
    # setup variables for the start of the game
    board = getBlankBoard()
    lastMoveDownTime = time.time()
    lastMoveSidewaysTime = time.time()
    lastFallTime = time.time()
    movingDown = False # note: there is no movingUp variable
    movingLeft = False
    movingRight = False
    score = 0
    level, fallFreq = calculateLevelAndFallFreq(score)

    fallingPiece = getNewPiece()    
    nextPiece = getNewPiece()

    while True: # 游戏循环
        if fallingPiece == None:
            # 如果没有下落的形状，就在最上面增加之前显示的“下一个形状”，同时获得新的“下一个形状”
            fallingPiece = nextPiece
            nextPiece = getNewPiece()
            lastFallTime = time.time() # 重置 下降开始时间

            if not isValidPosition(board, fallingPiece):
                return # 如果下降的形状在非法的位置，游戏结束
        
        checkForQuit()
        
        for event in pygame.event.get(): # 处理事件循环
            if event.type == pygame.KEYUP:
                if (event.key == pygame.K_p):
                    # 暂停游戏
                    DISPLAYSURF.fill(BGCOLOR)
                    pygame.mixer.music.stop()
                    showTextScreen('Paused') # 按下按键后继续
                    pygame.mixer.music.play(-1, 0.0)
                    lastFallTime = time.time()
                    lastMoveDownTime = time.time()
                    lastMoveSidewaysTime = time.time()
                elif (event.key == pygame.K_LEFT or event.key == pygame.K_a):
                    movingLeft = False
                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d):
                    movingRight = False
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s):
                    movingDown = False

            elif event.type == pygame.KEYDOWN:
                # 左右移动形状
                if event.key == pygame.K_ESCAPE: # ying
                    terminate()
                elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and isValidPosition(board, fallingPiece, adjX=-1):
                    fallingPiece['x'] -= 1
                    movingLeft = True
                    movingRight = False
                    lastMoveSidewaysTime = time.time()

                elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and isValidPosition(board, fallingPiece, adjX=1):
                    fallingPiece['x'] += 1
                    movingRight = True
                    movingLeft = False
                    lastMoveSidewaysTime = time.time()

                # （如果空间允许）旋转形状
                elif (event.key == pygame.K_UP or event.key == pygame.K_w):
                    fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])
                elif (event.key == pygame.K_q): # rotate the other direction
                    fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])

                # 按向下键，下落速度加快
                elif (event.key == pygame.K_DOWN or event.key == pygame.K_s):
                    movingDown = True
                    if isValidPosition(board, fallingPiece, adjY=1):
                        fallingPiece['y'] += 1
                    lastMoveDownTime = time.time()

                # move the current piece all the way down
                elif event.key == pygame.K_SPACE:
                    movingDown = False
                    movingLeft = False
                    movingRight = False
                    for i in range(1, BOARDHEIGHT):
                        if not isValidPosition(board, fallingPiece, adjY=i):
                            break
                    fallingPiece['y'] += i - 1
        
        # 处理用户输入的移动命令
        if (movingLeft or movingRight) and time.time() - lastMoveSidewaysTime > MOVESIDEWAYSFREQ:
            if movingLeft and isValidPosition(board, fallingPiece, adjX=-1):
                fallingPiece['x'] -= 1
            elif movingRight and isValidPosition(board, fallingPiece, adjX=1):
                fallingPiece['x'] += 1
            lastMoveSidewaysTime = time.time()
        
        if movingDown and time.time() - lastMoveDownTime > MOVEDOWNFREQ and isValidPosition(board, fallingPiece, adjY=1):
            fallingPiece['y'] += 1
            lastMoveDownTime = time.time()
        
        # 根据速度设置，如果到了下降的时间，形状下降
        if time.time() - lastFallTime > fallFreq:
            # 判断形状是否着陆
            if not isValidPosition(board, fallingPiece, adjY=1):
                # 如果形状着陆，将其固定在板子上
                addToBoard(board, fallingPiece)
                score += removeCompleteLines(board)
                level, fallFreq = calculateLevelAndFallFreq(score)
                fallingPiece = None
            else:
                # 如果形状没有着陆，正常下降
                fallingPiece['y'] += 1
                lastFallTime = time.time()
        
        # 将所有元素绘制在屏幕上
        DISPLAYSURF.fill(BGCOLOR)
        drawBoard(board)
        drawStatus(score, level)
        drawNextPiece(nextPiece)
        if fallingPiece != None:
            drawPiece(fallingPiece)
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        
# 创建文本对象
def makeTextObjs(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()

# 结束处理
def terminate():
    pygame.quit()



def checkForKeyPress():
    # 浏览事件队列以查找 按键松开 事件。
    # 抓取 按键按下 事件以将其从事件队列中删除。
    checkForQuit()
'''
    for event in pygame.event.get([pygame.KEYDOWN, pygame.KEYUP]):
        if event.type == pygame.KEYDOWN:
            continue
        return event.key
    return None
'''

def showTextScreen(text):
    # 此函数在屏幕中心显示大文本，直到按下一个键。
    
    # 绘制文本投影
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTSHADOWCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(titleSurf, titleRect.center)

    # 绘制文字
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 3)
    DISPLAYSURF.blit(titleSurf, titleRect.center)

    # 画出额外的“按一个键进行播放”。
    pressKeySurf, pressKeyRect = makeTextObjs('Press a key to play.', BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect.center)
    
    '''
    while checkForKeyPress() == None:
        pygame.display.update()
        FPSCLOCK.tick()
    '''
    
# 检查是否为结束状态
def checkForQuit():
    
    for event in pygame.event.get(pygame.QUIT): #获取所有QUIT事件
        
        terminate() # 如果存在任何QUIT事件，则终止
        
    
    '''
    for event in pygame.event.get(pygame.KEYUP): # get all the KEYUP events
        if event.key == pygame.K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        
        # pygame.event.post(event) # put the other KEYUP event objects back
        
    '''
# 计算等级以及对应的下降速度
def calculateLevelAndFallFreq(score):
    # 根据分数，返回玩家所在的等级
    # 以及经过多少秒钟，直到掉落的一块空间落下。
    level = int(score / 10) + 1
    fallFreq = 0.27 - (level * 0.02)
    return level, fallFreq

# 生成新的形状
def getNewPiece():
    # 以随机旋转和颜色返回一个随机的新片段
    shape = random.choice(list(PIECES.keys()))
    newPiece = {'shape': shape,
                'rotation': random.randint(0, len(PIECES[shape]) - 1),
                'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
                'y': -2, #在板子上方开始（即小于0）
                'color': random.randint(0, len(COLORS)-1)}
    return newPiece

# 将形状加入游戏区域
def addToBoard(board, piece):
    # fill in the board based on piece's location, shape, and rotation
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if PIECES[piece['shape']][piece['rotation']][y][x] != BLANK:
                board[x + piece['x']][y + piece['y']] = piece['color']

# 创建空的游戏区域 数据结构
def getBlankBoard():
    # 根据形状的位置，形状和旋转填充板
    board = []
    for i in range(BOARDWIDTH):
        board.append([BLANK] * BOARDHEIGHT)
    return board

# 判断形状在游戏区域内
def isOnBoard(x, y):
    return x >= 0 and x < BOARDWIDTH and y < BOARDHEIGHT

# 判断形状的位置是否合法
def isValidPosition(board, piece, adjX=0, adjY=0):
    # 如果棋子在棋盘内并且没有碰撞，则返回True
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            isAboveBoard = y + piece['y'] + adjY < 0
            if isAboveBoard or PIECES[piece['shape']][piece['rotation']][y][x] == BLANK:
                continue
            if not isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):
                return False
            if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != BLANK:
                return False
    return True
# 判断一行填满
def isCompleteLine(board, y):
    # R如果行填充没有间隙的行，则返回True。
    for x in range(BOARDWIDTH):
        if board[x][y] == BLANK:
            return False
    return True

# 消除填满的行
def removeCompleteLines(board):
    # 移除板上已完成的所有行，将其上方的所有行向下移动，并返回完整线条的数量。
    numLinesRemoved = 0
    y = BOARDHEIGHT - 1 # y轴从板底部开始
    while y >= 0:
        if isCompleteLine(board, y):
            # 删除完成的行并将框向下拉一行。
            for pullDownY in range(y, 0, -1):
                for x in range(BOARDWIDTH):
                    board[x][pullDownY] = board[x][pullDownY-1]
            # 将最上面的行设置为空白。
            for x in range(BOARDWIDTH):
                board[x][0] = BLANK
            numLinesRemoved += 1
            # 注意循环的下一次迭代，y是相同的。
            # 这样如果被拉下的行也是如此
            # 完成后，它将被删除。
        else:
            y -= 1 # 继续检查下一行
    return numLinesRemoved

# 像素转换
def convertToPixelCoords(boxx, boxy):
    # 将给定的板子xy坐标转换为真正的xy
    # 屏幕上位置的坐标。
    return (XMARGIN + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE))

# 画组成形状的格子
def drawBox(boxx, boxy, color, pixelx=None, pixely=None):
    # 画一个盒子（每个tetromino片有四个盒子）
    # 在板上的xy坐标处。或者，如果pixelx＆pixely
    # 指定, 绘制到存储的像素坐标
    # pixelx＆pixely（这用于“下一个形状”）。
    if color == BLANK:
        return
    if pixelx == None and pixely == None:
        pixelx, pixely = convertToPixelCoords(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, COLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 1, BOXSIZE - 1))
    pygame.draw.rect(DISPLAYSURF, LIGHTCOLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 4, BOXSIZE - 4))

# 画出游戏区域
def drawBoard(board):
    # 画出板子边框
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (XMARGIN - 3, TOPMARGIN - 7, (BOARDWIDTH * BOXSIZE) + 8, (BOARDHEIGHT * BOXSIZE) + 8), 5)

    # 填写板子的背景
    pygame.draw.rect(DISPLAYSURF, BGCOLOR, (XMARGIN, TOPMARGIN, BOXSIZE * BOARDWIDTH, BOXSIZE * BOARDHEIGHT))
    # 画出板子上的各个盒子
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            drawBox(x, y, board[x][y])

# 显示得分等级信息
def drawStatus(score, level):
    # 绘制得分文本
    
    scoreSurf = BASICFONT.render('Score: %s' % score, True, TEXTCOLOR)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 150, 20)
    DISPLAYSURF.blit(scoreSurf, scoreRect.topleft)

    # 绘制关卡文字
    levelSurf = BASICFONT.render('Level: %s' % level, True, TEXTCOLOR)
    levelRect = levelSurf.get_rect()
    levelRect.topleft = (WINDOWWIDTH - 150, 50)
    DISPLAYSURF.blit(levelSurf, levelRect.topleft)
    
# 画出形状
def drawPiece(piece, pixelx=None, pixely=None):
    shapeToDraw = PIECES[piece['shape']][piece['rotation']]
    if pixelx == None and pixely == None:
        # 如果未指定pixelx和pixely，请使用存储在片段数据结构中的位置
        pixelx, pixely = convertToPixelCoords(piece['x'], piece['y'])

    # 绘制构成该块的每个盒子
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if shapeToDraw[y][x] != BLANK:
                drawBox(None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))

# 画出下一个形状的提醒
def drawNextPiece(piece):
    # 绘制“next”文本
    nextSurf = BASICFONT.render('Next:', True, TEXTCOLOR)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (WINDOWWIDTH - 120, 80)
    DISPLAYSURF.blit(nextSurf, nextRect.topleft)
    
    # 画出“下一个”形状
    drawPiece(piece, pixelx=WINDOWWIDTH-120, pixely=100)
    

if __name__ == '__main__':
    main()