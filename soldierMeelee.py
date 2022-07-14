import pygame
from soldier import Soldier

class SoldierMeelee(Soldier):
  def __init__(self, pos, collidable_tiles, score = 100, life = 3, variant = 'green'):
    super().__init__(pos, collidable_tiles, score, life, variant)

    self.minimum_player_distance = 30  

  def attack(self, player):
    attack_range = 30
    if self.looking_right:
      rect = (self.rect.right, self.rect.top, attack_range, self.rect.height)
    else:
      rect = (self.rect.left - attack_range, self.rect.top, attack_range, self.rect.height)

    if player.rect.colliderect(rect):
      print('hit')  
      self.last_attack = pygame.time.get_ticks()
      self.time_passed_last_attack = 0
      self.can_attack = False
    
