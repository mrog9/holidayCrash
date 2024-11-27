import pygame
from config import *
import math
import random
from MattsBossLevelPart.Levels.runs.halloween_run import runHalloween
from MattsBossLevelPart.Levels.runs.thanksgiving_run import runThanksgiving
from MattsBossLevelPart.Levels.runs.christmans_run import runChristmas

# Spritesheet : A class that acts as a simplified way of interacting with the .png spritesheets
class Spritesheet:
	def __init__(self, file, rows, columns, tilesize, set_list, offset):
		#######################################################################################################################
		# __init__ - Instantiation fo the Spritesheet class
		# 	file : The .png file to read from that is composed of rows and columns of pixel images
		#	rows : The number of rows of images in this spritesheet
		# 	columns  : The number of columns of images in this spritesheet
		# 	tilesize : A number, in pixels, that define the square dimensions of each image
		#	set_list : This class reads in the images into a linear list from left to right, row by row, that then gets
		#			   further subdivided by this list of numbers defining how to group the images together in a sequence
		#              of animations for things like walking up, down, left, or right, or various actions that can be triggered
		#	offset   : A tuple (x,y) of how to offset new maps to the players position such as when traversing stairs but not
		#              changing levels
		#######################################################################################################################

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
		###############################################################################
		# get_sprites - returns the individual image requested from the spritesheet
		#	y      : The vertical position in pixels of the required image
		#	x      : The horizontal position in pixels of the required image
		#	width  : The width of the requested image
		#	height : The height of the requested image
		#	offset : A vertical offset for the health bar above the character
		###############################################################################

		sprite = pygame.Surface([width, height+offset])
		sprite.blit(self.sheet, (0,offset), (x, y, width, height))
		sprite.set_colorkey(BLACK)
		return sprite

# Projectile : An object representing the state of a 'bullet' that gets fired when you press the spacebar
class Projectile(pygame.sprite.Sprite):
	def __init__(self, game, x, y, direction, color):
		##############################################################################
		# __init__ - Instantiation and rendering of the Projectile object
		#	game      : A reference to the main game object instantiated in main.py
		#	x         : The x position in pixels of the player
		#	y    	  : The y position in pixels of the player
		#	direction : Which direction is the player facing, sent as a string
		#	color     : The individual color to render the projectile as
		##############################################################################
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
		###############################################################################
		# update - Since the class extends pygame.sprite.Sprite it needs to define
		#          this function that gets run cyclically when all sprites are called
		#          to be updated
		###############################################################################
		self.detect_collision()
		self.movement()

	def detect_collision(self):
		###########################################################################################
		# detect_collision - The logic to run when the projectile rect object overlaps the rect
		#                    object of another sprite
		###########################################################################################
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
		######################################################################################
		# movement - a method called from update that changes the position of the projectile
		######################################################################################
		self.rect.x += self.dx
		self.rect.y += self.dy			

