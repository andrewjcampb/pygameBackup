import pygame
import random
from Enemy import Enemy
from EnemyBullet import EnemyBullet
pygame.mixer.init()
pygame.font.init()

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
BLACK = (0, 0, 0)
SPACE = (20, 0, 40)
WHITE = (255, 255, 255)
SHIP_ORANGE = (200, 120, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 200, 20)
BLUE = (0, 0, 255)
PURPLE = (150, 0, 255)
TITLE_COLOR = (200, 20, 50)
TITLE_GREEN = (20, 180, 80)

#Fonts
DeathFont = pygame.font.SysFont('gigi', 50)
LevelFont = pygame.font.SysFont('poorrichard', 20)
TitleFont = pygame.font.SysFont('footlight', 90)
BeginFont = pygame.font.SysFont('hightowertext', 40)

#Images
SHIP_SPRITE = pygame.image.load('Sprites\Ship.png')
SHIP_SPRITE = pygame.transform.scale(SHIP_SPRITE, (SHIP_WIDTH, SHIP_HEIGHT))
BLUE_SPRITE = pygame.image.load('Sprites\Blue.png')
BLUE_SPRITE = pygame.transform.scale(BLUE_SPRITE, (ENEMY_WIDTH, ENEMY_HEIGHT))
GREEN_SPRITE = pygame.image.load('Sprites\Green.png')
GREEN_SPRITE = pygame.transform.scale(GREEN_SPRITE, (ENEMY_WIDTH, ENEMY_HEIGHT))
PURPLE_SPRITE = pygame.image.load('Sprites\Purple.png')
PURPLE_SPRITE = pygame.transform.scale(PURPLE_SPRITE, (ENEMY_WIDTH, ENEMY_HEIGHT))
BLAST_SPRITE = pygame.image.load('Sprites\Kaboom.png')
BLAST_SPRITE = pygame.transform.scale(BLAST_SPRITE, (SHIP_WIDTH, SHIP_HEIGHT))

#Sounds
PEW_SOUND = pygame.mixer.Sound('Sounds\LaserSound.wav')
DEATH_SOUND = pygame.mixer.Sound('Sounds\DeathSound.wav')
DEATH_SOUND.set_volume(0.4)
EXPLOSION_SOUND = pygame.mixer.Sound('Sounds\ExplosionSound.wav')
EXPLOSION_SOUND.set_volume(0.6)
STARTSOUND = pygame.mixer.Sound('Sounds\StartupSound.wav')
LEVELWINSOUND = pygame.mixer.Sound('Sounds\LevelWinSound.wav')
LEVELWINSOUND.set_volume(0.5)

#Events
KillPlayer = pygame.USEREVENT + 1
WinEvent = pygame.USEREVENT + 2


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

#Handles movement and colllision of player bullets
def player_handle_bullets(player_bullets, enemy_ships, x_offset):
    for bullet in player_bullets:
        bullet.y -= BULLET_VEL
        if (bullet.y + BULLET_HEIGHT < 0):
            player_bullets.remove(bullet)
        else:
            check = False
            for y in enemy_ships:
                for enemy in y:
                    if enemy.attack == False:
                        if enemy.default_rect(x_offset).colliderect(bullet):
                            player_bullets.remove(bullet)
                            y.remove(enemy)
                            EXPLOSION_SOUND.play()
                            check = True
                            break
                            #Add some Event here if I want to keep track of score
                    elif enemy.attack_rect().colliderect(bullet):
                          player_bullets.remove(bullet)
                          y.remove(enemy)
                          EXPLOSION_SOUND.play()
                          check = True
                          break
                          #A different event can be added here to get bonus points for shooting moving enemy
                if check == True:
                    break

#Handles enemy bullets. 1 of the total Enemy Bullets is reserved for attacking ships, but ships can also randomly attack while attacking
def enemy_handle_bullets(enemy_ships, enemy_bullets, ship, x_offset, bulletTimer, level):
    resetCheck = False #Used to allow bullet to fire again if random check fails
    if (len(enemy_bullets) < (MAX_ENEMY_BULLETS - 1) and bulletTimer <= 0) and (random.randint(0, 100) < 5):
        y = 0
        for row in enemy_ships:
            if len(row) > 0:
                enemy = random.choice(row)
                if not(enemy.attack == True and enemy.attackY > (ship.y - 400)):
                    if (random.randint(1, 5) > 4):
                        enemy_bullets.append(enemy.call_bullet(BULLET_HEIGHT, BULLET_WIDTH, ENEMY_BULLET_VEL, ship, x_offset, level))
                        PEW_SOUND.play()
                    else:
                        resetCheck = True
                break
    if len(enemy_bullets) < MAX_ENEMY_BULLETS:
        for row in enemy_ships:
            for enemy in row:
                if enemy.attack == True and (enemy.attackY > 300 + 20*level) and enemy.hasShot == False and (enemy.attackY < 600) and (random.randint(0, 100) < 20):
                    enemy_bullets.append(enemy.call_bullet(BULLET_HEIGHT, BULLET_WIDTH, ENEMY_BULLET_VEL - 2, ship, x_offset, level))
                    PEW_SOUND.play()
                    enemy.hasShot = True
    for bullet in enemy_bullets:
        bullet.bulletRect.y += ENEMY_BULLET_VEL
        bullet.bulletRect.x += bullet.xVel 
        if (bullet.bulletRect.y > HEIGHT):
            enemy_bullets.remove(bullet)
       
    if resetCheck:
        return 5
    elif (bulletTimer <= 0):
        return BULLET_TIMER
    return bulletTimer - 1

