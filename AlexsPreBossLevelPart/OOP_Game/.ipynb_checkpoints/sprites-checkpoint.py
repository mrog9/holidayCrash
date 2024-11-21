import pygame
from config import *
import math
import random

class Spritesheet:
	def __init__(self, file, rows, columns, tilesize, set_list, offset):
		self.sheet = pygame.image.load(file).convert()
		self.collection = []
		frames = []
		self.tilelist = []
		self.set_list = set_list
		total = 0
		for r in range(rows):
			for c in range(columns):
				self.tilelist.append(self.get_sprite(r*tilesize, c*tilesize, tilesize, tilesize, offset))
		for num in self.set_list:
			for i in range(num):
				frames.append(self.tilelist[i+total])
			self.collection.append(frames)
			total += num
			frames = []

	def get_sprite(self, y, x, width, height, offset):
		sprite = pygame.Surface([width, height+offset])
		sprite.blit(self.sheet, (0,offset), (x, y, width, height))
		sprite.set_colorkey(BLACK)
		return sprite

class Projectile(pygame.sprite.Sprite):
	def __init__(self, game, x, y, direction, color):
		self.game = game 
		self._layer = PROJECTILE_LAYER
		self.groups = self.game.all_sprites
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.offset = TILE_SIZE * SCALE

		if direction == 'right':
			self.dx = PROJ_SPEED
			self.dy = 0
			self.x = x + self.offset
			self.y = y + self.offset/2
		if direction == 'left':
			self.dx = -PROJ_SPEED
			self.dy = 0
			self.x = x 
			self.y = y + self.offset/2
		if direction == 'up':
			self.dx = 0
			self.dy = -PROJ_SPEED
			self.x = x + self.offset/2
			self.y = y 
		if direction == 'down':
			self.dx = 0
			self.dy = PROJ_SPEED
			self.x = x + self.offset/2
			self.y = y + self.offset
		
		self.width = PROJ_SIZE
		self.height = PROJ_SIZE

		self.image = pygame.Surface([self.width, self.height])
		self.image.fill(color)

		self.rect = self.image.get_rect()
		self.rect.x = self.x
		self.rect.y = self.y

	def update(self):
		self.detect_collision()
		self.movement()

	def detect_collision(self):
		collide_blocks = pygame.sprite.spritecollide(self, self.game.blocks, False)
		if collide_blocks:
			self.remove(self.game.all_sprites)
			self.kill()
		collide_enemies = pygame.sprite.spritecollide(self, self.game.enemies, False)
		if collide_enemies:
			self.remove(self.game.all_sprites)
			self.kill()
		for e in collide_enemies:
			e.tally_hit()

	def movement(self):
		self.rect.x += self.dx
		self.rect.y += self.dy			

