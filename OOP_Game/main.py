import pygame
from sprites import *
from config import *
import sys

class Game:
	def __init__(self):
		##########################################################################################################
		# __init__ - function that instantiates the primary values that will remain unchanged throughout the game
		##########################################################################################################
		pygame.init()
		self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))			# Instantiate the main screen
		self.clock = pygame.time.Clock()										# Start the game clock
		
		self.font_1 = pygame.font.Font('Arial.ttf', 32)							# Set a font size, file is in the main folder of the project
		self.font_2 = pygame.font.Font('Arial.ttf', 48)							# Same font as ^ but a different size

		# Instantiation of the graphics, the Spritesheet class is custom and defined in sprites.py
		# however this is where all of the pixel images are pulled from for the animations and terrain
		self.character_spritesheet = Spritesheet('img/Char_Sheet.png', 5, 3, 32, [3,3,3,3,3], 4)
		self.wall_spritesheet = Spritesheet('img/Halloween_Wall_Sheet.png', 4, 4, 32, [4,4,4,4], 0)
		self.enemy_spritesheet = Spritesheet('img/Halloween_Enemy_Sheet.png', 7, 6, 32, [4, 9, 6, 7, 5, 5, 5], 4)

		# I'm not sure why this is loaded here, should be in the intro screen function
		self.intro_background = pygame.image.load('img/background_image.png')

		# Set the game to a running state
		self.running = True

		# Define the starting level
		# The level variable has to be defined at this level as the level change wipes 
		# any values that might be stored by the other classes, with the only exception
		# being the player class
		self.level = 0


		self.isIncremented = False

	def update_level(self):
		#############################################################
		# update_level - Currently unused way to set the floor level
		#############################################################
		self.level += 1

	def create_tile_map(self, tile_map, floor, offset, levelchange):
		####################################################################################################################
		# create_tile_map - Creates the necessary sprite objects for a floor/level based on the tilemappings in config.py
		#	tile_map 		: A list of a list of chars that define the floor/level layout
		#	floor 			: The current floor the player is playing on
		#	offset			: A tuple (x,y) representing the rendering offsets based on player position
		#	levelchange		: A boolean indicating if this function is being called by stairs or a gate
		####################################################################################################################
		for i, row in enumerate(tile_map):
			for j, column in enumerate(row):
				if column == "B":
					Block(self, j, i, 'BOTTOM', offset)
				if column == "U":
					Block(self, j, i, 'UPPERLEFT', offset)
				if column == "T":
					Block(self, j, i, 'TOP', offset)
				if column == "C":
					Block(self, j, i, 'UPPERRIGHT', offset)
				if column == "R":
					Block(self, j, i, 'RIGHT', offset)
				if column == "L":
					Block(self, j, i, 'LEFT', offset)
				if column == "M":
					Block(self, j, i, 'LOWERLEFT', offset)
				if column == "F":
					Block(self, j, i, 'LOWERRIGHT', offset)
				if column == "W":
					Block(self, j, i, 'WALL', offset)
				if column == ".":
					Block(self, j, i, 'FLOOR', offset)
				if column == "E":
					Enemy(self, j, i, offset)
					Block(self, j, i, 'FLOOR', offset)
				if column == "S":
					Stairs(self, j, i, offset, floor)
				if column == "G":
					Gates(self, j, i, offset)

		if(levelchange):
			Block(self, 6, 4, 'FLOOR', offset)		
			self.players.sprites()[0].rect.x = 6*TILE_SIZE*SCALE
			self.players.sprites()[0].rect.y = 4*TILE_SIZE*SCALE
		if not self.players.sprites():	
			Block(self, 6, 4, 'FLOOR', offset)		
			Player(self, 6, 4)

	def new(self):
		#############################
		# new - Starts a new game
		#############################
		self.playing = True

		# Start the music
		self.background_music = pygame.mixer.Sound('audio/background_music.wav')
		self.background_music.play(-1)
		self.background_music.set_volume(0.5)

		# Sprite Groupings
		self.all_sprites = pygame.sprite.LayeredUpdates()
		self.players = pygame.sprite.LayeredUpdates()
		self.blocks = pygame.sprite.LayeredUpdates()
		self.enemies = pygame.sprite.LayeredUpdates()
		self.attacks = pygame.sprite.LayeredUpdates()
		self.stairs = pygame.sprite.LayeredUpdates()
		self.gates = pygame.sprite.LayeredUpdates()
		self.floors = pygame.sprite.LayeredUpdates()

		# Create the first level map
		self.create_tile_map(LEVELS[0][0], 0, (0,0), False)

	def events(self):
		#####################################################################################################
		# events - handle any event signals that pygame puts out, like a request by the user to end the game
		#####################################################################################################
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.playing = False
				self.running = False		

	def updates(self):
		##################################################################################################################
		# updates - called cyclically in the main function loop and calls all active sprites to run their update methods
		##################################################################################################################
		self.all_sprites.update()
		pygame.display.flip()

	def draw(self):
		###################################################################
		# draw - renders the screen background and updates the scoreboard
		###################################################################
		self.screen.fill(BLACK)
		self.all_sprites.draw(self.screen)

		border = pygame.Surface((400,100))
		border_rect = border.get_rect()
		border_rect.center = (WIN_WIDTH - 210, 60)

		score = self.font_2.render("Score: " + str(self.players.sprites()[0].score), True, BLACK)
		score_rect = score.get_rect(centerx=border_rect.centerx, centery=border_rect.centery)

		pygame.draw.rect(self.screen, WHITE, border_rect, 0, 20)
		pygame.draw.rect(self.screen, BLACK, border_rect, 3, 20)
		self.screen.blit(score, score_rect)

		self.clock.tick(FPS)
		pygame.display.update()

	def main(self):
		############################################################################
		# main - The main loop that runs until the playing variable is set to False
		############################################################################
		while self.playing:
			self.events()
			self.updates()
			self.draw()

		# Once playing is set to false, the loop finishes it's current execution loop then flows to setting the running
		#	variable to false, breaking out of the containing loop in the main loop
		self.running = False

	def game_over(self):
		####################################################################################################
		# game_over - A function called when the game breaks from the main function loop
		#				It renders the final score screen, pauses for 5 seconds, then kills the application
		####################################################################################################
		self.background_music.stop()
		gg = True
		border = pygame.Surface((600,500))
		border_rect = border.get_rect()
		border_rect.center = (WIN_WIDTH/2, WIN_HEIGHT/2)
		score = self.font_2.render("Final Score: " + str(self.players.sprites()[0].score), True, BLACK)
		score_rect = score.get_rect(centerx=border_rect.centerx, centery=border_rect.centery)
		prior_interval = pygame.time.get_ticks()

		while gg:
			now = pygame.time.get_ticks()
			self.screen.blit(pygame.transform.scale(self.intro_background, (WIN_WIDTH, WIN_HEIGHT)), (0,0))
			pygame.draw.rect(self.screen, BLACK, border_rect, 3, 20)
			self.screen.blit(score, score_rect)
			pygame.display.update()
			if now - prior_interval >= 5000:
				gg = False

	def intro_screen(self):
		#############################################################################################
		# intro_screen - Renders the intro screen then loops indefinitely until the player press the 
		#					start button
		#############################################################################################
		intro = True

		border = pygame.Surface((600,500))
		border_rect = border.get_rect()
		border_rect.center = (WIN_WIDTH/2, WIN_HEIGHT/2)
		
		
		title = self.font_2.render('Holiday Crash', True, BLACK)
		title_rect = title.get_rect(centerx=WIN_WIDTH/2, centery=WIN_HEIGHT/2-50)
		
		play_button = Button(WIN_WIDTH/2, WIN_HEIGHT/2+40, 100, 50, WHITE, BLACK, 'Play', 32)

		while intro:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					intro = False
					self.running = False

			mouse_pos = pygame.mouse.get_pos()
			mouse_pressed = pygame.mouse.get_pressed()

			if play_button.is_pressed(mouse_pos, mouse_pressed):
				intro = False

			self.screen.blit(pygame.transform.scale(self.intro_background, (WIN_WIDTH, WIN_HEIGHT)), (0,0))
			pygame.draw.rect(self.screen, BLACK, border_rect, 3, 20)
			self.screen.blit(title, title_rect)
			self.screen.blit(play_button.image, play_button.rect)
			
			self.clock.tick(FPS)
			pygame.display.update()

	def getSetting(self):
		self.surface = pygame.Surface((WIN_WIDTH,100))
		self.surface.fill((255,165,0))
		self.screen.blit(self.surface, (0,500))
		return self.screen



##########################################
# THIS IS THE START AND OVERHEAD CONTROL #
#          OF THE WHOLE GAME             #
##########################################
g = Game()          # Calls __init__ function
g.intro_screen()    # Sets up the intro screen loop and button detection
g.new()             # The start of the main game sequence

##########################################
# This section will loop indefinitely    #
# until the end condition is reached or  #
# the player dies.                       #
##########################################
while g.running:
	g.main()		# The main game loop
	g.game_over()   # Control flows to this once playing == False

pygame.quit()
sys.exit()

