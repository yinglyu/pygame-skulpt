# -*- coding:utf-8 -*-
'''
经典俄罗斯方块
游戏基于python2.7、pygame1.9.2b8编写。

游戏注解中出现的术语解释：
舞台：整个游戏界面，包括堆叠区、成绩等显示区，下个出现方块预告区。
堆叠区：游戏方块和活动方块形状堆放区域，游戏中主要互动区。
方块（基础方块）：这里的方块是对基础的小四方形统称，每个方块就是一个正方形。
方块形状：指一组以特定方式组合在一起的方块，也就是大家常说的下落方块形状，比如长条，方形，L形等。
固实方块：特指堆叠区中不能再进行移动，可被消除的基础方块集合。

version:1.0
author:lykyl
createdate:2016.9.29
'''
import sys
import random,copy
import pygame as pg
from pygame.locals import *

'''
常量声明
'''
EMPTY_CELL=0        #空区标识，表示没有方块
FALLING_BLOCK=1     #下落中的方块标识，也就是活动方块。
STATIC_BLOCK=2      #固实方块标识

'''
全局变量声明
变量值以sysInit函数中初始化后的结果为准
'''
defaultFont=None        #默认字体
screen=None     #屏幕输出对象
backSurface=None        #图像输出缓冲画板
score=0     #玩家得分记录
clearLineScore=0        #玩家清除的方块行数
level=1     #关卡等级
clock=None      #游戏时钟
nowBlock=None       #当前下落中的方块
nextBlock=None      #下一个将出现的方块
fallSpeed=10        #当前方块下落速度
beginFallSpeed=fallSpeed        #游戏初始时方块下落速度
speedBuff=0     #下落速度缓冲变量
keyBuff=None        #上一次按键记录
maxBlockWidth=10        #舞台堆叠区X轴最大可容纳基础方块数
maxBlockHeight=18       #舞台堆叠区Y轴最大可容纳基础方块数
blockWidth=30       #以像素为单位的基础方块宽度
blockHeight=30      #以像素为单位的基础方块高度
blocks=[]       #方块形状矩阵四维列表。第一维为不同的方块形状，第二维为每个方块形状不同的方向（以0下标起始，一共四个方向），第三维为Y轴方块形状占用情况，第四维为X轴方块形状占用情况。矩阵中0表示没有方块，1表示有方块。
stage=[]        #舞台堆叠区矩阵二维列表，第一维为Y轴方块占用情况，第二维为X轴方块占用情况。矩阵中0表示没有方块，1表示有固实方块，2表示有活动方块。
gameOver=False      #游戏结束标志
pause=False     #游戏暂停标志


def printTxt(content,x,y,font,screen,color=(255,255,255)):
    '''显示文本
    args:
        content:待显示文本内容
        x,y:显示坐标
        font:字体
        screen:输出的screen
        color:颜色
    '''
    imgTxt=font.render(content,True,color)
    screen.blit(imgTxt,(x,y))
    
    
class point(object):
    '''平面坐标点类
    attributes:
        x,y:坐标值
    '''
    def __init__(self,x,y):
        self.__x=x
        self.__y=y
    
    def getx(self):
        return self.__x
    
    def setx(self,x):
        self.__x=x
    
    x=property(getx,setx)
    
    def gety(self):
        return self.__y
    
    def sety(self,y):
        self.__y=y
    
    y=property(gety,sety)    
    
    def __str__(self):
        return "{x:"+"{:.0f}".format(self.__x)+",y:"+"{:.0f}".format(self.__y)+"}"