class Player(pygame.sprite.Sprite):
	def __init__(self, game, x, y):
		self.game = game
		self._layer = PLAYER_LAYER
		self.groups = self.game.all_sprites, self.game.players
		pygame.sprite.Sprite.__init__(self, self.groups)

		self.x = x*TILE_SIZE*SCALE
		self.y = y*TILE_SIZE*SCALE
		self.width = TILE_SIZE
		self.height = TILE_SIZE

		self.dx = 0
		self.dy = 0

		self.facing = 'down'

		self.image = pygame.transform.scale(self.game.character_spritesheet.collection[0][0], 
			(self.width*SCALE,self.height*SCALE))

		self.rect = self.image.get_rect()
		self.rect.x = self.x
		self.rect.y = self.y

		self.char_step = 0;
		self.set_length = 2
		self.last = pygame.time.get_ticks()
		self.hit = 10
		self.life_color = GREEN

	def update(self):
		self.movement()

		self.rect.x += self.dx
		self.rect.y += self.dy 

		block_collision = pygame.sprite.spritecollide(self, self.game.blocks, False)

		if(block_collision):
			self.rect.x -= BOUNCE_BACK * self.dx
			self.rect.y -= BOUNCE_BACK * self.dy
			self.dx *= -(BOUNCE_BACK - 1) 
			self.dy *= -(BOUNCE_BACK - 1) 

		enemy_collision = pygame.sprite.spritecollide(self, self.game.enemies, False)

		if(enemy_collision):
			self.dock_health()
			self.rect.x -= BOUNCE_BACK * self.dx
			self.rect.y -= BOUNCE_BACK * self.dy
			self.dx *= -(BOUNCE_BACK - 1)  
			self.dy *= -(BOUNCE_BACK - 1) 

		for sprite in self.game.all_sprites:
			sprite.rect.x -= self.dx
			sprite.rect.y -= self.dy

		self.dx = 0
		self.dy = 0

	def movement(self):
		keys = pygame.key.get_pressed()

		if self.char_step >= self.set_length :
			self.char_step = 0

		self.image = pygame.transform.scale(self.set_img(), 
			(self.width*SCALE,self.height*SCALE))

		# Movement controls
		if keys[pygame.K_LEFT]:
			self.dx -= PLAYER_SPEED
			self.facing = 'left'
			self.char_step += 1
			self.set_length = self.game.character_spritesheet.set_list[0]-1
		if keys[pygame.K_RIGHT]:
			self.dx += PLAYER_SPEED
			self.facing = 'right'
			self.char_step += 1
			self.set_length = self.game.character_spritesheet.set_list[1]-1
		if keys[pygame.K_UP]:
			self.dy -= PLAYER_SPEED
			self.facing = 'up'
			self.char_step += 1
			self.set_length = self.game.character_spritesheet.set_list[2]-1
		if keys[pygame.K_DOWN]:
			self.dy += PLAYER_SPEED
			self.facing = 'down'
			self.char_step += 1
			self.set_length = self.game.character_spritesheet.set_list[3]-1
		if keys[pygame.K_SPACE]:
			now = pygame.time.get_ticks()
			if now - self.last >= 100:
				Projectile(self.game, self.rect.x, self.rect.y, self.facing, RED)
				self.last = pygame.time.get_ticks()

	def set_img(self):
		if self.facing == 'right':
			img = self.game.character_spritesheet.collection[2][self.char_step]
		if self.facing == 'left':
			img = self.game.character_spritesheet.collection[1][self.char_step]
		if self.facing == 'up':
			img = self.game.character_spritesheet.collection[3][self.char_step]
		if self.facing == 'down':
			img = self.game.character_spritesheet.collection[0][self.char_step]

		pygame.draw.rect(img, BLACK, pygame.Rect(0, 0, 32, 4)) # NEW
		pygame.draw.rect(img, self.life_color, pygame.Rect(1, 1, 30 - (3 * (10 - self.hit)), 2)) # NEW
		pygame.draw.rect(img, WHITE, pygame.Rect(0, 0, 32, 4), 1) # NEW
		return img

	def dock_health(self):
		self.hit -= 1
		if self.hit <= 5:
			self.life_color = YELLOW
		if self.hit <= 3:
			self.life_color = RED
		if self.hit <= 0:
			self.remove(self.game.all_sprites)
			self.kill()

class Stairs(pygame.sprite.Sprite):
	def __init__(self, game, x, y, offset, floor):
		self.game = game 
		self._layer = BLOCK_LAYER
		self.floor = floor

		self.groups = self.game.all_sprites, self.game.stairs
		pygame.sprite.Sprite.__init__(self, self.groups)

		self.x = x * TILE_SIZE * SCALE + offset[0]
		self.y = y * TILE_SIZE * SCALE + offset[1]
		self.width = TILE_SIZE
		self.height = TILE_SIZE

		self.image = pygame.transform.scale(self.game.wall_spritesheet.collection[3][1], 
			(self.width*SCALE,self.height*SCALE))

		self.rect = self.image.get_rect()
		self.rect.x = self.x 
		self.rect.y = self.y

		self.prior_interval = pygame.time.get_ticks()

	def traverse(self):
		x_val = 1000
		y_val = 1000  

		blocks = self.game.blocks.sprites()
		enemies = self.game.enemies.sprites()
		stairs = self.game.stairs.sprites()

		for b in blocks:
			if b.rect.x < x_val:
				x_val = b.rect.x
				if b.rect.y < y_val:
					y_val = b.rect.y 
			b.remove(self.game.all_sprites)
			b.kill()
		for e in enemies:
			e.remove(self.game.all_sprites)
			e.kill()

		if(self.floor == 0):
			self.floor = 1
		else:
			self.floor = 0

		self.game.create_tile_map(LEVELS[self.game.level][self.floor], self.floor, (x_val, y_val))

		for s in stairs:
			s.remove(self.game.all_sprites)
			s.kill()

	def update(self):
		keys = pygame.key.get_pressed()

		player_collision = pygame.sprite.spritecollide(self, self.game.players, False)

		if keys[pygame.K_RETURN]:
			now = pygame.time.get_ticks()
			if ((now - self.prior_interval) >= 1000):
				self.prior_interval = pygame.time.get_ticks()
				if player_collision:
					self.traverse()

