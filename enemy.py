from math import sqrt
from random import choice

import pygame

from settings import screen_width

class Enemy(pygame.sprite.Sprite):
  def __init__(self, type, pos, score, life, variant, alert_radius, attack_radius):
    super().__init__()

    self.image = pygame.Surface((32, 64))
    self.image.fill(variant)
    self.rect = self.image.get_rect(topleft = pos)
    
    self.score = score
    self.life = life
    self.type = type

    self.direction = pygame.math.Vector2(0, 0)
    self.looking_right = choice([True, False])
    self.direction.x = 1 if self.looking_right else -1    

    self.seen = False
    self.alert_state = False
    self.alert_radius = alert_radius
    self.alert_time = 5
    self.alert_timer = 0
    self.alerted = 0

    self.can_attack = True
    self.attack_delay = 0.9
    self.attack_radius = attack_radius
    self.last_attack = pygame.time.get_ticks()
    self.time_passed_last_attack = 0

    self.action = 'patrol'

  
  def calc_player_distance(self, player):
    self.player_distance = sqrt((self.rect.x - player.rect.x)**2 + (self.rect.y - player.rect.y)**2)


  def alert(self):
    if self.alert_radius == 0 or self.player_distance < self.alert_radius:
      self.alert_state = True
      self.alerted = pygame.time.get_ticks()
      self.alert_timer = 0
      self.action = 'follow'


  def on_attack_radius(self):
    if self.alert_state == True and self.player_distance < self.attack_radius:
      return True
    else:
      return False
   

  def enemy_visibility(self):
    if not self.seen:
        if self.rect.left < screen_width:
          self.seen = True


  def update_attack_delay(self):
    self.time_passed_last_attack = (pygame.time.get_ticks() - self.last_attack)/1000
    if self.time_passed_last_attack > self.attack_delay:
      self.can_attack = True


  def update_alert_delay(self):
    if self.alert_state and not self.on_attack_radius():
      self.alert_timer = (pygame.time.get_ticks() - self.alerted)/1000
      if self.alert_timer >= self.alert_time:
        self.alert_state = False
        self.action = 'patrol'


  def take_hit(self, damage):
    self.life -= damage
    if self.life <= 0:
      self.kill()


  def follow(self):
    pass


  def attack(self):
    pass


  def update(self, x_shift, player):
    self.rect.x += x_shift
    self.enemy_visibility()

    if not self.seen:
      return False
    
    self.calc_player_distance(player)
    self.alert()
  
    return True