class blockSprite(object):
    '''
    方块形状精灵类
    下落方块的定义全靠它了。
    attributes:
        shape:方块形状编号
        direction:方块方向编号
        xy,方块形状左上角方块坐标
        block:方块形状矩阵
    '''
    def __init__(self,shape,direction,xy):
        self.shape=shape
        self.direction=direction
        self.xy=xy
    
    def chgDirection(self,direction):
        '''
        改变方块的方向
        args:
            direction:1为向右转，0为向左转。
        '''
        dirNumb=len(blocks[self.shape])-1
        if direction==1:
            self.direction+=1
            if self.direction>dirNumb:
                self.direction=0
        else:
            self.direction-=1
            if self.direction<0:
                self.direction=dirNumb
    
    def clone(self):
        '''
        克隆本体
        return:
            返回自身的克隆
        '''
        return blockSprite(self.shape,self.direction,point(self.xy.x,self.xy.y))
        
    def _getBlock(self):
        return blocks[self.shape][self.direction]
        
    block = property(_getBlock)


def getConf(fileName):
    '''
    从配置文件中读取方块形状数据
    每个方块以4*4矩阵表示形状，配置文件每行代表一个方块，用分号分隔矩阵行，用逗号分隔矩阵列，0表示没有方块，1表示有方块。
    因为此程序只针对俄罗斯方块的经典版，所以方块矩阵大小以硬编码的形式写死为4*4。
    args:
        fileName:配置文件名
    '''
    global blocks   #blocks记录方块形状。
    with open(fileName,'rt') as fp:
        for temp in fp.readlines():
            blocks.append([])
            blocksNumb=len(blocks)-1
            blocks[blocksNumb]=[]
            #每种方块形状有四个方向，以0～3表示。配置文件中只记录一个方向形状，另外三个方向的矩阵排列在sysInit中通过调用transform计算出来。
            blocks[blocksNumb].append([])
            row=temp.split(";")
            for r in range(len(row)):
                col=[]
                ct=row[r].split(",")
                #对矩阵列数据做规整，首先将非“1”的值全修正成“0”以过滤空字串或回车符。
                for c in range(len(ct)):
                    if ct[c]!="1":
                        col.append(0)
                    else:
                        col.append(1)
                #将不足4列的矩阵通过补“0”的方式，补足4列。
                for c in range(len(ct)-1,3):
                    col.append(0)
                blocks[blocksNumb][0].append(col)
            #如果矩阵某行没有方块，则配置文件中可以省略此行，程序会在末尾补上空行数据。
            for r in range(len(row)-1,3):
                blocks[blocksNumb][0].append([0,0,0,0])
            blocks[blocksNumb][0]=formatBlock(blocks[blocksNumb][0])


def sysInit():
    '''
    系统初始化
    包括pygame环境初始化，全局变量赋值，生成每个方块形状的四个方向矩阵。
    '''
    global defaultFont,screen,backSurface,clock,blocks,stage,gameOver,fallSpeed,beginFallSpeed,nowBlock,nextBlock,score,level,clearLineScore,pause
    
    #pygame运行环境初始化
    pg.init()
    screen=pg.display.set_mode((500,550))
    backSurface=pg.Surface((screen.get_rect().width,screen.get_rect().height))
    pg.display.set_caption("block")
    clock=pg.time.Clock()
    pg.mouse.set_visible(False)
    
    #游戏全局变量初始化
    defaultFont=pg.font.Font("res/font/yh.ttf",16)        #yh.ttf这个字体文件请自行上网搜索下载，如果找不到就随便用个ttf格式字体文件替换一下。
    nowBlock=None
    nextBlock=None
    gameOver=False
    pause=False
    score=0
    level=1
    clearLineScore=0
    beginFallSpeed=20
    fallSpeed=beginFallSpeed-level*2
    
    #初始化游戏舞台
    stage=[]
    for y in range(maxBlockHeight):
        stage.append([])
        for x in range(maxBlockWidth):
            stage[y].append(EMPTY_CELL)
            
    #生成每个方块形状4个方向的矩阵数据
    for x in range(len(blocks)):
        #因为重新开始游戏时会调用sysinit对系统所有参数重新初始化，为了避免方向矩阵数据重新生成，需要在此判断是否已经生成，如果已经生成则跳过。
        if len(blocks[x])<2:
            t=blocks[x][0]
            for i in range(3):
                t=transform(t,1)
                blocks[x].append(formatBlock(t))
                

