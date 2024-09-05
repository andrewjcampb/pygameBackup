import pygame
pygame.mixer.init()
pygame.font.init()
from Enemy import Enemy

#Display
WIDTH, HEIGHT = 800, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galagalish")

#Constants
FPS = 60
SHIP_VEL = 10
BULLET_VEL = 13
SHIP_MAX_BULLETS = 2
SHIP_WIDTH, SHIP_HEIGHT = (70, 40)
BULLET_WIDTH, BULLET_HEIGHT = (6, 20)
ENEMY_WIDTH, ENEMY_HEIGHT, ENEMY_ROWS = (50, 30, 4)

#Colors
BLACK = ((0, 0, 0))
SPACE = ((20, 0, 40))
WHITE = ((255, 255, 255))
SHIP_ORANGE = ((200, 120, 0))
YELLOW = ((255, 255, 0))
RED = ((255, 0, 0))
GREEN = ((0, 200, 20))
BLUE = ((0, 0, 255))
PURPLE = ((150, 0, 255))


#Fonts

#Images

#Sounds

#Events




#Moves player ship
def player_handle_movement(keys_pressed, ship): #Ship needs to be a rect
    if keys_pressed[pygame.K_a] and (ship.x - SHIP_VEL) > 0:
        ship.x -= SHIP_VEL
    elif keys_pressed[pygame.K_a]:
        ship.x = 0

    if keys_pressed[pygame.K_d] and (ship.x + SHIP_WIDTH) < WIDTH:
        ship.x += SHIP_VEL
    elif keys_pressed[pygame.K_d]:
        ship.x = WIDTH - SHIP_WIDTH

def player_handle_bullets(player_bullets, enemy_ships, x_offset):
    for bullet in player_bullets:
        bullet.y -= BULLET_VEL
        if (bullet.y + BULLET_HEIGHT < 0):
            player_bullets.remove(bullet)
        else:
            for y in enemy_ships:
                for enemy in y:
                    if enemy.trueRect(x_offset).colliderect(bullet):
                        player_bullets.remove(bullet)
                        y.remove(enemy)
                        break
                        #Add some Event here if I want to keep track of score

def round_start(enemy_ships):
    for y in range(ENEMY_ROWS):
        for x in range(10):
            color = ((0, 0, 0))
            if (y == 0):
                color = PURPLE
            elif (y == 1):
                color = GREEN
            elif (y >= 2):
                color = BLUE
            enemyRect = pygame.Rect((((WIDTH - 200) /10) * x) + 100, 40 * y + 20, ENEMY_WIDTH, ENEMY_HEIGHT)
            enemyStartX = (((WIDTH - 200) /10) * x) + 100
            enemyStartY = 50 * y + 20
            enemy = Enemy(enemyStartX, enemyStartY, enemyRect, color)

            enemy_ships[y - 1].append(enemy)

def handle_oscillation(x_offset, offset_direction):
    if x_offset >= 60:
        offset_direction = -1
    elif x_offset <= -60:
        offset_direction = 1
    
    if offset_direction == 1:
        x_offset += 1
    elif offset_direction == -1:
        x_offset -= 1  

    return x_offset, offset_direction

#Draws Window
def draw_window(ship, player_bullets, enemy_ships, x_offset):
    WIN.fill(SPACE)
    
    pygame.draw.rect(WIN, SHIP_ORANGE, ship)

    for bullet in player_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    for y in enemy_ships:
        for enemy in y:
            pygame.draw.rect(WIN, enemy.type, enemy.trueRect(x_offset))
    pygame.display.update()

def main():
    clock = pygame.time.Clock()

    enemy_ships = [[], [], [], []]
    
    enemy_bullets = []
    enemyMaxBullets = 3

    player_bullets = []

    x_offset = 0 #Used for oscillation of ships
    offset_direction = 1

    ship = pygame.Rect(WIDTH//2 - SHIP_WIDTH//2, HEIGHT - SHIP_HEIGHT - 50, SHIP_WIDTH, SHIP_HEIGHT)

    gameState = 2 #This determines what the game is doing. 1 is gameplay, 2 is title

    round_start(enemy_ships)

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(player_bullets) < SHIP_MAX_BULLETS:
                        bullet = pygame.Rect(ship.x + SHIP_WIDTH//2, ship.y - BULLET_HEIGHT, BULLET_WIDTH, BULLET_HEIGHT) #The // forces int
                        player_bullets.append(bullet)    
        
        keys_pressed = pygame.key.get_pressed()

        player_handle_movement(keys_pressed, ship)
        x_offset, offset_direction = handle_oscillation(x_offset, offset_direction)
        player_handle_bullets(player_bullets, enemy_ships, x_offset)
        draw_window(ship, player_bullets, enemy_ships, x_offset)
        
if __name__ == "__main__":
    main()