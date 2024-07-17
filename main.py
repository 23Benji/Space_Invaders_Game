import pygame
import random
import math
from pygame import mixer

# initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load("res/images/space.png")

# background Music
mixer.music.load('res/sounds/background.wav')
mixer.music.play(-1)  # -1 == looping

# title and icon ... icons= 32 pixel
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("res/images/ufo.png")
pygame.display.set_icon(icon)

#pause
ispaused = False

# player...player = 64 pixel
playerImg = pygame.image.load("res/images/player2.png")
playerX = 370
playerY = 480
playerX_change = 0

# enemy...enemy = 64 pixel
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 7

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("res/images/enemy.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.2)
    enemyY_change.append(15)

# bullet...bullet = 32 pixel
bulletImg = pygame.image.load("res/images/bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 25)

textX = 10
textY = 10

# game over text
over_font = pygame.font.Font('freesansbold.ttf', 64)
score_font = pygame.font.Font('freesansbold.ttf', 32)
pause_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render(str(score_value) + "x", True, (255, 255, 255))
    screen.blit(score, (x, y))
    screen.blit(pygame.image.load("res/images/enemy32.png"), (x + 47, y - 2))

def pause_screen():

    # Create a semi-transparent overlay
    overlay = pygame.Surface((800, 600))
    overlay.set_alpha(128)  # Set transparency level (0-255)
    overlay.fill((0, 0, 0))  # Fill with black color
    screen.blit(overlay, (0, 0))

    pause_text = pause_font.render("Paused", True, (255, 255, 255))
    screen.blit(pause_text, (290, 250))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
    score_text = score_font.render(f"Score: {score_value}", True, (255, 255, 255))
    screen.blit(score_text, (350, 325))



def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        False


# Game Loop
running = True
while running:
    # screen.fill((0, 250, 152))
    screen.fill((0, 0, 0))
    # background image
    screen.blit(background, (0, 0))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key ==pygame.K_ESCAPE:
                ispaused = not ispaused
            if event.key == pygame.K_a:
                playerX_change = -0.2
            if event.key == pygame.K_d:
                playerX_change = 0.2
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bullet_sound = mixer.Sound('res/sounds/laser.wav')
                bullet_sound.play()
                bulletX = playerX
                fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            playerX_change = 0


    if ispaused:
        pause_screen()
        pygame.display.update()
        continue

    playerX += playerX_change

    if playerX < 0:
        playerX = 0
    elif playerX > 736:
        playerX = 736

    # enemy movement
    for i in range(num_of_enemies):

        # Game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] < 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] > 736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('res/sounds/explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # bulleet moovment
    if bulletY < 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