#Handles enemy attacks, makes sure only MAX_ATTACKERS enemies can attack at any time
def call_attacks(enemy_ships, ship, x_offset, attackTimer, level):
    if attackTimer >= ATTACK_TIMER_MAX and random.randint(0, 100) < 5:
        attackTimer = 0
        attackers = 0
        ships = 0
        for y in enemy_ships:
            ships += len(y)
            for enemy in y:
                if enemy.attack == True:
                    attackers += 1
        if attackers < MAX_ATTACKERS:
            while ships > 0:
                x = random.choice(enemy_ships)
                if len(x) != 0:
                    random.choice(x).handle_attack(ship, SHIP_WIDTH, x_offset, HEIGHT, level)
                    break

    attackTimer += 1
    return attackTimer

#Starts A Round by adding enemies
    #This should be where any difficulty changes happen
def round_start(enemy_ships, level):
    global ENEMY_BULLET_VEL
    global MAX_ATTACKERS
    global ATTACK_TIMER_MAX
    global MAX_ENEMY_BULLETS
    global BULLET_TIMER
    ENEMY_BULLET_VEL = 8 + level // 3
    MAX_ATTACKERS = level // 10 + 2
    ATTACK_TIMER_MAX = 100 - 5 * level #Tied to attackTimer, used to know when enemies should attack\
    if (ATTACK_TIMER_MAX < 50):
        ATTACK_TIMER_MAX = 50
    MAX_ENEMY_BULLETS = level // 5 + 2
    BULLET_TIMER = 60 - 4 * level
    if BULLET_TIMER < 20:
        BULLET_TIMER = 20
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
            enemy = Enemy(enemyStartX, enemyStartY, enemyRect, color, level)

            enemy_ships[y - 1].append(enemy)
    return level + 1

#Handles the oscillating motion of the enemies when not attacking
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

def check_winner(enemy_ships):
    check = False
    for y in  enemy_ships:
        if len(y) > 0:
            check = True
    if check == False:
        pygame.event.post(pygame.event.Event(WinEvent))


#Draws Window
def draw_window(ship, player_bullets, enemy_ships, x_offset, enemy_bullets, level):
    global BLUE
    global GREEN
    global PURPLE
    
    WIN.fill(SPACE)
    
    #pygame.draw.rect(WIN, SHIP_ORANGE, ship)
    WIN.blit(SHIP_SPRITE, (ship.x, ship.y))

    for bullet in player_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    for enemyBullet in enemy_bullets:
        pygame.draw.rect(WIN, RED, enemyBullet.bulletRect)
        if (enemyBullet.bulletRect.colliderect(ship)):
            pygame.event.post(pygame.event.Event(KillPlayer))


    for y in enemy_ships:
        for enemy in y:
            sprite = 0
            if enemy.type == BLUE:
                sprite = BLUE_SPRITE
            elif enemy.type == GREEN:
                sprite = GREEN_SPRITE
            elif enemy.type == PURPLE:
                sprite = PURPLE_SPRITE
            
            if enemy.attack == True:
                WIN.blit(sprite, (enemy.attackX, enemy.attackY))
                enemy.handle_attack(ship, SHIP_WIDTH, x_offset, HEIGHT, level)
                if (enemy.attack_rect().colliderect(ship)):
                    pygame.event.post(pygame.event.Event(KillPlayer))
            else: 
                WIN.blit(sprite, (enemy.relative_x + x_offset, enemy.relative_y))

    draw_text = LevelFont.render(f'Level: {level}', 1, WHITE)
    WIN.blit(draw_text, ((9/10) * WIDTH - draw_text.get_width() / 2, (19/20) * HEIGHT - draw_text.get_height()/2))

    pygame.display.update()

