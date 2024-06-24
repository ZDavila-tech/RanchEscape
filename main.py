import pygame
from pygame import mixer
from pygame.locals import *
import time
import random
from playsound import playsound


pygame.font.init()
game = True
#Setting up Window
WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Steer RoundUp!")

#background music
BG = pygame.transform.scale(pygame.image.load("background.jpg"), (WIDTH, HEIGHT))
mixer.init()
mixer.music.load("music.mp3")
mixer.music.set_volume(0.7)

#sound effects
horse_neigh = "horseneigh.wav"
cow_moo = "cowmoo.wav"

#Player Stats
PLAYER_WIDTH = 100
PLAYER_HEIGHT = 80
PLAYER_VEL = 5
PLAYER_ICON = pygame.transform.scale(pygame.image.load("player.png"), (PLAYER_WIDTH, PLAYER_HEIGHT))

#Enemy Stats
STEER_WIDTH = 20
STEER_HEIGHT = 20
STEER_VEL = 4
STEER_NUM = 3

#Fonts
FONT = pygame.font.SysFont("comicsans", 30)

#Draw Function
def draw(player, elasped_time, steers):
    WIN.blit(BG, (0,0))

    time_text = FONT.render(f"Time: {round(elasped_time)}s", 1, (255,255,255))
    WIN.blit(time_text, (10,10))

    WIN.blit(PLAYER_ICON, (player.x, player.y))

    for steer in steers:
        pygame.draw.rect(WIN, (255,255,255), steer)

    pygame.display.update()


#main gameplay
def main():
    run = True
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT - 10, PLAYER_WIDTH, PLAYER_HEIGHT)
    PLAYER_LIVES = 3
    clock = pygame.time.Clock()
    start_time = time.time()
    elasped_time = 0

    steer_add_increment = 2000
    steer_count = 0 
    steers = []

    hit = False
    mixer.music.play()
    while run:
        steer_count += clock.tick(60)
        elasped_time = time.time() - start_time

        if elasped_time % 40 == 0:
            steer_add_increment -= 200
        if elasped_time % 20 == 0:
            STEER_NUM += 1

        if steer_count > steer_add_increment:
            for _ in range(STEER_NUM):
                steer_x = random.randint(0, WIDTH - STEER_WIDTH)
                steer = pygame.Rect(steer_x, -STEER_HEIGHT, STEER_WIDTH, STEER_HEIGHT)
                steers.append(steer)

            steer_add_increment = max(200, steer_add_increment - 50)
            steer_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL  

        for steer in steers[:]:
            steer.y += STEER_VEL  
            if steer.y > HEIGHT:
                steers.remove(steer)
            elif steer.y + steer.height >= player.y and steer.colliderect(player):
                steers.remove(steer)
                hit = True
                break    
        
        if hit:
            PLAYER_LIVES -= 1
            if PLAYER_LIVES <= 0 :
                lost_text = FONT.render(f"You Lost! High Score {round(elasped_time)}", 1, (255,255,255))
                WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
                pygame.display.update()
                mixer.music.stop()
                playsound(horse_neigh, block=False)
                pygame.time.delay(3000)
                break;
            else:
                playsound(cow_moo, block=False)
            hit = False

        draw(player, elasped_time, steers)    


if __name__ == "__main__":
    while game:
        main()
        pygame.event.clear()
        while True:
            restart_text = FONT.render("Press R to Restart or Q to Quit", 1, (255,255,255))
            WIN.blit(restart_text, (WIDTH/2 - restart_text.get_width()/2, HEIGHT/2 - restart_text.get_height()/2 + 50))
            pygame.display.update()
            event = pygame.event.wait()
            if event.type == KEYDOWN:
                if event.key == K_r:
                    break
                elif event.key == K_q:
                    game = False
                    pygame.quit()
                    
