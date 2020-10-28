import pygame
import sys
from pygame.locals import *
import myclass

 
# Initialize pygame and create window
pygame.init()
screen_size = width, height = 480, 700
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Airspace Alert')

# Load the background image 
bg = pygame.image.load('./images/1.jpg').convert()

# Load the background music
pygame.mixer.music.load('./sound/game_music.ogg')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)                            # set -1 to play music infinitely

# Create medium enemy planes
def add_mid_enemies(group1, group2, num):
    for mid_enemy_num in range(num):                   # num means the number of enemy plane
        each_mid_enemy = myclass.MidEnemy(screen_size)
        group1.add(each_mid_enemy)
        group2.add(each_mid_enemy)

# Create small enemy planes
def add_small_enemies(group1, group2, num):
    for small_enemy_num in range(num):
        each_small_enemy = myclass.SmallEnemy(screen_size)
        group1.add(each_small_enemy)
        group2.add(each_small_enemy)
 
 
def main():
    clock = pygame.time.Clock()                        # Create a Clock to control the frame rate
 
    heroPlane = myclass.myPlane(screen, screen_size)
 
    enemies = pygame.sprite.Group()                    # Create a container class to hold and manage all enemies
   
 
    mid_enemies = pygame.sprite.Group()
    add_mid_enemies(mid_enemies, enemies, 4)
 
    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies, enemies, 15)

    # Bullet
    bullet1 = []
    bullet1_index = 0                                  # Python uses zero-based indexing                   
    BULLET1_NUM = 5
    for i in range(BULLET1_NUM):
        bullet1.append(myclass.Bullet(heroPlane.rect.midtop, True))
 
    small_destroy_index = 0                          
    mid_destroy_index = 0
    big_destroy_index = 0
    hero_destroy_index = 0

    # Life of the heroPlane
    life_image = pygame.image.load("images/life.png").convert_alpha()          # Load the life image
    life_rect = life_image.get_rect()
    life_NUM = 3                                                               # Set heroPlane has 3 lives

    # Score
    score = 0
    score_font = pygame.font.Font("font/font.ttf", 30)                          # Load the font and its size
    WhiteFont = (255, 255, 255)
    gameover_font = pygame.font.Font("font/font.ttf", 48)
    restart_image = pygame.image.load("images/restart.png").convert_alpha()     # Load the restar image
    gameover_image = pygame.image.load("images/quit.png").convert_alpha()
 
    # Game Loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
 
        key_pressed = pygame.key.get_pressed()              # Press the key to move the heroPlane
        if key_pressed[K_UP]:
            heroPlane.moveUp()
        if key_pressed[K_DOWN]:
            heroPlane.moveDown()
        if key_pressed[K_LEFT]:
            heroPlane.moveLeft()
        if key_pressed[K_RIGHT]:
            heroPlane.moveRight()
 
        screen.blit(bg, (0, 0))                            # Draw the background image on display             
        heroPlane.time_delay()

        if life_NUM > 0:

            # Draw medium enemy planes
            for each in mid_enemies:
                if each.active == True:
                    each.move()
                    screen.blit(each.image, each.rect)     # Draw the enemy planes on the display
                else:
                    if not (heroPlane.delay % 3):          # A little bit delay when replace the image
                        screen.blit(each.destroy_images[mid_destroy_index], each.rect)       # Draw the image of plane get destoryed
                        mid_destroy_index = (mid_destroy_index + 1) % 4                      # There are 4 images to show how enemy plane get destoryed 
                        if mid_destroy_index == 0:                                           # If it is the last image
                            each.play_sound()                                                # Play the sound effect
                            score += 200                                                     # Get 200 points
                            each.reset()                                                     # Rebrith the plane                                          

            # Draw small enemy plane
            for each in small_enemies:
                if each.active == True:
                    each.move()
                    screen.blit(each.image, each.rect)
                else:
                    if not (heroPlane.delay % 3):
                        screen.blit(each.destroy_images[small_destroy_index], each.rect)
                        small_destroy_index = (small_destroy_index + 1) % 4
                        if small_destroy_index == 0:
                            each.play_sound()
                            score += 100
                            each.reset()

            # Determine what would happen when heroPlane get destroyed
            if heroPlane.active == True:                 
                heroPlane.animation()
            else:
                if not (heroPlane.delay % 3):
                    screen.blit(heroPlane.destroy_images[hero_destroy_index], heroPlane.rect)   # Draw the image of heroPlane get destroyed
                    hero_destroy_index = (hero_destroy_index + 1) % 4                           # There are 4 images to show how heroPlane get destroyrd
                    if hero_destroy_index == 0:         # If it is the last image
                        life_NUM -= 1                   # lives -1
                        heroPlane.play_sound()          
                        heroPlane.reset()               # Rebrith the hero
 
            if life_NUM > 0:
                for i in range(life_NUM):
                    screen.blit(life_image, (width - 10 - (i + 1) * life_rect.width, height - 10 - life_rect.height))   
 
            if not (heroPlane.delay % 10):
                bullet1[bullet1_index].reset(heroPlane.rect.midtop)
                bullet1_index = (bullet1_index + 1) % BULLET1_NUM


            # Draw bullet
            for each in bullet1:
                if each.active == True:
                    each.move()
                    screen.blit(each.image, each.rect)      # Draw the bullet
                    enemies_hit = pygame.sprite.spritecollide(each, enemies, False,pygame.sprite.collide_mask)
                    if enemies_hit:
                        each.active = False
                        for e in enemies_hit:           
                            if e in mid_enemies:             # If the bullet hit the medium enemy plane
                                e.energy -= 1
                                if e.energy == 0:            # If no energy, medium enemy plane get destoryed
                                    e.active = False
                            else:
                                e.active = False     
                else:
                    each.reset(heroPlane.rect.midtop)        # The bullet update on the midtop of heroPlane
 
            enemies_collided = pygame.sprite.spritecollide(heroPlane, enemies, False, pygame.sprite.collide_mask)

 
            # Check to see if the heroPlane collides with the enemies
            if enemies_collided:                             # if the heroPlane collides with enemies, it will be destoryed
                heroPlane.active = False                     # Undate the state of heroPlane
                for each in enemies_collided:
                    each.active = False
 
            score_surface = score_font.render("Score : %s" % str(score), True, WhiteFont)
            screen.blit(score_surface, (10, 5))
        else:
            pygame.mixer.music.stop()

 
            # Gameover page setting
            gameover_score = gameover_font.render("Score : %s" % str(score), True, WhiteFont)
            screen.blit(gameover_score,(100,200))        # Draw the score on (100,200)
            screen.blit(restart_image, (90,350))
            screen.blit(gameover_image, (90,450))


            # Mouse press
            mouse_down = pygame.mouse.get_pressed()     
            if mouse_down[0]:
                pos = pygame.mouse.get_pos()
                if 90 < pos[0] < 390 and 350 < pos[1] < 390:      # If the mouse click on the position of 'restart' 
                    main()
                elif 90 < pos[0] < 390 and 450 < pos[1] < 490:
                    pygame.quit()
                    sys.exit()
 
        pygame.display.flip()          # Update the game display
        clock.tick(60)                 # 60 frames update per second
 
if __name__ == '__main__':
    main()