#transform,removeTopBlank,formatBlock这三个函数只为生成方块形状4个方向矩阵使用，在游戏其他环节无作用,在阅读程序时可以先跳过。
def transform(block,direction=0):  
    '''
    生成指定方块形状转换方向后的矩阵数据
    args:
        block:方块形状矩阵参数
        direction:转换的方向，0代表向左，1代表向右
    return:
        变换方向后的方块形状矩阵参数
    '''
    result=[]
    for y in range(4):
        result.append([])
        for x in range(4):
            if direction==0:
                result[y].append(block[x][3-y])
            else:
                result[y].append(block[3-x][y])
    return result 


def removeTopBlank(block):
    '''
    清除方块矩阵顶部空行数据
    args:
        block:方块开关矩阵
    return:
        整理后的方块矩阵数据
    '''
    result=copy.deepcopy(block)
    blankNumb=0
    while sum(result[0])<1 and blankNumb<4:
        del result[0]
        result.append([0,0,0,0])
        blankNumb+=1
    return result
    

def formatBlock(block):
    '''
    整理方块矩阵数据，使方块在矩阵中处于左上角的位置
    args:
        block:方块开关矩阵
    return:
        整理后的方块矩阵数据
    '''
    result=removeTopBlank(block)
    #将矩阵右转，用于计算左侧X轴线空行,计算完成后再转回
    result=transform(result, 1)
    result=removeTopBlank(result)
    result=transform(result,0)
    return result


def checkDeany(sprite):
    '''
    检查下落方块是否与舞台堆叠区中固实方块发生碰撞
    args:
        sprite:下落方块
    return:
        如果发生碰撞则返回True
    '''
    topX=sprite.xy.x
    topY=sprite.xy.y
    for y in range(len(sprite.block)):
        for x in range(len(sprite.block[y])):
            if sprite.block[y][x]==1:
                yInStage=topY+y
                xInStage=topX+x
                if yInStage>maxBlockHeight-1 or yInStage<0:
                    return True
                if xInStage>maxBlockWidth-1 or xInStage<0:
                    return True
                if stage[yInStage][xInStage]==STATIC_BLOCK:
                    return True                
    return False


def checkLine():
    '''
    检测堆叠区是否有可消除的整行固实方块
    根据检测结果重新生成堆叠区矩阵数据，调用updateScore函数更新玩家积分等数据。
    return:
        本轮下落周期消除的固实方块行数
    '''
    global stage
    clearCount=0    #本轮下落周期消除的固实方块行数
    tmpStage=[]     #根据消除情况新生成的堆叠区矩阵，在有更新的情况下会替换全局的堆叠区矩阵。
    
    for y in stage:
        #因为固实方块在堆叠矩阵里以2表示，所以判断方块是否已经满一整行只要计算矩阵行数值合计是否等于堆叠区X轴最大方块数*2就可以。
        if sum(y)>=maxBlockWidth*2:
            tmpStage.insert(0,maxBlockWidth*[0])
            clearCount+=1
        else:
            tmpStage.append(y)
    if clearCount>0:
        stage=tmpStage
        updateScore(clearCount)
    return clearCount
   

def updateStage(sprite,updateType=1):
    '''
    将下落方块坐标数据更新到堆叠区数据中。下落方块涉及的坐标在堆叠区中用数字1标识，固实方块在堆叠区中用数字2标识。
    args:
        sprite:下落方块形状
        updateType:更新方式，0代表清除，1代表动态加入,2代表固实加入。
    '''
    
    global stage
    topX=sprite.xy.x
    topY=sprite.xy.y
    for y in range(len(sprite.block)):
        for x in range(len(sprite.block[y])):
            if sprite.block[y][x]==1:
                if updateType==0:
                    if stage[topY+y][topX+x]==FALLING_BLOCK:
                        stage[topY+y][topX+x]=EMPTY_CELL
                elif updateType==1:
                    if stage[topY+y][topX+x]==EMPTY_CELL:
                        stage[topY+y][topX+x]=FALLING_BLOCK
                else:
                    stage[topY+y][topX+x]=STATIC_BLOCK


