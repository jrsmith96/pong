#!/usr/bin/env python3
"""A simple pong game in Pygame!"""

import math
import pygame
from Player import Player

# Initialize the Pygame library
pygame.init()

TITLE = True

# Sounds
BOUNCE_SOUND = pygame.mixer.Sound('sounds/pong_bounce.ogg')
VICTORY_SOUND = pygame.mixer.Sound('sounds/pong_victory.ogg')

DISPLAY = pygame.display.set_mode([800, 600])
CLOCK = pygame.time.Clock()

WHITE = pygame.Color("white")
BLUE = (0, 0, 200)
BRIGHT_BLUE = (0, 0, 255)
RED = (200, 0, 0)
BRIGHT_RED = (255, 0, 0)

SCORE_1 = 0
SCORE_2 = 0

PAUSED = False
FONT = pygame.font.Font(None, 36)
VALUE = 0

def text_objects(text, font):
  """Returns a text object that can be rendered to the game display"""
  text_surface = font.render(text, True, WHITE)
  return text_surface, text_surface.get_rect()

def button(message, x, y, w, h, inactive, active, action=None):
  """Creates a button"""
  mouse = pygame.mouse.get_pos()
  click = pygame.mouse.get_pressed()

  if x + w > mouse[0] > x and y + h > mouse[1] > y:
    pygame.draw.rect(DISPLAY, active, (x, y, w, h))
    if click[0] == 1 and action != None:
      if action == "play":
        print("Success!")
      elif action == "quit":
        pygame.quit()
        quit()

  else:
    pygame.draw.rect(DISPLAY, inactive, (x, y, w, h))

  small_text = pygame.font.Font("freesansbold.ttf", 20)
  text_surf, text_rect = text_objects(message, small_text)
  text_rect.center = ((x + (w / 2)), (y + (h / 2)))
  DISPLAY.blit(text_surf, text_rect)

def title_screen():
  """Displays title screen for the start of the game"""

  while TITLE:
    for instance in pygame.event.get():
      if instance.type == pygame.QUIT:
        pygame.quit()
        quit()
    large_text = pygame.font.Font('freesansbold.ttf', 57)
    text_surf, text_rect = text_objects("PONG", large_text)
    text_rect.center = ((400), (300))
    DISPLAY.blit(text_surf, text_rect)

    button("GO!", 150, 450, 100, 50, BLUE, BRIGHT_BLUE, "play")
    button("Quit", 550, 450, 100, 50, RED, BRIGHT_RED, "quit")

    pygame.display.update()
    CLOCK.tick(15)

def pause():
  """Pauses the game"""
  while PAUSED:

    for key in pygame.event.get():
      if key.type == pygame.KEYUP:
        if key.key == pygame.K_p:
          unpause()

def unpause():
  """Unpauses the game"""
  global PAUSED
  PAUSED = False

