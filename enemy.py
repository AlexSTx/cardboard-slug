from abc import abstractmethod
import pygame
from math import sqrt

class Enemy(pygame.sprite.Sprite):
  def __init__(self, type, pos, score, life, variant, alert_radius):
    super().__init__()

    self.image = pygame.Surface((32, 64))
    self.image.fill(variant)
    self.rect = self.image.get_rect(topleft = pos)
    
    self.score = score
    self.life = life
    self.type = type

    self.alert_state = False
    self.alert_radius = alert_radius
  

  def alert(self, player):
    if not self.alert_state:
      distance = sqrt((self.rect.x - player.rect.x)**2 + (self.rect.y - player.rect.y)**2)
      if distance < self.alert_radius:
        self.alert_state = True
    else:
      print('alertado!!!')
    

  def follow(self):
    pass


  def attack(self):
    pass


  def update(self):
    pass