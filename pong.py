import pygame
from pygame.locals import *

def main():
  pygame.init()
  pygame.font.init()

  DISPLAY=pygame.display.set_mode((600,400),0,32)

  WHITE=(255,255,255)
  BLUE=(0,0,255)

  pygame.draw.circle(DISPLAY, WHITE, (300, 200), 10)

  while True:
    for event in pygame.event.get():
      if event.type==QUIT:
        pygame.quit()
        sys.exit()
    pygame.display.update()

main()