class Ball(pygame.sprite.Sprite):
  """Class to set the properties and behaviors of the ball"""

  # pylint: disable = too-many-instance-attributes
  # Constructor
  def __init__(self):
    super(Ball, self).__init__()

    self.image = pygame.Surface([10, 10])
    self.image.fill(WHITE)

    # Ball hitspace
    self.rect = self.image.get_rect()

    self.screenheight = pygame.display.get_surface().get_height()
    self.screenwidth = pygame.display.get_surface().get_width()
    self.speed = 0

    # Ball pos
    self._x = 0
    self._y = 0

    # Ball direction
    self.direction = 0

    # Ball dimensions
    self.width = 10
    self.height = 10

    # Reset ball to initial speed and position
    self.reset(0)

  def reset(self, direction):
    """Resets the ball after a player has scored"""
    self._x = pygame.display.get_surface().get_width() / 2
    self._y = pygame.display.get_surface().get_height() / 2
    self.speed = 8.0

    self.direction = direction
    self._y = pygame.display.get_surface().get_height() / 2

  def bounce(self, diff):
    """Executes whenever the ball bounces off a player"""
    pygame.mixer.Sound.play(BOUNCE_SOUND)
    self.direction = (180 - self.direction) % 360
    self.direction -= diff

    # Increase screen with each bounce
    self.speed *= 1.05

  # Update the position of the ball
  def update(self):
    """Constantly running function that determines the ball's movement and position"""
    # Convert sin and cos
    direction_radians = math.radians(self.direction)
    # Change position according to speed and direction
    self._x += self.speed * math.sin(direction_radians)
    self._y -= self.speed * math.cos(direction_radians)

    if self._y < 0:
      global SCORE_1
      SCORE_1 += 1
      self.reset(0)
      PLAYER_1.reset()
      PLAYER_2.reset()

    if self._y > 600:
      global SCORE_2
      SCORE_2 += 1
      self.reset(180)
      PLAYER_1.reset()
      PLAYER_2.reset()

    # Move image
    self.rect.x = self._x
    self.rect.y = self._y

    # Manage bouncing off the sides of the screen
    if self._x < 0:
      pygame.mixer.Sound.play(BOUNCE_SOUND)
      self.direction = (360 - self.direction) % 360

    if self._x > self.screenwidth - self.width:
      pygame.mixer.Sound.play(BOUNCE_SOUND)
      self.direction = (360 - self.direction) % 360

# title_screen()

pygame.display.set_caption('Pong')
pygame.mouse.set_visible(0)
BACKGROUND = pygame.Surface(DISPLAY.get_size())

BALL = Ball()
BALLS = pygame.sprite.Group()
BALLS.add(BALL)

PLAYER_1 = Player(580, 1)
PLAYER_2 = Player(25, 2)

MOVING_SPRITES = pygame.sprite.Group()
MOVING_SPRITES.add(PLAYER_1)
MOVING_SPRITES.add(PLAYER_2)
MOVING_SPRITES.add(BALL)

DONE = False
EXIT_PROGRAM = False

while not EXIT_PROGRAM:

  DISPLAY.fill(pygame.Color("black"))

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      EXIT_PROGRAM = True
    if event.type == pygame.KEYUP:
      if event.key == pygame.K_p:
        PAUSED = True
        pause()

  if abs(SCORE_1 - SCORE_2) > 3:
    DONE = True

  if not DONE:
    PLAYER_1.update()
    PLAYER_2.update()
    BALL.update()

  if DONE:
    if SCORE_1 > SCORE_2:
      TEXT = FONT.render("Player 1 wins!", 1, (200, 200, 200))
    else:
      TEXT = FONT.render("Player 2 wins!", 1, (200, 200, 200))
    TEST_POS = TEXT.get_rect(centerx=BACKGROUND.get_width() / 2)
    TEST_POS.top = 50
    DISPLAY.blit(TEXT, TEST_POS)

  if pygame.sprite.spritecollide(PLAYER_1, BALLS, False):

    DIFF = (PLAYER_1.rect.x + PLAYER_1.width / 2) - (BALL.rect.x + BALL.width / 2)

    BALL._y = 570 # pylint: disable = protected-access
    BALL.bounce(DIFF)

  if pygame.sprite.spritecollide(PLAYER_2, BALLS, False):

    DIFF = (PLAYER_2.rect.x + PLAYER_2.width / 2) - (BALL.rect.x + BALL.width / 2)

    BALL._y = 40 # pylint: disable = protected-access
    BALL.bounce(DIFF)

  SCORE_PRINT = "Player 1: "+str(SCORE_1)
  TEXT = FONT.render(SCORE_PRINT, 1, WHITE)
  TEST_POS = (0, 0)
  DISPLAY.blit(TEXT, TEST_POS)

  SCORE_PRINT = "Player 2: "+str(SCORE_2)
  TEXT = FONT.render(SCORE_PRINT, 1, WHITE)
  TEST_POS = (680, 0)
  DISPLAY.blit(TEXT, TEST_POS)

  MOVING_SPRITES.draw(DISPLAY)

  pygame.display.flip()

  CLOCK.tick(30)

pygame.quit()

# We desperately need a game_loop function
