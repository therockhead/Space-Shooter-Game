import math
import pygame
import random
from pygame import mixer
import sys

# Initialize Pygame
pygame.init()

# Screen setup
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Background
bg = pygame.image.load('final-bg.png')

# Background music
mixer.music.load('space-bg.wav')
mixer.music.play(-1)

# Game title and icon
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
bullets_img = pygame.image.load('bullets.png')
bulletsX = 0
bulletsY = 480
bulletsX_change = 2
bulletsY_change = 10
bullets_state = "ready"

# Score
score_value = 0
font = pygame.font.SysFont('verdana', 18)
textX = 10
textY = 10

# Game over
game_over_font = pygame.font.Font('freesansbold.ttf', 64)

# Functions
def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (250, 255, 0))
    screen.blit(score, (x, y))

def game_over_text():
    text = game_over_font.render("GAME OVER", True, (250, 255, 0))
    screen.blit(text, (200, 250))

def player(x, y):
    screen.blit(player_img, (x, y))

def invader(x, y, i):
    screen.blit(invader_img[i], (x, y))

def fire_bullets(x, y):
    global bullets_state
    bullets_state = "fire"
    screen.blit(bullets_img, (x + 16, y + 10))

def collision_checker(invaderX, invaderY, bulletsX, bulletsY):
    distance = math.sqrt((math.pow(invaderX - bulletsX, 2)) + (math.pow(invaderY - bulletsY, 2)))
    return distance < 27

def draw_restart_button():
    button_width, button_height = 200, 50
    button_x = (screen_width - button_width) // 2
    button_y = 350
    pygame.draw.rect(screen, (255, 0, 0), (button_x, button_y, button_width, button_height))
    text = font.render("Restart", True, (255, 255, 255))
    text_rect = text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
    screen.blit(text, text_rect)
    return button_x, button_y, button_width, button_height

def reset_game():
    global playerX, playerY, playerX_change, bulletsX, bulletsY, bullets_state, score_value, invaderX, invaderY
    playerX = 370
    playerY = 480
    playerX_change = 0
    bulletsX = 0
    bulletsY = 480
    bullets_state = "ready"
    score_value = 0
    for i in range(num_of_invaders):
        invaderX[i] = random.randint(10, 726)
        invaderY[i] = random.randint(50, 300)

# Main game loop
run = True
game_over = False

while run:
    screen.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE and bullets_state == "ready":
                bullets_sound = mixer.Sound('bullets_firing_sound.wav')
                bullets_sound.play()
                bulletsX = playerX
                fire_bullets(bulletsX, bulletsY)

        if event.type == pygame.KEYUP and not game_over:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

        if event.type == pygame.MOUSEBUTTONDOWN and game_over:
            mouse_pos = event.pos
            button_x, button_y, button_width, button_height = draw_restart_button()
            if button_x <= mouse_pos[0] <= button_x + button_width and button_y <= mouse_pos[1] <= button_y + button_height:
                reset_game()
                game_over = False

    if not game_over:
        playerX += playerX_change
        playerX = max(10, min(playerX, 726))

        for i in range(num_of_invaders):
            if invaderY[i] > 440:
                game_over = True
                break

            invaderX[i] += invaderX_change[i]
            if invaderX[i] <= 10:
                invaderX_change[i] = 2
                invaderY[i] += invaderY_change[i]
            elif invaderX[i] >= 726:
                invaderX_change[i] = -2
                invaderY[i] += invaderY_change[i]

            collision = collision_checker(invaderX[i], invaderY[i], bulletsX, bulletsY)
            if collision:
                collision_sound = mixer.Sound('explosion.wav')
                collision_sound.play()
                bulletsY = 480
                bullets_state = "ready"
                score_value += 1
                invaderX[i] = random.randint(10, 726)
                invaderY[i] = random.randint(50, 300)

            invader(invaderX[i], invaderY[i], i)

        if bulletsY <= 0:
            bulletsY = 480
            bullets_state = "ready"

        if bullets_state == "fire":
            fire_bullets(bulletsX, bulletsY)
            bulletsY -= bulletsY_change

        player(playerX, playerY)
        show_score(textX, textY)
    else:
        game_over_text()
        button_x, button_y, button_width, button_height = draw_restart_button()

    pygame.display.update()