# Player : A class representing the controllable player character, rendering it, tracking health, ect..
class Player(pygame.sprite.Sprite):
	def __init__(self, game, x, y):
		################################################################################################################
		# __init__ - Instantiate the default sprite object and call the parent constructor
		#	game   : The game object governing all of these classes and variables that need to persist between levels
		#	x      : The x position of the player on startup
		#	y      : The y position of the player on startup
		################################################################################################################
		self.game = game
		self._layer = PLAYER_LAYER
		self.groups = self.game.all_sprites, self.game.players
		pygame.sprite.Sprite.__init__(self, self.groups)

		# Load the audio file required for the collision sound
		self.bump_sound = pygame.mixer.Sound('audio/bump.wav')

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

		# timing variables to 'debounce' player inputs
		self.last_shot = pygame.time.get_ticks()
		self.last_bump = pygame.time.get_ticks()

		self.hit = 10 				# Number of hitpoints for the player
		self.life_color = GREEN		# Starting color of the health bar
		self.score = 0 				# Players score that persists through the game

	def update(self):
		###############################################################################
		# update - Since the class extends pygame.sprite.Sprite it needs to define
		#          this function that gets run cyclically when all sprites are called
		#          to be updated
		# NOTE : This function also updates the location of the other sprites in the 
		#			game so it appears that the player is in the same place
		###############################################################################
		self.movement()

		self.rect.x += self.dx
		self.rect.y += self.dy 

		# This section governs collisions with block sprites 
		#	and controlling the 'bounce back' from the enemy
		block_collision = pygame.sprite.spritecollide(self, self.game.blocks, False)

		if(block_collision):
			now = pygame.time.get_ticks()
			if now - self.last_bump > 500:
				self.bump_sound.play()
				self.last_bump = pygame.time.get_ticks()
			self.rect.x -= BOUNCE_BACK * self.dx
			self.rect.y -= BOUNCE_BACK * self.dy
			self.dx *= -(BOUNCE_BACK - 1) 
			self.dy *= -(BOUNCE_BACK - 1) 


		# This section governs collisions with enemy sprites and decrementing health
		#	and controlling the 'bounce back' from the enemy
		enemy_collision = pygame.sprite.spritecollide(self, self.game.enemies, False)

		if(enemy_collision):
			self.dock_health()
			self.rect.x -= BOUNCE_BACK * self.dx
			self.rect.y -= BOUNCE_BACK * self.dy
			self.dx *= -(BOUNCE_BACK - 1)  
			self.dy *= -(BOUNCE_BACK - 1) 

		# This section controls passing through a gate and updating the level of the
		#	game
		gate_collision = pygame.sprite.spritecollide(self, self.game.gates, False)

		if gate_collision:
			gate_collision[0].traverse()

		for sprite in self.game.all_sprites:
			sprite.rect.x -= self.dx
			sprite.rect.y -= self.dy

		self.dx = 0
		self.dy = 0

	def movement(self):
		##########################################################################
		# movement - Governs the players movement, updating the sprite image to 
		#	give the impression of animation, and updating the character position
		##########################################################################
		keys = pygame.key.get_pressed()

		if self.char_step >= self.set_length :
			self.char_step = 0

		self.image = pygame.transform.scale(self.set_img(), 
			(self.width*SCALE,self.height*SCALE))

		# Movement controls, picks up on multiple buttons being pressed and moving the 
		#	character along the diagonal and using the animation of the last button pressed
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
			if now - self.last_shot >= 100:
				Projectile(self.game, self.rect.x, self.rect.y, self.facing, BLACK)
				self.last_shot = pygame.time.get_ticks()

	def set_img(self):
		########################################################################
		# set_img - render the correct image taken from the player spritesheet
		########################################################################
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
		#########################################################################
		# dock_health - Updates the players health when it bumps into an enemy
		#			  - Also removes the player and ends the game when health
		#					decreases to zero
		#########################################################################
		self.hit -= 1
		if self.hit <= 5:
			self.life_color = YELLOW
		if self.hit <= 3:
			self.life_color = RED
		if self.hit <= 0:
			self.game.playing = False
			self.remove(self.game.all_sprites)
			self.kill()

# Stairs : The class controlling the special behavior of stairs and how they move 
#				the player from one floor to the next
class Stairs(pygame.sprite.Sprite):
	def __init__(self, game, x, y, offset, floor):
		#####################################################################################################################
		# __init__ - Instantiates the Stairs object when called and adds it to the sprite collection
		#	game 		: The game object governing all of these classes and variables that need to persist between levels
		#	x 			: The x position in pixels of the Stair sprite
		#	y 			: The y position in pixels of the Stair sprite
		#	offset		: The offset from the origin to instantiate the object at when rendering after a level change
		#	floor 		: The current floor the Stair sprite exists on
		#####################################################################################################################
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
		#######################################################################
		# traverse - Controls what happens when a player activates the stairs
		#				and updates the floor the player is on between main
		#				and basement floors
		#######################################################################
		x_val = 1000
		y_val = 1000  

		stairs = self.game.stairs.sprites()

		for b in self.game.blocks.sprites():
			if b.rect.x < x_val:
				x_val = b.rect.x
				if b.rect.y < y_val:
					y_val = b.rect.y 
			b.remove(self.game.all_sprites)
			b.remove(self.game.blocks)
			b.kill()
		for e in self.game.enemies:
			e.remove(self.game.all_sprites)
			e.remove(self.game.enemies)
			e.kill()
		for g in self.game.gates.sprites():
			g.remove(self.game.all_sprites)
			g.remove(self.game.gates)
			g.kill()
		for f in self.game.floors.sprites():
			f.remove(self.game.all_sprites)
			f.remove(self.game.floors)
			f.kill()

		if(self.floor == 0):
			self.floor = 1
		else:
			self.floor = 0

		self.game.create_tile_map(LEVELS[self.game.level][self.floor], self.floor, (x_val, y_val), False)

		for s in stairs:
			s.remove(self.game.all_sprites)
			s.remove(self.game.stairs)
			s.kill()

	def update(self):
		########################################################################################
		# update - Runs every frame of the game, and handles the keypress event for the stairs
		########################################################################################
		keys = pygame.key.get_pressed()

		player_collision = pygame.sprite.spritecollide(self, self.game.players, False)

		if keys[pygame.K_RETURN]:
			now = pygame.time.get_ticks()
			if ((now - self.prior_interval) >= 1000):
				self.prior_interval = pygame.time.get_ticks()
				if player_collision:
					self.traverse()

