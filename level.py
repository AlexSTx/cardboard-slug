import pygame
from tiles import Tile
from player import Player
from settings import tile_size, screen_width

class Level:
  def __init__(self, level_data, surface):

    # entities
    self.projectiles = pygame.sprite.Group()

    # level setup
    self.display_surface = surface
    self.setup_level(level_data)


    self.world_shift = 0

  
  def setup_level(self, layout):
    self.tiles = pygame.sprite.Group()
    self.player = pygame.sprite.GroupSingle()

    for row_index, row in enumerate(layout):
      for col_index, cell in enumerate(row):
        x = col_index * tile_size
        y = row_index * tile_size

        if cell == 'X':
          tile = Tile((x, y), tile_size)
          self.tiles.add(tile)
        if cell == 'P':
          player_sprite = Player((x, y), self.projectiles)
          self.player.add(player_sprite)

  
  def scroll_x(self):
    player = self.player.sprite
    player_x = player.rect.centerx
    direction_x = player.direction.x

    if player_x < (screen_width / 4) and direction_x < 0:
      self.world_shift = 8
      player.speed = 0
    elif player_x > (3 * screen_width / 4) and direction_x > 0:
      self.world_shift = -8
      player.speed = 0
    else:
      self.world_shift = 0
      player.speed = 8


  def horizontal_movement_collision(self):
    player = self.player.sprite
    player.rect.x += player.direction.x * player.speed

    for tile in self.tiles.sprites():
      if tile.rect.colliderect(player.rect):
        if player.direction.x < 0:
          player.rect.left = tile.rect.right
        elif player.direction.x > 0:
          player.rect.right = tile.rect.left


  def vertical_movement_collision(self):
    player = self.player.sprite
    player.apply_gravity()

    player.on_floor = False

    for tile in self.tiles.sprites():
      if tile.rect.colliderect(player.rect):
        if player.direction.y > 0:
          player.rect.bottom = tile.rect.top
          player.direction.y = 0
          player.on_floor = True
        elif player.direction.y < 0:
          player.rect.top = tile.rect.bottom
          player.direction.y = 0
  

  def run(self):      
    # level tiles
    self.tiles.update(self.world_shift)
    self.tiles.draw(self.display_surface)
    self.scroll_x()
    
    # player
    self.player.update()
    self.horizontal_movement_collision()
    self.vertical_movement_collision()
    self.player.draw(self.display_surface)

    # projectiles
    self.projectiles.update()
    self.projectiles.draw(self.display_surface)