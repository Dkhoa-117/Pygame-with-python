import pygame
import math
import random
from pygame import mixer

# Initialize
pygame.init()

# Caption and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ship.png")
pygame.display.set_icon(icon)

# background
background = pygame.image.load("galaxy2.jpg")
mixer.music.load("background.wav")
mixer.music.play(-1)

# create the screen
screen = pygame.display.set_mode((800, 600))

# Score
scoreVal = 0
font = pygame.font.Font("Silkscreen-Regular.ttf", 32)
textX = 10
textY = 10
def showScore(scoreVal, x, y):
    score = font.render("Point: " + str(scoreVal), True, (255,255,255))
    screen.blit(score, (x, y))
gameOverFont = pygame.font.Font("Silkscreen-Regular.ttf", 64)

def gameOverText():
    text = gameOverFont.render("GAME OVER", True, (255,255,255))
    screen.blit(text, (200, 250))

# Player
playerImg = pygame.image.load("space-shuttle.png")
playerMove = 0
playerX = 368
playerY = 450
def player(x, y):
    screen.blit(playerImg, (x, y))

# Bullet
# state ready: not shooted yet, state fire: shooted 
bulletImg = pygame.image.load("bullet.png")
bulletMove = 10
bulletX = 0
bulletY = 450
bulletState = "ready"
def bullet(x,y):
    global bulletState
    bulletState = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

# Enemies
enemyImg = []
enemyX = []
enemyY = []
enemyMoveX = []
enemyMoveY = []
enemyMoveX = []
enemyMoveY = []
numOfEnemies = 6
def enemy(i, x, y):
    screen.blit(enemyImg[i], (x, y))

for i in range(numOfEnemies):
    enemyImg.append(pygame.image.load("monster.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyMoveX.append(1)
    enemyMoveY.append(40)

def isCollision(x1, y1, x2, y2):
    distanceVal = math.sqrt((math.pow(x1 - x2, 2)) + (math.pow(y1 - y2, 2)))
    if distanceVal < 27:
        return True
    else:
        return False

# Mantain the Screen
running = True
while running:
    screen.fill((0,0,50))
    # show the background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        # Quit game
        if event.type == pygame.QUIT:
            running = False
        # Moving Handler
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerMove = 5
            elif event.key == pygame.K_LEFT:
                playerMove = -5
            if event.key == pygame.K_SPACE:
                if bulletState is "ready":
                    bulletSound = mixer.Sound("laser.wav")
                    bulletSound.play()
                    bulletX = playerX
                    bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerMove = 0
    
    playerX += playerMove
    if playerX < 0:
        playerX = 0
    elif playerX > 736:
        playerX = 736
    player(playerX, playerY)

    # Bullet movement
    if bulletY < 0:
        bulletState = "ready"
        bulletY = 450
    if bulletState is "fire":
        bullet(bulletX, bulletY)
        bulletY -= bulletMove

    # Enemies moving X
    for i in range(numOfEnemies):
        if enemyY[i] > 400:
            for j in range(numOfEnemies):
                enemyY[j] = 2000
            gameOverText()
        if enemyX[i] < 0 or enemyX[i] > 736:
            enemyMoveX[i] = -enemyMoveX[i]
            enemyY[i] += enemyMoveY[i]
        enemyX[i] += enemyMoveX[i]
        if isCollision(bulletX, bulletY, enemyX[i], enemyY[i]):
            explosionSound = mixer.Sound("explosion.wav")
            explosionSound.play()
            bulletY = 450
            bulletState = "ready"
            scoreVal+=1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
        enemy(i, enemyX[i], enemyY[i])
    
    showScore(scoreVal, textX, textY)
    # update view
    pygame.display.update()
