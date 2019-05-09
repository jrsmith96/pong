import pygame
from pygame.locals import *

def main():
  # Initialize the Pygame library 
  pygame.init()
  pygame.font.init()

  DISPLAY=pygame.display.set_mode((800,600),0,32)

  WHITE=(255,255,255)
  BLUE=(0,0,255)

  # pygame.draw.circle(DISPLAY, WHITE, (300, 200), 10)

  class Ball(pygame.sprite.Sprite):

    # Constructor
    def __init__(self):
      super().__init__()

      self.image = pygame.Surface([10,  10])
      self.image.fill(WHITE)

      # Ball hitspace
      self.rect = self.image.get_rect()

      self.screenheight = pygame.display.get_surface().get_height()
      self.screenwidth = pygame.display.get_surface().get_width()
      self.speed = 0

      # Ball pos
      self.x = 0
      self.y = 0

      # Ball direction
      self.direction = 0

      # Ball dimensions
      self.width = 10
      self.height = 10

      # Reset ball to initial speed and position
      self.reset()

    # TODO: Need to add which direction the ball will go to after each round
    def reset(self):
      self.x = 300.0
      self.y = 200.0
      self.speed = 5.0

    def bounce(self, diff):
      self.direction = (180 - self.direction) % 360
      self.direction -= diff

      # Increase screen with each bounce
      self.speed *= 1.1

    def update(self):


  while True:
    for event in pygame.event.get():
      if event.type==QUIT:
        pygame.quit()
        sys.exit()
    pygame.display.update()

main()