class Gates(pygame.sprite.Sprite):
	def __init__(self, game, x, y, offset):
		self.game = game 
		self._layer = BLOCK_LAYER

		self.groups = self.game.all_sprites, self.game.gates
		pygame.sprite.Sprite.__init__(self, self.groups)

		self.x = x * TILE_SIZE * SCALE + offset[0]
		self.y = y * TILE_SIZE * SCALE + offset[1]
		self.width = TILE_SIZE
		self.height = TILE_SIZE

		self.image = pygame.transform.scale(self.game.wall_spritesheet.collection[3][1], 
			(self.width*SCALE,self.height*SCALE))

		self.rect = self.image.get_rect()
		self.rect.x = self.x 
		self.rect.y = self.y

		self.prior_interval = pygame.time.get_ticks()

	def traverse(self):

		blocks = self.game.blocks.sprites()
		enemies = self.game.enemies.sprites()
		stairs = self.game.stairs.sprites()
		gates = self.game.gates.sprites()
		player = self.game.players.sprites()

		for b in blocks:
			b.remove(self.game.blocks)
			b.remove(self.game.all_sprites)
			b.kill()
		for e in enemies:
			e.remove(self.game.all_sprites)
			e.remove(self.game.enemies)
			e.kill()
		for s in stairs:
			s.remove(self.game.all_sprites)
			s.remove(self.game.stairs)
			s.kill()
		for p in player:
			p.remove(self.game.all_sprites)
			p.remove(self.game.players)
			p.kill()

		if self.game.level == 0:
			self.game.wall_spritesheet = Spritesheet('img/Thanksgiving_Wall_Sheet.png', 4, 4, 32, [4,4,4,4], 0)
			self.game.enemy_spritesheet = Spritesheet('img/Thanksgiving_Enemy_Sheet.png', 6, 5, 32, [4, 3, 4, 4, 5, 5, 5], 4)
		if self.game.level == 1:
			self.game.wall_spritesheet = Spritesheet('img/Christmas_Wall_Sheet.png', 4, 4, 32, [4,4,4,4], 0)
		if self.game.level == 2:
			self.game.playing = False
			return

		self.game.level += 1

		self.game.create_tile_map(LEVELS[self.game.level][0], 0, (0,0))

		for g in gates:
			g.remove(self.game.all_sprites)
			g.remove(self.game.gates)
			g.kill()

	def update(self):
		now = pygame.time.get_ticks()
		if ((now - self.prior_interval) >= 1000):
			self.prior_interval = pygame.time.get_ticks()
			player_collision = pygame.sprite.spritecollide(self, self.game.players, False)

			if player_collision:
				self.traverse()


class Block(pygame.sprite.Sprite):
	def __init__(self, game, x, y, block_d, offset):
		self.game = game 
		self._layer = BLOCK_LAYER

		self.groups = self.game.all_sprites, self.game.blocks
		pygame.sprite.Sprite.__init__(self, self.groups)

		self.x = x * TILE_SIZE * SCALE + offset[0]
		self.y = y * TILE_SIZE * SCALE + offset[1]
		self.width = TILE_SIZE
		self.height = TILE_SIZE

		self.image = pygame.transform.scale(self.set_img(block_d), (self.width*SCALE,self.height*SCALE))

		self.rect = self.image.get_rect()
		self.rect.x = self.x 
		self.rect.y = self.y 

	def set_img(self, block_d):
		if block_d == 'TOP':
			return self.game.wall_spritesheet.collection[1][1]
		if block_d == 'UPPERRIGHT':
			return self.game.wall_spritesheet.collection[2][0]
		if block_d == 'UPPERLEFT':
			return self.game.wall_spritesheet.collection[2][1]
		if block_d == 'LOWERRIGHT':
			return self.game.wall_spritesheet.collection[2][3]
		if block_d == 'LOWERLEFT':
			return self.game.wall_spritesheet.collection[2][2]
		if block_d == 'RIGHT':
			return self.game.wall_spritesheet.collection[1][0]
		if block_d == 'LEFT':
			return self.game.wall_spritesheet.collection[1][2]
		if block_d == 'BOTTOM':
			return self.game.wall_spritesheet.collection[1][3]
		if block_d == 'WALL':
			return self.game.wall_spritesheet.collection[3][0]

