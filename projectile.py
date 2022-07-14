import pygame
from settings import screen_height
from math import sqrt

class Projectile(pygame.sprite.Sprite):
  def __init__(self, pos, direction, type = 1, speed = 30, weight = 0.01, height_increase = 30, damage = 1):
    super().__init__()

    self.type = type

    self.image = pygame.Surface((10, 10))
    self.image.fill('yellow')
    self.rect = self.image.get_rect(center = pos)

    direction[1] -= height_increase
    self.direction = direction

    self.gravity = weight
    self.speed = speed
    self.damage = damage


  def move(self):
    x = self.direction[0]
    y = self.direction[1]

    self.vector_module = sqrt(x*x + y*y)
    self.direction.x /= self.vector_module
    self.direction.y /= self.vector_module

    self.rect.center += self.direction * self.speed

    if self.rect.y > screen_height or self.rect.y < 0:
      self.kill()


  def apply_gravity(self):
      self.direction.y += self.gravity
      self.rect.y += self.direction.y

  
  def update(self):
    self.move()
    self.apply_gravity()