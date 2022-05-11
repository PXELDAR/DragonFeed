#============================================================================================

import pygame, random
pygame.init()

#============================================================================================

# Variables #

# Display Surface
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 400
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Dragon Feed")

# Clock
FPS = 60
clock = pygame.time.Clock() # Similar to fixed time

# In Game
PLAYER_STARING_LIFE = 5
PLAYER_VELOCITY = 10
COIN_STARTING_VELOCITY = 10
COIN_ACCELERATION = 0.5
BUFFER_DISTANCE = 100 

score = 0
player_life = PLAYER_STARING_LIFE
coin_velocity = COIN_STARTING_VELOCITY

# Colors
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Texts
font = pygame.font.Font("assets/AttackGraffiti.ttf", 20)

score_text = font.render("Score: " + str(score), True, GREEN, BLACK)
score_rect = score_text.get_rect()
score_rect.topleft = (10, 10)

title_text  = font.render("Dragon Feed", True, GREEN, BLACK)
title_rect = title_text.get_rect()
title_rect.centerx = WINDOW_WIDTH / 2
title_rect.y = 10

life_text = font.render("Lives: " + str(player_life), True, GREEN, BLACK)
life_rect = life_text.get_rect()
life_rect.topright = (WINDOW_WIDTH - 10, 10)

game_over_text = font.render("Game Over", True, GREEN, BLACK)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)

continue_text = font.render("Press any key to play again", True, GREEN, BLACK)
continue_rect = continue_text.get_rect()
continue_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 32)

# Sounds
coin_sound = pygame.mixer.Sound("assets/coin.wav")
miss_sound = pygame.mixer.Sound("assets/miss.wav")
miss_sound.set_volume(0.1)
pygame.mixer.music.load("assets/music.wav")
pygame.mixer.music.play(-1, 0.0)

# Images
player_image = pygame.image.load("assets/dragon.png")
player_rect = player_image.get_rect()
player_rect.left = 32
player_rect.centery = WINDOW_HEIGHT / 2

coin_image = pygame.image.load("assets/coin.png")
coin_rect = coin_image.get_rect()
coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
coin_rect.y = random.randint(64, WINDOW_HEIGHT - 32) # Subtract the actual pixel size to fit in screen

#============================================================================================

# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Check Input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] or keys[pygame.K_w] and player_rect.top > 0:
        player_rect.y -= PLAYER_VELOCITY
    if keys[pygame.K_DOWN] or keys[pygame.K_s] and player_rect.bottom < WINDOW_HEIGHT:
        player_rect.y += PLAYER_VELOCITY

    # Check Coin Miss State
    if coin_rect.x < 0:
        player_life -= 1
        miss_sound.play()
        coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
        coin_rect.y = random.randint(64, WINDOW_HEIGHT - 32) # Subtract the actual pixel size to fit in screen
        coin_velocity -= COIN_ACCELERATION
    else:
        coin_rect.x -= coin_velocity

    # Update Hud
    score_text = font.render("Score: " + str(score), True, GREEN, BLACK)
    life_text = font.render("Lives: " + str(player_life), True, GREEN, BLACK)

    # Check Game Over
    if player_life == 0:
        display_surface.blit(game_over_text, game_over_rect)
        display_surface.blit(continue_text, continue_rect)
        pygame.display.update()
        
        # Pause Game
        pygame.mixer.music.stop()
        is_paused = True
        
        # Check Input        
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN: # Restart Game
                    score = 0
                    player_life = PLAYER_STARING_LIFE
                    player_rect.y = WINDOW_HEIGHT / 2
                    coin_velocity = COIN_STARTING_VELOCITY
                    pygame.mixer.music.play(-1, 0.0)
                    is_paused = False
                    
                if event.type == pygame.QUIT: # Quit Game
                    is_paused = False
                    running = False

    # Check Collision
    if player_rect.colliderect(coin_rect):
        score += 1
        coin_sound.play()
        coin_velocity += COIN_ACCELERATION
        coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
        coin_rect.y = random.randint(64, WINDOW_HEIGHT - 32)
            
    # Fill Display
    display_surface.fill(BLACK)

    # Blit HUD
    display_surface.blit(score_text, score_rect)
    display_surface.blit(title_text, title_rect)
    display_surface.blit(life_text, life_rect)

    # Blit Assets
    display_surface.blit(player_image, player_rect)
    display_surface.blit(coin_image, coin_rect)

    # Update
    pygame.display.update()
    clock.tick(FPS)
            
pygame.quit()