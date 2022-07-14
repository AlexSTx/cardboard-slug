import pygame

from random import randint

from soldier import Soldier
from projectile import Projectile


class SoldierRanged(Soldier):
  def __init__(self, pos, collidable_tiles, projectiles, score = 100, life = 3, variant = 'blue'):
    super().__init__(pos, collidable_tiles, score, life, variant)

    self.projectiles = projectiles
    self.minimum_player_distance = randint(250, 450)


  def attack(self, player):
    direction = pygame.math.Vector2(player.rect.centerx - self.rect.x, player.rect.centery - self.rect.y) 
    self.projectiles.add(Projectile((self.rect.center), direction, -1, 15, 0.005))

    self.last_attack = pygame.time.get_ticks()
    self.time_passed_last_attack = 0
    self.can_attack = False