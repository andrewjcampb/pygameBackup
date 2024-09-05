import pygame
from EnemyBullet import EnemyBullet

BLACK = ((0, 0, 0))
SPACE = ((20, 0, 40))
WHITE = ((255, 255, 255))
SHIP_ORANGE = ((200, 120, 0))
YELLOW = ((255, 255, 0))
RED = ((255, 0, 0))
GREEN = ((0, 200, 20))
BLUE = ((0, 0, 255))
PURPLE = ((150, 0, 255))

class Enemy:

    def __init__(self, relative_x, relative_y, rect, type, level):
        self.relative_x = relative_x #Y without oscillation: These don't apply if an enemy is attacking
        self.relative_y = relative_y #X without oscillation
        self.rect = rect
        self.type = type #Color
        self.attackX = -1
        self.attackY = -1
        self.attack = False
        self.targetX = 0
        self.targetY = 0
        self.attackXVel = 0
        self.attackYVel = 0
        if self.type == BLUE:
            self.attackTime = 120 - 5 * level
        elif self.type == GREEN:
            self.attackTime = 60 - 4 * level
        else:
            self.attackTime = 140 - 6 * level
        self.attackSection = 0 #Needed for GREEN
        self.attackDelay = 0 #Needed for GREEN
        self.maxXVel = 10 #For Green and Purple
        self.bulletXVel = 0
        self.hasShot = False #Used for the midRun fire

    #Returns a Rect of the enemy in its default state
    def default_rect(self, x_offset):
        return pygame.Rect(self.relative_x + x_offset, self.relative_y, self.rect.width, self.rect.height)
    
    #Returns a Rect of the enemy, to be used if it is currently attacking
    def attack_rect(self):
        return pygame.Rect(self.attackX, self.attackY, self.rect.width, self.rect.height)

    #Updates Movement of an attacking ship, or causes the enemy to attack
    def handle_attack(self, ship, SHIP_WIDTH, x_offset, HEIGHT, level):
        if self.type == BLUE:
            if self.attack == False:
                self.hasShot = False
                self.targetX = ship.x + (SHIP_WIDTH - self.rect.width) / 2
                self.targetY = ship.y
                self.attackX = self.relative_x + x_offset
                self.attackY = self.relative_y
                self.attack = True
                self.attackXVel = (self.targetX - self.attackX) / self.attackTime
                self.attackYVel = (self.targetY - self.attackY) / self.attackTime
            elif self.attackY >= HEIGHT:
                self.attack = False
            else:
                self.attackX += self.attackXVel
                self.attackY += self.attackYVel
        elif self.type == GREEN:
            if self.attack == False:
                self.hasShot = False
                self.targetX = ship.x + (SHIP_WIDTH - self.rect.width) / 2
                self.targetY = self.relative_y + 300 + level * 10
                self.attackX = self.relative_x + x_offset
                self.attackY = self.relative_y
                self.attack = True
                self.attackXVel = (self.targetX - self.attackX) / self.attackTime
                self.attackYVel = (self.targetY - self.attackY) / self.attackTime
                self.attackSection = 1
            elif self.attackY > self.targetY and self.attackSection == 1:
                self.attackSection = 2
            elif self.attackSection == 2:
                self.attackDelay += 1
                if self.attackDelay > 20:
                    self.targetX = ship.x + (SHIP_WIDTH - self.rect.width) / 2
                    self.targetY = ship.y
                    self.attackXVel = (self.targetX - self.attackX) / self.attackTime
                    self.attackYVel = (self.targetY - self.attackY) / self.attackTime
                    if self.attackXVel > self.maxXVel:
                        self.attackXVel = self.maxXVel
                    elif self.attackXVel < -self.maxXVel:
                        self.attackXVel = -self.maxXVel
                    self.attackSection = 3
            elif self.attackY >= HEIGHT:
                self.attack = False
                self.attackDelay = 0
            else:
                self.attackX += self.attackXVel
                self.attackY += self.attackYVel
        elif self.type == PURPLE:
            if self.attack == False:
                self.hasShot = False
                self.targetX = ship.x + (SHIP_WIDTH - self.rect.width) / 2
                self.targetY = ship.y
                self.attackX = self.relative_x + x_offset
                self.attackY = self.relative_y
                self.attack = True
                self.attackXVel = (self.targetX - self.attackX) / self.attackTime
                self.attackYVel = (self.targetY - self.attackY) / self.attackTime
            elif self.attackY >= HEIGHT:
                self.attack = False
            else:
                self.attackX += self.attackXVel
                self.attackY += self.attackYVel
                self.targetX = ship.x
                if self.attackY < self.targetY - 200:
                    self.attackXVel = (self.targetX - self.attackX) / (((ship.y - self.attackY) / (ship.y - self.relative_y)) * self.attackTime)
                if self.attackXVel > self.maxXVel:
                    self.attackXVel = self.maxXVel
                elif self.attackXVel < -self.maxXVel:
                    self.attackXVel = -self.maxXVel
    

    def call_bullet(self, BULLET_HEIGHT, BULLET_WIDTH, ENEMY_BULLET_VEL, ship, x_offset, level):
        if self.attack == True:
            x = self.attackX
            y = self.attackY
        else:
            x = self.relative_x + x_offset     
            y = self.relative_y
        time = (ship.y - y) / ENEMY_BULLET_VEL
        xVel = (ship.x - x) / time
        
        return EnemyBullet(xVel, x, self.rect.width, y, self.rect.height, BULLET_HEIGHT, BULLET_WIDTH, level)