class Enemy(pygame.sprite.Sprite):
	def __init__(self, game, x, y, offset):
		self.game = game
		self._layer = PLAYER_LAYER
		self.groups = self.game.all_sprites, self.game.enemies
		pygame.sprite.Sprite.__init__(self, self.groups)

		self.x = x*TILE_SIZE*SCALE + offset[0]
		self.y = y*TILE_SIZE*SCALE + offset[1]
		self.width = TILE_SIZE
		self.height = TILE_SIZE

		self.dx = 0
		self.dy = 0

		self.facing = 'down'

		self.image = pygame.transform.scale(self.game.enemy_spritesheet.collection[0][0], 
			(self.width*SCALE,self.height*SCALE))

		self.rect = self.image.get_rect()
		self.rect.x = self.x
		self.rect.y = self.y

		self.char_step = 0;
		self.set_length = 2
		self.last = pygame.time.get_ticks()
		self.prior_interval = pygame.time.get_ticks()
		self.direc = 0
		self.travel_len = 10
		self.curr_step = 0
		self.hit = 10
		self.life_color = GREEN

	def update(self):
		now = pygame.time.get_ticks()
		self.image = pygame.transform.scale(self.set_img(), 
			(self.width*SCALE,self.height*SCALE))

		if now - self.prior_interval >= 50:
			self.prior_interval = pygame.time.get_ticks()
			self.movement()

		self.rect.x += self.dx
		self.rect.y += self.dy 

		block_collision = pygame.sprite.spritecollide(self, self.game.blocks, False)
		enemy_collision = pygame.sprite.spritecollide(self, self.game.players, False)

		if(block_collision or enemy_collision):
			self.rect.x -= BOUNCE_BACK * self.dx
			self.rect.y -= BOUNCE_BACK * self.dy
		if(enemy_collision):
			for e in enemy_collision:
				e.rect.x += BOUNCE_BACK * self.dx
				e.rect.y += BOUNCE_BACK * self.dy
				e.dock_health()
		self.dx = 0
		self.dy = 0

	def movement(self):
		if self.char_step >= self.set_length :
			self.char_step = 0

		if self.travel_len <= self.curr_step:
			self.travel_len = random.randint(0,100)
			self.curr_step = 0
			self.char_step = 0
			self.direc = random.randint(0,len(self.game.enemy_spritesheet.set_list)-1)
			self.set_length = self.game.enemy_spritesheet.set_list[self.direc]-1

		# Movement controls
		if self.direc == 6:
			self.dx -= PLAYER_SPEED
			self.facing = 'left'
		if self.direc == 4:
			self.dx += PLAYER_SPEED
			self.facing = 'right'
		if self.direc == 5:
			self.dy -= PLAYER_SPEED
			self.facing = 'up'
		if self.direc == 0:
			self.dy += PLAYER_SPEED
			self.facing = 'down'
		if self.direc == 1:
			self.facing = 'stare'
		if self.direc == 2:
			self.facing = 'stare'
		if self.direc == 3:
			self.facing = 'stare'

		self.char_step += 1
		self.curr_step += 1

		if self.direc == 7:
			now = pygame.time.get_ticks()
			if now - self.last >= 100:
				Projectile(self.game, self.rect.x, self.rect.y, self.facing, WHITE)
				self.last = pygame.time.get_ticks()
				self.char_step = self.set_length
				self.curr_step = self.travel_len

	def set_img(self):
		if self.facing == 'right':
			img = self.game.enemy_spritesheet.collection[4][self.char_step]
		if self.facing == 'left':
			img = self.game.enemy_spritesheet.collection[6][self.char_step]
		if self.facing == 'up':
			img = self.game.enemy_spritesheet.collection[5][self.char_step]
		if self.facing == 'down':
			img = self.game.enemy_spritesheet.collection[0][self.char_step]
		if self.facing == 'stare':
			img = self.game.enemy_spritesheet.collection[self.direc][self.char_step]

		pygame.draw.rect(img, BLACK, pygame.Rect(0, 0, 32, 4)) # NEW
		pygame.draw.rect(img, self.life_color, pygame.Rect(1, 1, 30 - (3 * (10 - self.hit)), 2)) # NEW
		pygame.draw.rect(img, WHITE, pygame.Rect(0, 0, 32, 4), 1) # NEW

		return img

	def tally_hit(self):
		self.hit -= 1
		if self.hit <= 5:
			self.life_color = YELLOW
		if self.hit <= 3:
			self.life_color = RED
		if self.hit <= 0:
			self.remove(self.game.all_sprites)
			self.kill()
		
class Button:
	def __init__(self, x, y, width, height, fg, bg, content, fontsize):
		self.font = pygame.font.Font('Arial.ttf', fontsize)
		self.content = content 
		self.x = x 
		self.y = y 
		self.width = width
		self.height = height
		self.fg = fg 
		self.bg = bg 

		self.image = pygame.Surface((self.width, self.height))
		self.image.fill(self.bg)
		self.rect = self.image.get_rect()

		self.rect.x = self.x 
		self.rect.y = self.y 

		self.text = self.font.render(self.content, True, self.fg)
		self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))
		self.image.blit(self.text, self.text_rect)

	def is_pressed(self, pos, pressed):
		if self.rect.collidepoint(pos):
			if pressed[0]:
				return True
			return False
		return False
