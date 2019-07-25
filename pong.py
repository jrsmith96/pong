import math
import pygame
import random

# Initialize the Pygame library 
pygame.init()

# Sounds
pygame.mixer.music.load('pong_bounce.ogg')

WHITE = pygame.Color("white")

SCORE_1 = 0
SCORE_2 = 0

PAUSED = False
font = pygame.font.Font(None, 36)
value = 0

def pause():

  while PAUSED:

    for event in pygame.event.get():
      if event.type == pygame.KEYUP:
        if event.key == pygame.K_p:
          unpause()

def unpause():
  global PAUSED
  PAUSED = False

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
    self.reset(0)

  def reset(self, direction):

    self.x = pygame.display.get_surface().get_width() / 2
    self.y = pygame.display.get_surface().get_height() / 2
    self.speed = 8.0

    self.direction = direction
    self.y = pygame.display.get_surface().get_height() / 2

  def bounce(self, diff):
    pygame.mixer.music.play(0)
    self.direction = (180 - self.direction) % 360
    self.direction -= diff

    # Increase screen with each bounce
    self.speed *= 1.05

  # Update the position of the ball
  def update(self):
    # Convert sin and cos
    direction_radians = math.radians(self.direction)
    # Change position according to speed and direction
    self.x += self.speed * math.sin(direction_radians)
    self.y -= self.speed * math.cos(direction_radians)

    if self.y < 0:
      global SCORE_1
      SCORE_1 += 1
      self.reset(0)
      player1.reset()
      player2.reset()
      
    if self.y > 600:
      global SCORE_2
      SCORE_2 += 1
      self.reset(180)
      player1.reset()
      player2.reset()

    # Move image
    self.rect.x = self.x
    self.rect.y = self.y

    # Manage bouncing off the sides of the screen
    if self.x < 0:
      pygame.mixer.music.play(0)
      self.direction = (360 - self.direction) % 360

    if self.x > self.screenwidth - self.width:
      pygame.mixer.music.play(0)
      self.direction = (360 - self.direction) % 360

class Player(pygame.sprite.Sprite):
  def __init__(self, y_pos, playerNumber):
    super().__init__()

    self.playerNumber = playerNumber

    self.width=75
    self.height=15
    self.image = pygame.Surface([self.width, self.height])
    self.image.fill(WHITE)

    self.rect = self.image.get_rect()
    self.screenheight = pygame.display.get_surface().get_height()
    self.screenwidth = pygame.display.get_surface().get_width()

    self.rect.x = (pygame.display.get_surface().get_width() / 2) - 37.5
    self.rect.y = y_pos

  def update(self):

    pressed = pygame.key.get_pressed()
    if self.playerNumber == 1:
      if pressed[pygame.K_a] and self.rect.x > 10:
        self.rect.x -= 10
      elif pressed[pygame.K_d] and self.rect.x < self.screenwidth - 75:
        self.rect.x += 10
    elif self.playerNumber == 2:
      if pressed[pygame.K_LEFT] and self.rect.x > 10:
        self.rect.x -= 10
      elif pressed[pygame.K_RIGHT] and self.rect.x < self.screenwidth - 75:
        self.rect.x += 10

  def reset(self):

    self.rect.x = (pygame.display.get_surface().get_width() / 2) - 37.5

DISPLAY = pygame.display.set_mode([800,600])
pygame.display.set_caption('Pong')
pygame.mouse.set_visible(0)
background = pygame.Surface(DISPLAY.get_size())

ball = Ball()
balls = pygame.sprite.Group()
balls.add(ball)

player1 = Player(580, 1)
player2 = Player(25, 2)

movingsprites = pygame.sprite.Group()
movingsprites.add(player1)
movingsprites.add(player2)
movingsprites.add(ball)

clock = pygame.time.Clock()
done = False
exit_program = False

while not exit_program:

  DISPLAY.fill(pygame.Color("black"))

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      exit_program = True
    if event.type == pygame.KEYUP:
      if event.key == pygame.K_p:
        PAUSED = True
        pause()

  if abs(SCORE_1 - SCORE_2) > 3:
    done = True

  if not done:
    player1.update()
    player2.update()
    ball.update()

  if done:
    text = font.render("Game Over", 1, (200, 200, 200))
    textpos = text.get_rect(centerx = background.get_width() / 2)
    textpos.top = 50
    DISPLAY.blit(text, textpos)

  if pygame.sprite.spritecollide(player1, balls, False):

    diff = (player1.rect.x + player1.width / 2) - (ball.rect.x + ball.width / 2)

    ball.y = 570
    ball.bounce(diff)
 
  if pygame.sprite.spritecollide(player2, balls, False):

    diff = (player2.rect.x + player2.width / 2) - (ball.rect.x + ball.width / 2)

    ball.y = 40
    ball.bounce(diff)

  scoreprint = "Player 1: "+str(SCORE_1)
  text = font.render(scoreprint, 1, WHITE)
  textpos = (0, 0)
  DISPLAY.blit(text, textpos)
 
  scoreprint = "Player 2: "+str(SCORE_2)
  text = font.render(scoreprint, 1, WHITE)
  textpos = (680, 0)
  DISPLAY.blit(text, textpos)

  movingsprites.draw(DISPLAY)

  pygame.display.flip()

  clock.tick(30)

pygame.quit()