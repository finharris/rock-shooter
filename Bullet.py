import pygame

class Bullet(pygame.sprite.Sprite):
  movement_speed = 10
  width = 10
  height = 20

  def __init__(self, player_position):
    super(Bullet, self).__init__()
    self.surf = pygame.Surface((self.width, self.height))
    self.surf.fill((0, 0, 0))
    self.rect = self.surf.get_rect()
    self.rect.move_ip(player_position[0],player_position[1])
          
  def update(self):
    # move upwards
    self.rect.move_ip(0, -self.movement_speed)
