import math
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

    # Update the position of the ball
    def update(self):
      # Convert sin and cos
      direction_radians = math.radians(self.direction)
      # Change position according to speed and direction
      self.x += self.speed * math.sin(direction_radians)
      self.y -= self.speed * math.cos(direction_radians)

      if self.y < 0:
        self.reset()

      if self.y > 600:
        self.reset()

      # Move image
      self.rect.x = self.x
      self.rect.y = self.y

      # Manage bouncing off the sides of the screen
      if self.x < 0:
        self.direction = (360 - self.direction) % 360
        print(self.direction)

      if self.x > self.screenwidth - self.width:
        self.direction = (360 - self.direction) % 360

  while True:
    for event in pygame.event.get():
      if event.type==QUIT:
        pygame.quit()
        sys.exit()
    pygame.display.update()

main()