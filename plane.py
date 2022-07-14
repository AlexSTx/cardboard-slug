import pygame

from random import choice

from enemy import Enemy
from settings import screen_width
from projectile import Projectile

class Plane(Enemy):
	def __init__(self, pos, projectiles, score = 300, life = 2, variant = 'blue'):
		super().__init__('plane', pos, score, life, variant, 0, 500)

		self.image_facing_left = pygame.transform.scale(pygame.image.load('img/enemy/plane.png').convert_alpha(), (32 * 2.3, 48 * 2))
		self.image_facing_right = pygame.transform.flip(self.image_facing_left, True, False)
		self.rect = self.image.get_rect(topleft = pos)

		self.image = self.image_facing_left
		self.direction = pygame.math.Vector2(-1, 0)
		
		self.speed = 8

		self.attack_delay = 0.7
		self.projectiles = projectiles


	def attack(self, player):
		direction = pygame.math.Vector2(player.rect.centerx - self.rect.x, player.rect.centery - self.rect.y)
		if self.rect.x > 0 and self.rect.x < screen_width:
			if (direction.x < 0 and self.direction.x < 0) or (direction.x > 0 and self.direction.x > 0):
				self.projectiles.add(Projectile((self.rect.center), direction, -1, 20, 0.005))

				self.last_attack = pygame.time.get_ticks()
				self.time_passed_last_attack = 0
				self.can_attack = False


	def move(self):
		self.rect.x += self.direction.x * self.speed
		if self.rect.right <= -50:
			self.direction.x = 1
			self.image = self.image_facing_right

		if self.rect.left >= screen_width + 50:
			self.direction.x = -1
			self.image = self.image_facing_left

	def update(self, x_shift, player):
		if not super().update(x_shift, player): return

		if self.action == 'follow':
			self.move()

		if self.alert_state:
			if self.can_attack:
				self.attack(player)
			self.action = 'follow'
		
		self.update_attack_delay()