# Import the pygame module
import pygame
import random
import sys

from Rock import Rock
from Bullet import Bullet

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    K_a,
    K_d,
    KEYDOWN,
    KEYUP,
    QUIT,
)

# Initialize pygame
pygame.init()
pygame.display.set_caption('Rock Shooter - Score: 0')

pygame.font.init()

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
 
bullets = []
rocks = []

score = 0

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
  movement_speed = 10
  fire_rate = 250
  width = 75
  height = 25
  last_shot = pygame.time.get_ticks()

  def __init__(self):
    super(Player, self).__init__()
    self.surf = pygame.Surface((self.width, self.height))
    self.surf.fill((0, 0, 0))
    self.rect = self.surf.get_rect()
    self.rect.move_ip(SCREEN_WIDTH/2 - self.width/2,SCREEN_HEIGHT*0.8)
  
  def shoot(self):
    bullets.append(Bullet([self.rect.centerx,SCREEN_HEIGHT*0.8]))
          
  def update(self, pressed_keys):
    # if pressed_keys[K_UP]:
    #   self.rect.move_ip(0, -self.movement_speed)
    # if pressed_keys[K_DOWN]:
    #   self.rect.move_ip(0, self.movement_speed)
    if pressed_keys[K_LEFT] or pressed_keys[K_a]:
      self.rect.move_ip(-self.movement_speed, 0)
    if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
      self.rect.move_ip(self.movement_speed, 0)
      
    # Keep player on the screen
    if self.rect.left < 0:
      self.rect.left = 0
    if self.rect.right > SCREEN_WIDTH:
      self.rect.right = SCREEN_WIDTH
    if self.rect.top <= 0:
      self.rect.top = 0
    if self.rect.bottom >= SCREEN_HEIGHT:
      self.rect.bottom = SCREEN_HEIGHT
    
def gameOver(message):
  pygame.display.quit()
  pygame.quit()
  print(message)
  print(f'\nScore: {score}')
  return sys.exit()

player = Player()

# Variable to keep the main loop running
running = True
pressed=False
# Main loop
while running:
  # Look at every event in the queue
  for event in pygame.event.get():
      # Did the user hit a key?
      if event.type == KEYDOWN:
        # Was it the Escape key? If so, stop the loop.
        if event.key == K_ESCAPE:
            running = False
            
        if event.key == K_SPACE and not pressed: 
          # Do something
          player.shoot()
          pressed = True
      
      if event.type == KEYUP:
        if event.key == K_SPACE:
          pressed = False

      # Did the user click the window close button? If so, stop the loop.
      elif event.type == QUIT:
          running = False
      


  # Fill the screen with white
  screen.fill((255, 255, 255))
  
  screen.blit(player.surf, player.rect)
  
  # handle bullet rendering
  for bullet in bullets:
    if bullet.rect.y < 0:
      bullets.remove(bullet) # remove bullet if it goes off top of screen
      
    bullet.update()
    screen.blit(bullet.surf, bullet.rect)
  
  # handle rock rendering

  # randomly spawn rocks
  if random.randint(1,100) == 69:
    rocks.append(Rock([random.randint(player.width,SCREEN_WIDTH-player.width),0], 2))

  for rock in rocks:
    if rock.rect.y > SCREEN_HEIGHT:
      rocks.remove(rock)
      gameOver('A rock got past the player and destroyed the universe.')
            
    if pygame.sprite.spritecollideany(rock, bullets):
      rocks.remove(rock)
      score += 1
      pygame.display.set_caption(f'Rock Shooter - Score: {score}')
    
    rock.update()
    screen.blit(rock.surf, rock.rect)
  
  pressed_keys = pygame.key.get_pressed()

  player.update(pressed_keys)
  
  # handle player collision
  if pygame.sprite.spritecollideany(player,  rocks):
    gameOver('The player was smashed to bits by a rock.')
  
  pygame.display.flip()
  clock.tick(60)
