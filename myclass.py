import pygame
from random import *

# Small enemy plane
class SmallEnemy(pygame.sprite.Sprite):           # Create a sprite
    def __init__(self, screen_size):
        pygame.sprite.Sprite.__init__(self)       # Initialize the sprite

        self.image = pygame.image.load("images/2.png").convert_alpha()         # Load the small enemy image
        self.destroy_images = []                
        self.destroy_images.extend([
            pygame.image.load("./images/enemy1_down1.png").convert_alpha(),    # Load the image of small enemy plane get destroyed and down
            pygame.image.load("./images/enemy1_down2.png").convert_alpha(),
            pygame.image.load("./images/enemy1_down3.png").convert_alpha(),
            pygame.image.load("./images/enemy1_down4.png").convert_alpha()])
        self.rect = self.image.get_rect()
        self.width, self.height = screen_size[0], screen_size[1]
        self.speed = 2                                          # Speed of the plane
        self.active = True
        self.rect.left, self.rect.top = randint(0, self.width - self.rect.width),\
                                        randint(-5*self.height,0)         # Set up the original position of small enemy plane
        self.mask = pygame.mask.from_surface(self.image)

        self.down_sound = pygame.mixer.Sound("sound/enemy1_down.wav")     # Load the sound of small enemy plane get destroyed and down
        self.down_sound.set_volume(0.3)                                   # Volume

    def move(self):                             # Define the method to move
        if self.rect.top < self.height - 60:
            self.rect.top +=  self.speed
        else:
            self.reset()
    def reset(self):
        self.active = True         # Reset the state of plane          
        self.rect.left, self.rect.top = randint(0, self.width - self.rect.width),\
                                        randint(-5*self.height,0)         # The position where the enemy plane appeared is random
    def play_sound(self):
        self.down_sound.play()     # Play the sound effect of plane get destroyed and down
  
# Medium enemy plane
class MidEnemy(pygame.sprite.Sprite):
    ENERGY = 10
    def __init__(self,screen_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/3.png").convert_alpha()           # Load the medium enemy image
        self.destroy_images = []
        self.destroy_images.extend([
            pygame.image.load("./images/enemy2_down1.png").convert_alpha(),      # Load the image of medium enemy plane get destroyed and down
            pygame.image.load("./images/enemy2_down2.png").convert_alpha(),
            pygame.image.load("./images/enemy2_down3.png").convert_alpha(),
            pygame.image.load("./images/enemy2_down4.png").convert_alpha()])
        self.rect = self.image.get_rect()
        self.width, self.height = screen_size[0], screen_size[1]
        self.speed = 1
        self.active = True
        self.energy = MidEnemy.ENERGY
        self.rect.left, self.rect.top = randint(0, self.width - self.rect.width),\
                                        randint(-10*self.height, -self.height)   # Set up the original position of small enemy plane
        self.mask = pygame.mask.from_surface(self.image)

        self.down_sound = pygame.mixer.Sound("sound/enemy2_down.wav")
        self.down_sound.set_volume(0.3)                                          # Play the sound of plane get destroyed and down

    def move(self):                           # Define the method to move
        if self.rect.top < self.height - 60:
            self.rect.top +=  self.speed
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.energy = MidEnemy.ENERGY
        self.rect.left, self.rect.top = randint(0, self.width - self.rect.width),\
                                        randint(-10*self.height,0)               # The position where the enemy plane appeared is random

    def play_sound(self):
        self.down_sound.play()



# My plane
class myPlane(pygame.sprite.Sprite):         # Create a class of myPlane
    def __init__(self,screen,screen_size):
        pygame.sprite.Sprite.__init__(self)
        self.image1 = pygame.image.load('./images/1.png').convert_alpha()            # Load the first image of myPlane
        self.image2 = pygame.image.load('./images/1.png').convert_alpha()            # Load the second image. Two images are continuously replaced and creatr animation effects
        self.mask = pygame.mask.from_surface(self.image1)
        self.rect = self.image1.get_rect()
        self.width,self.height = screen_size[0],screen_size[1]                       # Get the size of the screen
        self.rect.left,self.rect.bottom = (self.width-self.rect.width)//2, self.height-10
 
        self.screen = screen       # Draw the display
        self.speed = 10            # Speed of My plane
        self.switch_image = True   # The sign of switching between two images
        self.delay = 100           # Delay time for switching between two pictures
 
        self.destroy_images = []            
        self.destroy_images.extend([
            pygame.image.load('./images/me_destroy_1.png').convert_alpha(),    # Load four images of the destoryed plane and add them in the list
            pygame.image.load('./images/me_destroy_2.png').convert_alpha(),
            pygame.image.load('./images/me_destroy_3.png').convert_alpha(),
            pygame.image.load('./images/me_destroy_4.png').convert_alpha()])
        self.active = True         
        self.down_sound = pygame.mixer.Sound("sound/me_down.wav")                     # Load the sound of myPlane get destroyed and down
        self.down_sound.set_volume(0.2)                                               # Volume



    def moveUp(self):
        if self.rect.top > 0:
            self.rect.top -= self.speed
        else:
            self.rect.top = 0
 
    def moveDown(self):
        if self.rect.bottom < self.height-10:
            self.rect.bottom += self.speed
        else:
            self.rect.bottom = self.height-10
 
    def moveLeft(self):
        if self.rect.left > 0:
            self.rect.left -= self.speed
        else:
            self.rect.left = 0
 
    def moveRight(self):
        if self.rect.right < self.width:
            self.rect.right += self.speed
        else:
            self.rect.right = self.width
 
    def animation(self):
        if self.switch_image:
            self.screen.blit(self.image1, self.rect)
        else:
            self.screen.blit(self.image2, self.rect)
        if self.delay % 5 == 0:
            self.switch_image = not self.switch_image
        self.delay -= 1
        if self.delay == 0:
            self.delay = 100
 
    def time_delay(self):    
        self.delay -= 1
        if self.delay == 0:
            self.delay = 100
 
    def reset(self):    
        self.active = True
        self.rect.left, self.rect.bottom = (self.width - self.rect.left) // 2, self.height - 10
 
    def play_sound(self):        # Play sound effect
        self.down_sound.play()



# Bullet
class Bullet(pygame.sprite.Sprite):                   # Create the class of Bullet
    def __init__(self, position, direction):
        pygame.sprite.Sprite.__init__(self)           # Initialize the sprite

        self.image = pygame.image.load(
            "./images/bullet1.png").convert_alpha()   # Load the image of bullet
        self.rect = self.image.get_rect()             
        self.rect.left, self.rect.top = position      # Set up the original position of bullet
        self.speed = 12        # Speed of bullet
        self.active = True     
        self.mask = pygame.sprite.from_surface(self.image)    
        self.direction = direction    # Direction of the bullet

    def move(self):              # Define the method of move
        if self.direction:       # If the direction of bullet is upward，direction is True
            self.rect.top -= self.speed    # Bullet move
            if self.rect.top < 0:          # Determine whether the bullet exceeds the boundary
                self.active = False     
        else:
            self.rect.top += self.speed
            if self.rect.top > 700:
                self.active = False

    def reset(self, position):
        self.rect.left, self.rect.top = position    # Rebrith the bullet
        self.active = True                        