def updateScore(clearCount):
    '''
    更新玩家游戏记录，包括积分、关卡、消除方块行数，并且根据关卡数更新方块下落速度。
    args:
        clearCount:本轮下落周期内清除的方块行数。
    return:
        当前游戏的最新积分
    '''
    global score,fallSpeed,level,clearLineScore
    
    prizePoint=0    #额外奖励分数，同时消除的行数越多，奖励分值越高。
    if clearCount>1:
        if clearCount<4:
            prizePoint=clearCount**clearCount
        else:
            prizePoint=clearCount*5
    score+=(clearCount+prizePoint)*level
    #玩得再牛又有何用？ :)
    if score>99999999:
        score=0
    clearLineScore+=clearCount
    if clearLineScore>100:
        clearLineScore=0
        level+=1
        if level>(beginFallSpeed/2):
            level=1
            fallSpeed=beginFallSpeed
        fallSpeed=beginFallSpeed-level*2
    return score


def drawStage(drawScreen):
    '''
    在给定的画布上绘制舞台
    args:
        drawScreen:待绘制的画布
    '''
    staticColor=30,102,76       #固实方块颜色
    activeColor=255,239,0       #方块形状颜色
    fontColor=200,10,120        #文字颜色
    baseRect=0,0,blockWidth*maxBlockWidth+1,blockHeight*maxBlockHeight+1        #堆叠区方框
    
    #绘制堆叠区外框
    drawScreen.fill((180,200,170))
    pg.draw.rect(drawScreen, staticColor, baseRect,1)
    
    #绘制堆叠区内的所有方块，包括下落方块形状
    for y in range(len(stage)):
        for x in range(len(stage[y])):
            baseRect=x*blockWidth,y*blockHeight,blockWidth,blockHeight
            if stage[y][x]==2:
                pg.draw.rect(drawScreen, staticColor, baseRect)
            elif stage[y][x]==1:
                pg.draw.rect(drawScreen, activeColor, baseRect)
                
    #绘制下一个登场的下落方块形状
    printTxt("Next:",320,350,defaultFont,backSurface,fontColor)
    if nextBlock!=None:
        for y in range(len(nextBlock.block)):
            for x in range(len(nextBlock.block[y])):
                baseRect=320+x*blockWidth,380+y*blockHeight,blockWidth,blockHeight
                if nextBlock.block[y][x]==1:
                    pg.draw.rect(drawScreen, activeColor, baseRect)
                
    #绘制关卡、积分、当前关卡消除整行数
    printTxt("Level:%d" % level,320,40,defaultFont,backSurface,fontColor)
    printTxt("Score:%d" % score,320,70,defaultFont,backSurface,fontColor)
    printTxt("Clear:%d" % clearLineScore,320,100,defaultFont,backSurface,fontColor)
    
    #特殊游戏状态的输出
    if gameOver:
        printTxt("GAME OVER",230,200,defaultFont,backSurface,fontColor)   
        printTxt("<PRESS RETURN TO REPLAY>",200,260,defaultFont,backSurface,fontColor)   
    if pause:
        printTxt("Game pausing",230,200,defaultFont,backSurface,fontColor)   
        printTxt("<PRESS RETURN TO CONTINUE>",200,260,defaultFont,backSurface,fontColor)   


