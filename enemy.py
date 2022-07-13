from math import sqrt

import pygame

from settings import screen_width

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
    self.visible = False
  

  def alert(self, player):
    # if not self.alert_state:
    distance = sqrt((self.rect.x - player.rect.x)**2 + (self.rect.y - player.rect.y)**2)
    if distance < self.alert_radius:
      self.alert_state = True
      # print('alertado!!!')
    else:
      self.alert_state = False
    

  def enemy_visibility(self):
    if not self.visible:
        if self.rect.left < screen_width:
          self.visible = True


  def follow(self):
    pass


  def attack(self):
    pass


  def update(self, x_shift, player):
    self.rect.x += x_shift
    self.enemy_visibility()
    
    if self.visible:
      self.alert(player)