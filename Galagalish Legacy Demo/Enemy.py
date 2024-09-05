import pygame
class Enemy:

    def __init__(self, relative_x, relative_y, rect, type):
        self.relative_x = relative_x #Y without oscillation: These don't apply if an enemy is attacking
        self.relative_y = relative_y #X without oscillation
        self.rect = rect
        self.type = type #Color

    def trueRect(self, x_offset):
        return pygame.Rect(self.relative_x + x_offset, self.relative_y, self.rect.width, self.rect.height)
    
    def trueX(self, x_offset):
        return self.relative_x + x_offset
    
    