def process():
    '''
    游戏控制及逻辑处理
    '''
    global gameOver,nowBlock,nextBlock,speedBuff,backSurface,keyBuff,pause
    
    if nextBlock is None:
        nextBlock=blockSprite(random.randint(0,len(blocks)-1),random.randint(0,3),point(maxBlockWidth+4,maxBlockHeight))
    if nowBlock is None:
        nowBlock=nextBlock.clone()
        nowBlock.xy=point(maxBlockWidth//2,0)
        nextBlock=blockSprite(random.randint(0,len(blocks)-1),random.randint(0,3),point(maxBlockWidth+4,maxBlockHeight))
        #每次生成新的下落方块形状时检测碰撞，如果新的方块形状一出现就发生碰撞，则显然玩家已经没有机会了。
        gameOver=checkDeany(nowBlock)
        #游戏失败后，要将活动方块形状做固实处理
        if gameOver:
            updateStage(nowBlock,2)
            
    '''
    对于下落方块形状操控以及移动，采用影子形状进行预判断。如果没有碰撞则将变化应用到下落方块形状上，否则不变化。
    '''
    tmpBlock=nowBlock.clone()       #影子方块形状
    '''
    处理用户输入
    对于用户输入分为两部分处理。
    第一部分，将退出、暂停、重新开始以及形状变换的操作以敲击事件处理。
    这样做的好处是只对敲击一次键盘做出处理，避免用户按住单一按键后程序反复处理影响操控，特别是形状变换操作，敲击一次键盘换变一次方向，玩家很容易控制。
    '''
    for event in pg.event.get():
        if event.type== pg.QUIT:
            sys.exit()
            pg.quit()
        elif event.type==pg.KEYDOWN:
            if event.key==pg.K_ESCAPE:
                sys.exit()
                pg.quit()
            elif event.key==pg.K_RETURN:
                if gameOver:
                    sysInit()
                    return
                elif pause:
                    pause=False
                else:
                    pause=True
                    return
            elif not gameOver and not pause:
                if event.key==pg.K_SPACE:
                    tmpBlock.chgDirection(1)
                elif event.key==pg.K_UP:
                    tmpBlock.chgDirection(0)
                    
    if not gameOver and not pause:
        '''
        用户输入处理第二部分，将左右移动和快速下落的操作以按下事件处理。
        这样做的好处是不需要玩家反复敲击键盘进行操作，保证了操作的连贯性。
        由于连续移动的速度太快，不利于定位。所以在程序中采用了简单的输入减缓处理，即通过keyBuff保存上一次操作按键，如果此次按键与上一次按键相同，则跳过此轮按键处理。
        '''
        keys=pg.key.get_pressed()
        if keys[K_DOWN]:
            tmpBlock.xy=point(tmpBlock.xy.x,tmpBlock.xy.y+1)
            keyBuff=None
        elif keys[K_LEFT]:
            if keyBuff!=pg.K_LEFT:
                tmpBlock.xy=point(tmpBlock.xy.x-1,tmpBlock.xy.y)
                keyBuff=pg.K_LEFT
            else:
                keyBuff=None
        elif keys[K_RIGHT]:
            if keyBuff!=pg.K_RIGHT:
                tmpBlock.xy=point(tmpBlock.xy.x+1,tmpBlock.xy.y)
                keyBuff=pg.K_RIGHT
            else:
                keyBuff=None
        if not checkDeany(tmpBlock):
            updateStage(nowBlock,0)
            nowBlock=tmpBlock.clone()
        
        #处理自动下落
        speedBuff+=1
        if speedBuff>=fallSpeed:
            speedBuff=0
            tmpBlock=nowBlock.clone()
            tmpBlock.xy=point(nowBlock.xy.x,nowBlock.xy.y+1)
            if not checkDeany(tmpBlock):
                updateStage(nowBlock,0)
                nowBlock=tmpBlock.clone()
                updateStage(nowBlock,1)
            else:
                #在自动下落过程中一但发生活动方块形状的碰撞，则将活动方块形状做固实处理，并检测是否有可消除的整行方块
                updateStage(nowBlock,2)
                checkLine()
                nowBlock=None
        else:
            updateStage(nowBlock,1)
    drawStage(backSurface)
    screen.blit(backSurface,(0,0))
    pg.display.update()
    clock.tick(40)

    
def main():
    '''
    主程序
    '''
    getConf("elsfk.cfg")
    sysInit()
    while True:
        process() 
  
    
if __name__ == "__main__":
    main()