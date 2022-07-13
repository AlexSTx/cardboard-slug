import pygame
from enemy import Enemy
from projectile import Projectile
from random import choice

class Soldier(Enemy):
  def __init__(self, pos, collidable_tiles, projectiles, score = 100, life = 3, variant = 'blue'):
    super().__init__('soldier', pos, score, life, variant, 400)

    self.collidable_tiles = collidable_tiles

    self.direction = pygame.math.Vector2(0, 0)
    self.speed = 3
    self.gravity = 0.8

    self.looking_right = choice([True, False])
    self.direction.x = 1 if self.looking_right else -1

    # attack
    self.can_attack = True
    self.delay = 0.9
    self.last_attack = pygame.time.get_ticks()
    self.time_passed = 0
    self.projectiles = projectiles


  def apply_gravity(self):
    self.direction.y += self.gravity
    self.rect.y += self.direction.y


  def change_direction(self):
    self.looking_right = not self.looking_right
    self.direction.x *= -1


  def patrol(self):
    turn = True

    y_verify = self.rect.bottom + self.speed 
    x_verify = (self.rect.right if self.looking_right else self.rect.left) + (self.speed * self.direction.x)

    for tile in self.collidable_tiles.sprites():
      if tile.rect.collidepoint(x_verify, y_verify):
        turn = False
      if tile.rect.collidepoint(x_verify, self.rect.centery):
        turn = True
        break
 
    if turn:
      self.change_direction()

    self.rect.x += self.direction.x * self.speed


  def attack(self, player):
    direction = pygame.math.Vector2(player.rect.centerx - self.rect.x, player.rect.centery - self.rect.y) 
    self.projectiles.add(Projectile((self.rect.center), direction, -1, 15, 0.0075))

    self.last_attack = pygame.time.get_ticks()
    self.time_passed = 0
    self.can_attack = False


  def update_delay(self):
    self.time_passed = (pygame.time.get_ticks() - self.last_attack)/1000
    if self.time_passed > self.delay:
      self.can_attack = True


  def update(self, x_shift, player):
    super().update(x_shift, player)

    if self.visible:
      self.patrol()
    
    if self.alert_state:
      if self.can_attack:
        self.attack(player)

    self.update_delay()
