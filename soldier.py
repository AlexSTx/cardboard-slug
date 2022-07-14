import pygame
from random import random

from enemy import Enemy

class Soldier(Enemy):
  def __init__(self, pos, collidable_tiles, score, life, variant):
    super().__init__('soldier', pos, score, life, variant, 400, 500)

    self.collidable_tiles = collidable_tiles

    self.speed = 2 * (1 + random())


  def can_move_forward(self):
    border = True
    y_verify = self.rect.bottom + self.speed 
    if self.direction.x == 1: x_verify = self.rect.right + (self.speed * self.direction.x)
    else: x_verify = self.rect.left + (self.speed * self.direction.x)

    for tile in self.collidable_tiles.sprites():
      if tile.rect.collidepoint(x_verify, y_verify):
        border = False
      if tile.rect.collidepoint(x_verify, self.rect.centery):
        border = True
        break
    return not border


  def walk(self):
    self.rect.x += self.direction.x * self.speed

    
  def change_direction(self):
    self.looking_right = not self.looking_right
    self.direction.x *= -1


  def patrol(self):
    if not self.can_move_forward():
      self.change_direction() 
    self.walk()     
    

  def follow(self, player):
    # checa o lado que o inimigo está olhando
    if self.rect.right < player.rect.right:
      self.looking_right = True
    else:
      self.looking_right = False

    # checa a distância entre inimigo e player
    if self.player_distance > self.minimum_player_distance:
      self.direction.x = 1
    elif self.player_distance < self.minimum_player_distance:
      self.direction.x = -1
    else: self.direction.x = 0

    # se tiver olhando pra esquerda, inverte a direção
    if not self.looking_right:
      self.direction.x *= -1

    # se puder andar, anda
    if self.can_move_forward():
      self.walk()


  def update(self, x_shift, player):
    if not super().update(x_shift, player): return

    if self.action == 'patrol':
      self.patrol()
    elif self.action == 'follow':
      self.follow(player)
    
    if self.alert_state:
      if self.can_attack:
        self.attack(player)
      self.action = 'follow'

    self.update_attack_delay()
    self.update_alert_delay()