def draw_title():
    WIN.fill(SPACE)
    title = TitleFont.render('GALAGALISH', 1, TITLE_COLOR)
    WIN.blit(title, (WIDTH/2 - title.get_width() / 2, HEIGHT/7 - title.get_height()/2))
    begin = BeginFont.render('Please Press Enter to Begin', 1, TITLE_GREEN)
    WIN.blit(begin, (WIDTH/2 - begin.get_width() / 2, HEIGHT/2 + HEIGHT/3 - begin.get_height()/2))
    pygame.display.update()

def draw_paused():
    WIN.fill(SPACE)
    pause = TitleFont.render('Paused', 1, TITLE_COLOR)
    WIN.blit(pause, (WIDTH/2 - pause.get_width() / 2, HEIGHT/3 - pause.get_height()/2))
    begin = BeginFont.render('Please Press Enter to Begin', 1, TITLE_GREEN)
    WIN.blit(begin, (WIDTH/2 - begin.get_width() / 2, HEIGHT/2 + HEIGHT/4 - begin.get_height()/2))
    exit = BeginFont.render('Press ESC to Return to Menu', 1, RED)
    WIN.blit(exit, (WIDTH/2 - exit.get_width() / 2, HEIGHT/2 + HEIGHT/3 + HEIGHT/16 - exit.get_height()/2))
    pygame.display.update()

#Main Gameplay loop
def main():
    clock = pygame.time.Clock()

    enemy_ships = [[], [], [], []]
    
    enemy_bullets = []
    bulletTimer = 60

    player_bullets = []

    x_offset = 0 #Used for oscillation of ships
    offset_direction = 1

    ship = pygame.Rect(WIDTH//2 - SHIP_WIDTH//2, HEIGHT - SHIP_HEIGHT - 50, SHIP_WIDTH, SHIP_HEIGHT)

    gameState = 2 #This determines what the game is doing. 1 is gameplay, 2 is title
    level = 0

    attackTimer = 0 #Used to know when to send the next enemy attack

    level = round_start(enemy_ships, level)

    run = True
    playerDead = 0

    while run:
        clock.tick(FPS)
        if gameState == 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and len(player_bullets) < SHIP_MAX_BULLETS:
                        bullet = pygame.Rect(ship.x + SHIP_WIDTH//2, ship.y - BULLET_HEIGHT, BULLET_WIDTH, BULLET_HEIGHT) #The // forces int
                        player_bullets.append(bullet)
                        PEW_SOUND.play()
                

                if event.type == KillPlayer:
                    run = False
                    playerDead = 2
                if event.type == WinEvent:
                    LEVELWINSOUND.play()
                    draw_text = DeathFont.render(f'On To Level {level + 1}', 1, WHITE)
                    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() / 2, HEIGHT/2 - draw_text.get_height()/2))
                    pygame.display.update()
                    pygame.time.delay(1000)
                    enemy_ships = [[], [], [], []]
                    enemy_bullets = []
                    player_bullets = []
                    level = round_start(enemy_ships, level)
        
            keys_pressed = pygame.key.get_pressed()

            player_handle_movement(keys_pressed, ship)
            attackTimer = call_attacks(enemy_ships, ship, x_offset, attackTimer, level)
            x_offset, offset_direction = handle_oscillation(x_offset, offset_direction)
            player_handle_bullets(player_bullets, enemy_ships, x_offset)
            bulletTimer = enemy_handle_bullets(enemy_ships, enemy_bullets, ship, x_offset, bulletTimer, level)
            draw_window(ship, player_bullets, enemy_ships, x_offset, enemy_bullets, level)
            check_winner(enemy_ships)

            if keys_pressed[pygame.K_p]:
                gameState = 3
                
        elif gameState == 2:
            draw_title()
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_RETURN]:
                gameState = 1
                STARTSOUND.play()
                pygame.time.delay(1000)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
        
        elif gameState == 3:
            draw_paused()
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_RETURN]:
                gameState = 1
            if keys_pressed[pygame.K_ESCAPE]:
                gameState = 1
                playerDead = 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
        
        if playerDead == 2:
            DEATH_SOUND.play()
            WIN.blit(BLAST_SPRITE, (ship.x, ship.y))
            draw_text = DeathFont.render('Game Over Yeah!', 1, WHITE)
            WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() / 2, HEIGHT/2 - draw_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)
            gameState = 2
            enemy_ships = [[], [], [], []]
            enemy_bullets = []
            bulletTimer = 60
            player_bullets = []
            x_offset = 0
            offset_direction = 1
            ship = pygame.Rect(WIDTH//2 - SHIP_WIDTH//2, HEIGHT - SHIP_HEIGHT - 50, SHIP_WIDTH, SHIP_HEIGHT)
            level = 0
            attackTimer = 0
            level = round_start(enemy_ships, level)
            run = True
            playerDead = 0
        if playerDead == 1:
            playerDead = 2 #Delays playerDead from activating until after the screen is drawn again
       
if __name__ == "__main__":
    main()