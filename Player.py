import pygame

WHITE = pygame.Color("white")

class Player(pygame.sprite.Sprite):
  """Class to set the properties and behaviors of the player"""
  def __init__(self, y_pos, player_num):
    super(Player, self).__init__()

    self.player_number = player_num

    self.width = 75
    self.height = 15
    self.image = pygame.Surface([self.width, self.height])
    self.image.fill(WHITE)

    self.rect = self.image.get_rect()
    self.screenheight = pygame.display.get_surface().get_height()
    self.screenwidth = pygame.display.get_surface().get_width()

    self.rect.x = (pygame.display.get_surface().get_width() / 2) - 37.5
    self.rect.y = y_pos

  def update(self):
    """Constantly running function that controls the player's movement and position"""
    pressed = pygame.key.get_pressed()
    if self.player_number == 1:
      if pressed[pygame.K_a] and self.rect.x > 10:
        self.rect.x -= 10
      elif pressed[pygame.K_d] and self.rect.x < self.screenwidth - 75:
        self.rect.x += 10
    elif self.player_number == 2:
      if pressed[pygame.K_LEFT] and self.rect.x > 10:
        self.rect.x -= 10
      elif pressed[pygame.K_RIGHT] and self.rect.x < self.screenwidth - 75:
        self.rect.x += 10

  def reset(self):
    """Resets the player back to the center of the screen after a point is scored"""
    self.rect.x = (pygame.display.get_surface().get_width() / 2) - 37.5