import math
import pygame
import random
from pygame import mixer


# just initial korte arki (Just to initialize pygame)
pygame.init()

screen_width = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))

# background
bg = pygame.image.load('final-bg.png')

# background Music
mixer.music.load('space-bg.wav')
mixer.music.play(-1)

#  score = 0

pygame.display.set_caption("Alien Invader Mu-Ha-Ha")
icon = pygame.image.load('space-ship.png')
pygame.display.set_icon(icon)

# Player 
player_img = pygame.image.load('main ship icon.png')
playerX = 370
playerY = 480
playerX_change = 0

# Invaders
invader_img = []
invaderX = []
invaderY = []
invaderX_change = []
invaderY_change = []
num_of_invaders = 10

for i in range(num_of_invaders):
    invader_img.append(pygame.image.load('alien-on-ufo.png'))
    invaderX.append(random.randint(10, 726))
    invaderY.append(random.randint(50, 300))
    invaderX_change.append(2) 
    invaderY_change.append(40)
# Bullets
# status- ready- invisible
# status- fire - visible firing 
bullets_img = pygame.image.load('bullets.png')
bulletsX = 0
bulletsY = 480
bulletsX_change = 2
bulletsY_change = 10
bullets_state = "ready" 

# score 
score_value = 0
# font = pygame.font.Font('Debrosee-ALPnL.ttf', 20)
font = pygame.font.SysFont('verdana', 18)
textX = 10
textY = 10

# Game Over
# game_over_font = pygame.font.SysFont('verdana', 100)
game_over_font = pygame.font.Font('freesansbold.ttf', 64)

# functions I used
def show_score(x, y):
    score = font.render("Score : "+str(score_value), True, (250,255,0))
    screen.blit(score, (x, y))

def game_over_text():
    text = game_over_font.render("GAME OVER", True, (250,255,0))
    screen.blit(text, (200, 250))

def player(x, y):
    screen.blit(player_img, (x,y))

def invader(x, y, i):
    screen.blit(invader_img[i], (x, y))

def fire_bullets(x, y):
    global bullets_state
    bullets_state = "fire"
    screen.blit(bullets_img, (x + 16, y + 10)) # firing from the top of the shooter

def collision_checker(invaderX, invaderY, bulletsX, bulletsY):
    distance = math.sqrt((math.pow(invaderX-bulletsX,2)) + (math.pow(invaderY-bulletsY, 2)))
    if distance < 27:
        return True
    else:
        return False
    
run = True
# loop
while run:
    
    # screen.fill((41, 36, 66)) # RGB
    #bg-image
    screen.blit(bg, (0,0))

    # playerX += 0.1
    # print(playerX)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                # print("Left arrow is pressed")
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                # print("Left arrow is pressed")
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullets_state == "ready":
                    bullets_sound = mixer.Sound('bullets_firing_sound.wav')
                    bullets_sound.play()
                    bulletsX = playerX
                    fire_bullets(bulletsX, bulletsY)
    
        if event.type == pygame.KEYUP: 
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                # print("Keystoke has been released")
                playerX_change = 0.5
    
    # player Movement
    playerX += playerX_change

    if playerX <= 10: # boundary set for player
        playerX = 10
    elif playerX >= 726:
        playerX = 726

    # invader movement
    for i in range(num_of_invaders):

        # Game Over
        if invaderY[i] > 440:
            for j in range(num_of_invaders):
                invaderY[j] = 2000
                
            game_over_text()
            break

        invaderX[i] += invaderX_change[i]
        if invaderX[i] <= 10: # boundary set for enemy
            invaderX_change[i] = 2
            invaderY[i] += invaderY_change[i]
        elif invaderX[i] >= 726:
            invaderX_change[i] = -2
            invaderY[i] += invaderY_change[i]
        
        # collision check
        collision = collision_checker(invaderX[i], invaderY[i], bulletsX, bulletsY)

        if collision:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            bulletsY = 480
            bullets_state = "ready"
            score_value += 1
            # print(score)
            invaderX[i] = random.randint(10, 726)
            invaderY[i] = random.randint(50, 300)
        
        invader(invaderX[i], invaderY[i], i)
    
    # Bullet Movement
    if bulletsY <= 0:
        bulletsY = 480
        bullets_state = "ready"

    if bullets_state == "fire":
        fire_bullets(bulletsX, bulletsY)
        bulletsY -= bulletsY_change 


    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()

# game_over_sound = mixer.Sound('game-over-sound.wav')
# game_over_sound.play()
    


