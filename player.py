import pygame
from projectile import Projectile

class Player(pygame.sprite.Sprite):
  def __init__(self, pos, projectiles):
    super().__init__()
    self.type = 'player'

    self.image = pygame.Surface((32, 64))
    self.image.fill('red')
    self.rect = self.image.get_rect(topleft = pos)

    self.projectiles = projectiles

    # player movement
    self.direction = pygame.math.Vector2(0, 0) 
    self.speed = 6
    self.gravity = 0.8
    self.jump_speed = -16

    # player state
    self.on_floor = True
    self.idle = True

    # player interaction
    self.can_shoot = True
    self.delay = 0.4
    self.last_shot = pygame.time.get_ticks()
    self.time_passed = 0


  def get_input(self):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
      self.direction.x = 1
    elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
      self.direction.x = -1
    else:
      self.direction.x = 0

    if keys[pygame.K_SPACE] and self.on_floor == True:
      self.jump()    

    if pygame.mouse.get_pressed()[0] and self.can_shoot:
      self.shoot(pygame.mouse.get_pos())


  def shoot(self, target):
    direction = pygame.math.Vector2(target[0] - self.rect.x, target[1] - self.rect.y) 
    self.projectiles.add(Projectile((self.rect.center), direction))

    self.last_shot = pygame.time.get_ticks()
    self.time_passed = 0
    self.can_shoot = False


  def apply_gravity(self):
    self.direction.y += self.gravity
    self.rect.y += self.direction.y


  def update_delay(self):
    self.time_passed = (pygame.time.get_ticks() - self.last_shot)/1000
    if self.time_passed > self.delay:
      self.can_shoot = True


  def jump(self):
    self.direction.y = self.jump_speed


  def update(self):
    self.get_input()
    self.update_delay()
    