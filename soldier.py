import pygame
from enemy import Enemy

class Soldier(Enemy):
  def __init__(self, pos, score = 100, life = 3, variant = 'blue'):
    super().__init__('soldier', pos, score, life, variant, 400)

    self.direction = pygame.math.Vector2(0, 0)
    self.speed = 6
    self.gravity = 0.8

    self.facing = 1


  def apply_gravity(self):
    self.direction.y += self.gravity
    self.rect.y += self.direction.y


  def patrol(self):
    pass

  def update(self, x_shift, player):
    self.rect.x += x_shift
    
    self.alert(player)