# Stairs : The class controlling the special behavior of gates and how they move 
#				the player from one level to the next
class Gates(pygame.sprite.Sprite):
	def __init__(self, game, x, y, offset):
		#####################################################################################################################
		# __init__ - Instantiates the Gates object when called and adds it to the sprite collection
		#	game 		: The game object governing all of these classes and variables that need to persist between floors
		#	x 			: The x position in pixels of the Gates sprite
		#	y 			: The y position in pixels of the Gates sprite
		#	offset		: The offset from the origin to instantiate the object at when rendering after a floor change
		#####################################################################################################################
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
		#######################################################################
		# traverse - Controls what happens when a player activates the gates
		#				and updates the level the player is on between the
		#				three levels, called by the player when a collision
		#				is detected
		#######################################################################
		gates = self.game.gates.sprites()

		for b in self.game.blocks.sprites():
			pygame.sprite.Group.remove(self.game.blocks, b)
			pygame.sprite.Group.remove(self.game.all_sprites, b)
			b.kill()
		for e in self.game.enemies.sprites():
			pygame.sprite.Group.remove(self.game.enemies, e)
			pygame.sprite.Group.remove(self.game.all_sprites, e)
			e.kill()
		for s in self.game.stairs.sprites():
			pygame.sprite.Group.remove(self.game.stairs, s)
			pygame.sprite.Group.remove(self.game.all_sprites, s)
			s.kill()
		for f in self.game.floors.sprites():
			f.remove(self.game.all_sprites)
			f.remove(self.game.players)
			f.kill()
		for g in gates:
			g.remove(self.game.all_sprites)
			g.remove(self.game.gates)
			g.kill()

		# Level updating code that checks the self.game.level variable and uses it to reset the sprite sheets for each level
		if self.game.level == 0:
			self.game.players.sprites()[0].score = runHalloween(self.game.players.sprites()[0].score, self.game)
			self.game.wall_spritesheet = Spritesheet('img/Thanksgiving_Wall_Sheet.png', 4, 4, 32, [4,4,4,4], 0)
			self.game.enemy_spritesheet = Spritesheet('img/Thanksgiving_Enemy_Sheet.png', 6, 5, 32, [4, 3, 4, 4, 5, 5, 5], 4)
		if self.game.level == 1:
			self.game.wall_spritesheet = Spritesheet('img/Christmas_Wall_Sheet.png', 4, 4, 32, [4,4,4,4], 0)
			self.game.enemy_spritesheet = Spritesheet('img/Christmas_Enemy_Sheet.png', 6, 5, 32, [4, 4, 5, 5, 4, 4, 4], 4)
		if self.game.level == 2:
			self.game.players.sprites()[0].score = runChristmas(self.game.players.sprites()[0].score, self.game)
			self.game.playing = False
			return

		# This was an attempt at 'thread safing' this section of code as when a player
		#	traverses a gate, there's never just one that gets activated, but two
		if not self.game.isIncremented:
			self.game.isIncremented = True
			self.game.level += 1
			self.game.create_tile_map(LEVELS[self.game.level][0], 0, (0,0), True)
		self.game.isIncremented = False

# Block : A class extending the pygame.sprite.Sprite class representing an impassible block
class Block(pygame.sprite.Sprite):
	def __init__(self, game, x, y, block_d, offset):
		#######################################################################################################################
		# __init__ - Instantiates the Block object when called and adds it to the sprite collection
		#	game 		: The game object governing all of these classes and variables for each block sprite
		#	x 			: The x position in pixels of the Block sprite
		#	y 			: The y position in pixels of the Block sprite
		#	block_d		: The block descriptor used to render the correct block image based on the level mapping in config.py
		#	offset		: The offset from the origin to instantiate the object at when rendering after a level change
		#######################################################################################################################
		self.game = game 
		self._layer = BLOCK_LAYER
		if block_d == 'FLOOR':
			self.groups = self.game.all_sprites, self.game.floors
		else:
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
		################################################################################
		# set_img - Sets the background image of the block based on the level mapping
		#	block_d : The descriptor of the block image to use for this instance
		################################################################################
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
		if block_d == 'FLOOR':
			return self.game.wall_spritesheet.collection[3][3]

