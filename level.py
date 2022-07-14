import pygame

from settings import tile_size, screen_width

from tiles import Tile
from player import Player

from soldierRanged import SoldierRanged
from soldierMeelee import SoldierMeelee

class Level:
  def __init__(self, level_data, surface):

    # entities
    self.collidable_tiles = pygame.sprite.Group()
    self.non_collidable_tiles = pygame.sprite.Group()
    self.projectiles = pygame.sprite.Group()
    self.enemies = pygame.sprite.Group()
    self.player = pygame.sprite.GroupSingle()

    # level setup
    self.display_surface = surface
    self.setup_level(level_data)


    self.world_shift = 0
      

  def setup_level(self, layout):
    for row_index, row in enumerate(layout):
      for col_index, cell in enumerate(row):
        x = col_index * tile_size
        y = row_index * tile_size

        if cell == 'X':
          tile = Tile((x, y), tile_size)
          self.collidable_tiles.add(tile)
        if cell == 'V':
          tile = Tile((x, y), tile_size)
          self.non_collidable_tiles.add(tile)
        if cell == 'P':
          player_sprite = Player((x, y), self.projectiles)
          self.player.add(player_sprite)
        if cell == 'S':
          enemy = SoldierRanged((x, y), self.collidable_tiles, self.projectiles)
          self.enemies.add(enemy)
        if cell == 's':
          enemy = SoldierMeelee((x, y), self.collidable_tiles)
          self.enemies.add(enemy)

  
  def scroll_x(self):
    player = self.player.sprite
    player_x = player.rect.centerx
    direction_x = player.direction.x

    if player_x < (screen_width / 4) and direction_x < 0:
      self.world_shift = 8
      player.speed = 0
    elif player_x > screen_width / 2 and direction_x > 0:
      self.world_shift = -8
      player.speed = 0
    else:
      self.world_shift = 0
      player.speed = 8


  def horizontal_movement_collision(self):
    player = self.player.sprite
    player.rect.x += player.direction.x * player.speed

    # player
    for tile in self.collidable_tiles.sprites():
      if tile.rect.colliderect(player.rect):
        if player.direction.x < 0:
          player.rect.left = tile.rect.right
        elif player.direction.x > 0:
          player.rect.right = tile.rect.left
      for projectile in self.projectiles.sprites():
        if tile.rect.colliderect(projectile.rect) and projectile.type in [-1, 1]:
            projectile.kill()


  def vertical_movement_collision(self):
    player = self.player.sprite
    player.apply_gravity()

    player.on_floor = False

    # player
    for tile in self.collidable_tiles.sprites():
      if tile.rect.colliderect(player.rect):
        if player.direction.y > 0:
          player.rect.bottom = tile.rect.top
          player.direction.y = 0
          player.on_floor = True
        elif player.direction.y < 0:
          player.rect.top = tile.rect.bottom
          player.direction.y = 0
      for projectile in self.projectiles.sprites(): 
        if tile.rect.colliderect(projectile.rect) and projectile.type in [-1, 1]:
            projectile.kill()
    

  def check_damage(self):
    for projectile in self.projectiles.sprites():
      if projectile.type > 0:
        for enemy in self.enemies.sprites():
          if enemy.rect.colliderect(projectile.rect):
            enemy.take_hit(projectile.damage)
            projectile.kill()


  def run(self):      
    # level tiles
    self.collidable_tiles.update(self.world_shift)
    self.non_collidable_tiles.update(self.world_shift)
    self.collidable_tiles.draw(self.display_surface)
    self.non_collidable_tiles.draw(self.display_surface)
    self.scroll_x()
    
    # player
    self.player.update()
    self.player.draw(self.display_surface)

    # projectiles
    self.projectiles.update()
    self.projectiles.draw(self.display_surface)
    self.check_damage()

    # enemies
    self.enemies.update(self.world_shift, self.player.sprite)
    self.enemies.draw(self.display_surface)

    # world
    self.horizontal_movement_collision()
    self.vertical_movement_collision()
