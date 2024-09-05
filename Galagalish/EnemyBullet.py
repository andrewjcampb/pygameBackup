import pygame

#Helps create a rect for enemy bullets and stores their xVel
class EnemyBullet:
    def __init__(self, xVel, xStart, xWidth, yStart, yHeight, BULLET_HEIGHT, BULLET_WIDTH, level):
        if (xVel > 8 + level // 5):
            xVel = 8 + level // 5
        elif (xVel < -(8 + level // 5)):
            xVel = -(8 + level // 5)
        self.xVel = xVel
        self.xStart = xStart 
        self.xWidth = xWidth
        self.ystart = yStart
        self.yHeight = yHeight
        self.bulletRect = pygame.Rect(xStart + xWidth//2, yStart + yHeight, BULLET_WIDTH, BULLET_HEIGHT)