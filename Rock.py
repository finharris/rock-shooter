import pygame

class Rock(pygame.sprite.Sprite):
  width = 40
  height = 40

  def __init__(self, position, movement_speed = 1):
    super(Rock, self).__init__()
    self.surf = pygame.Surface((self.width, self.height))
    self.surf.fill((0, 0, 0))
    self.rect = self.surf.get_rect()
      
    self.rect.move_ip(position[0],position[1])

    self.movement_speed = movement_speed
          
  def update(self):
    # move upwards
    self.rect.move_ip(0, self.movement_speed)
