import pygame
from sprites import *
from config import *
import sys

class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
		self.clock = pygame.time.Clock()
		
		self.font_1 = pygame.font.Font('alexsFinalVersion/OOP_Game/Arial.ttf', 32)
		self.font_2 = pygame.font.Font('alexsFinalVersion/OOP_Game/Arial.ttf', 48)

		self.character_spritesheet = Spritesheet('alexsFinalVersion/OOP_Game/img/Char_Sheet.png', 5, 3, 32, [3,3,3,3,3], 4)
		self.wall_spritesheet = Spritesheet('alexsFinalVersion/OOP_Game/img/Halloween_Wall_Sheet.png', 4, 4, 32, [4,4,4,4], 0)
		self.enemy_spritesheet = Spritesheet('alexsFinalVersion/OOP_Game/img/Halloween_Enemy_Sheet.png', 7, 6, 32, [4, 9, 6, 7, 5, 5, 5], 4)

		self.intro_background = pygame.image.load('alexsFinalVersion/OOP_Game/img/background_image.png')
		self.running = True
		self.level = 0
		self.isIncremented = False

	def update_level(self):
		self.level += 1

	def create_tile_map(self, tile_map, floor, offset, levelchange):
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
		# Start a new game
		self.playing = True

		# Sprite Groupings
		self.all_sprites = pygame.sprite.LayeredUpdates()
		self.players = pygame.sprite.LayeredUpdates()
		self.blocks = pygame.sprite.LayeredUpdates()
		self.enemies = pygame.sprite.LayeredUpdates()
		self.attacks = pygame.sprite.LayeredUpdates()
		self.stairs = pygame.sprite.LayeredUpdates()
		self.gates = pygame.sprite.LayeredUpdates()
		self.floors = pygame.sprite.LayeredUpdates()

		self.create_tile_map(LEVELS[0][0], 0, (0,0), False)

	def events(self):
		# game loop events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.playing = False
				self.running = False		

	def updates(self):
		# game loop updates
		self.all_sprites.update()
		pygame.display.flip()

	def draw(self):
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
		# Game Loop
		while self.playing:
			self.events()
			self.updates()
			self.draw()

		self.running = False

	def game_over(self):
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

g = Game()
g.intro_screen()
g.new()

while g.running:
	g.main()
	g.game_over()

pygame.quit()
sys.exit()