# Enemy - A class extending pygame.sprite.Sprite that represents the enemies to present in the game
class Enemy(pygame.sprite.Sprite):
	def __init__(self, game, x, y, offset):
		################################################################################################################
		# __init__ - Instantiate the default sprite object and call the parent constructor
		#	game   : The game object governing all of these classes and variables that need to persist between levels
		#	x      : The x position of the enemy on startup
		#	y      : The y position of the enemy on startup
		#	offset : The offset tuple (x,y) to offset the enemy when creating an enemy
		################################################################################################################
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
		self.sprites = self.game.enemy_spritesheet

		self.image = pygame.transform.scale(self.sprites.collection[0][0], 
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
		###############################################################################
		# update - Since the class extends pygame.sprite.Sprite it needs to define
		#          this function that gets run cyclically when all sprites are called
		#          to be updated
		###############################################################################
		now = pygame.time.get_ticks()

		# Only execute the movement function every 50 milliseconds to keep the enemy
		#	from appearing to spaz out
		if now - self.prior_interval >= 50:
			self.prior_interval = pygame.time.get_ticks()
			self.movement()
			self.image = pygame.transform.scale(self.set_img(), 
				(self.width*SCALE,self.height*SCALE))

		self.rect.x += self.dx
		self.rect.y += self.dy 

		block_collision = pygame.sprite.spritecollide(self, self.game.blocks, False)
		enemy_collision = pygame.sprite.spritecollide(self, self.game.players, False)

		# handle collisions between enemies and blocks as well as enemies and players
		if(block_collision or enemy_collision):
			self.rect.x -= BOUNCE_BACK * self.dx
			self.rect.y -= BOUNCE_BACK * self.dy
		if(enemy_collision):
			for e in enemy_collision:
				e.rect.x += BOUNCE_BACK * self.dx
				e.rect.y += BOUNCE_BACK * self.dy
		self.dx = 0
		self.dy = 0

	def movement(self):
		####################################################################################
		# movement - Controls updating the sprite image of the enemy based on direction and 
		#				where the animation is in it's rendering
		####################################################################################
		if self.char_step >= self.set_length :
			self.char_step = 0

		if self.travel_len <= self.curr_step:
			self.travel_len = random.randint(0,100)
			self.curr_step = 0
			self.char_step = 0
			self.direc = random.randint(0,len(self.sprites.set_list)-1)
			self.set_length = self.sprites.set_list[self.direc]-1

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

		# A potential use case if the enemies can fire at the players, currently unused
		if self.direc == 7:
			now = pygame.time.get_ticks()
			if now - self.last >= 100:
				Projectile(self.game, self.rect.x, self.rect.y, self.facing, BLACK)
				self.last = pygame.time.get_ticks()
				self.char_step = self.set_length
				self.curr_step = self.travel_len

	def set_img(self):
		#################################################################################
		# set_image - Update the background image based on animation step and direction
		#################################################################################
		if self.facing == 'right':
			img = self.sprites.collection[4][self.char_step]
		if self.facing == 'left':
			img = self.sprites.collection[6][self.char_step]
		if self.facing == 'up':
			img = self.sprites.collection[5][self.char_step]
		if self.facing == 'down':
			img = self.sprites.collection[0][self.char_step]
		if self.facing == 'stare':
			img = self.sprites.collection[self.direc][self.char_step]

		# Update the health bar
		pygame.draw.rect(img, BLACK, pygame.Rect(0, 0, 32, 4)) # NEW
		pygame.draw.rect(img, self.life_color, pygame.Rect(1, 1, 30 - (3 * (10 - self.hit)), 2)) # NEW
		pygame.draw.rect(img, WHITE, pygame.Rect(0, 0, 32, 4), 1) # NEW

		return img

	def tally_hit(self):
		##################################################################################################
		# tally_hit - Called by an impacting Projectile object and handles decrementing the units health
		#				and disposing of the enemy object when it's health reaches 0
		##################################################################################################
		self.hit -= 1
		if self.hit <= 5:
			self.life_color = YELLOW
		if self.hit <= 3:
			self.life_color = RED
		if self.hit <= 0:
			self.game.players.sprites()[0].score += 10
			self.remove(self.game.all_sprites)
			self.kill()

# Button : A generic button class to handle the rendering and properties of a button in the game
class Button:
	def __init__(self, x, y, width, height, fg, bg, content, fontsize):
		################################################################################################################
		# __init__ - Instantiate the default sprite object and call the parent constructor
		#	x        : The x position of the button on startup
		#	y        : The y position of the button on startup
		#	width    : The width of the button
		#	height   : the height of the button
		#	fg       : Button foreground (text) color
		#	bg       : Color of the actual button square
		#	content  : What the button label says
		#	fontsize : The size of the font used on the button
		################################################################################################################
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

		self.rect.centerx = self.x 
		self.rect.centery = self.y 

		self.text = self.font.render(self.content, True, self.fg)
		self.text_rect = self.text.get_rect(center=(self.width/2, self.height/2))
		self.image.blit(self.text, self.text_rect)

	def is_pressed(self, pos, pressed):
		#######################################################
		# is_pressed - Handle the clicking event on the button
		#######################################################
		if self.rect.collidepoint(pos):
			if pressed[0]:
				return True
			return False
		return False
