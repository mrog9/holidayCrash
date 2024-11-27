SCALE = 2 						# How to scale the game to render it larger on the screen

WIN_WIDTH = 640 * SCALE			# Width of the game window
WIN_HEIGHT = 480 * SCALE		# Height of the game window

TILE_SIZE = 32					# Size in pixels of the sprite tiles
PROJ_SIZE = 6 					# Size in pixels of the 'bullets' the player fires

# Game layers of each class of objects
PROJECTILE_LAYER = 4
TURF_LAYER = 3
PLAYER_LAYER = 2
BLOCK_LAYER = 1

# Default colors represented as a tuple (r,g,b)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
BLACK = (0,0,0)
WHITE = (255,255,255)

# The number of iterations to run per second for the main game loop
FPS = 60

# Game object default speeds
PLAYER_SPEED = 4
PROJ_SPEED = 6
BOUNCE_BACK = 4

# Game level and floor mappings to be fed to the tilemap function in main.py
HALLOWEEN_MAIN = [
	'UTTTTTTTTTTTTTTTTTTC',
	'L..................R',
	'LWWWWW.............R',
	'L....W........S....R',
	'L....W.............R',
	'L....WWWW..........R',
	'L..................R',
	'L..................R',
	'L.......WW...E.....R',
	'L.........W........R',
	'L..E......W........R',
	'L..........WWWWWW..R',
	'L..S.............WWR',
	'L..................R',
	'L..................R',
	'MBBBBBBBBGGBBBBBBBBF',
]

HALLOWEEN_BASEMENT = [
	'UTTTTTTTTTTTTTTTTTTC',
	'L..W...............R',
	'L...W..............R',
	'L....W........S....R',
	'L....W.............R',
	'L..................R',
	'L..................R',
	'L.......W..........R',
	'L.......WW...E.....R',
	'L.........W........R',
	'L..E......W........R',
	'L..................R',
	'L..S...............R',
	'L..................R',
	'L..................R',
	'MBBBBBBBBBBBBBBBBBBF',
]

THANKSGIVING_MAIN = [
	'UTTTTTTTTTTTTTTTTTTC',
	'L.........S..W.....R',
	'L.S..........W.....R',
	'L..........WWW..S..R',
	'LWWWWW.....W.......R',
	'L....WWWWWWW.......R',
	'L.......W..........R',
	'L.......W..........R',
	'L.......WW...E.....R',
	'L.........W........R',
	'L..E......W........R',
	'L..........WWWWWWS.R',
	'L..S.............WWR',
	'L..................R',
	'L..................R',
	'MBBBBBBBBGGBBBBBBBBF',
]

THANKSGIVING_BASEMENT = [
	'UTTTTTTTTTTTTTTTTTTC',
	'L...W.....S........R',
	'L.S.W..............R',
	'L....W..........S..R',
	'L....W.............R',
	'L....WWWWWWWWWWWWWWR',
	'L..................R',
	'L.......W..........R',
	'L.......WW...E.....R',
	'L.........W........R',
	'L..E......W........R',
	'L................S.R',
	'L..S...............R',
	'L..................R',
	'L..................R',
	'MBBBBBBBBBBBBBBBBBBF',
]

CHRISTMAS_MAIN = [
	'UTTTTTTTTTTTTTTTTTTC',
	'L.........S..W.....R',
	'LWWWWW.......W.....R',
	'L....W.....WWW..S..R',
	'L....W.....W.......R',
	'L....WWWWWWW.......R',
	'L.......W......S...R',
	'L.......W..........R',
	'L.......WW...E.....R',
	'L.........W........R',
	'L..E......W......S.R',
	'L..........W.......R',
	'L..S.......W...S...R',
	'L..........W.......R',
	'L...........W......R',
	'MBBBBBBBBGGBBBBBBBBF',
]

CHRISTMAS_BASEMENT = [
	'UTTTTTTTTTTTTTTTTTTC',
	'L...W.....S........R',
	'L...W..............R',
	'L....W..........S..R',
	'L....W.............R',
	'L....WWWWWWWWWWWWWWR',
	'L...........W..S...R',
	'L...........W......R',
	'L.......W...WE.....R',
	'L........W...WWWWWWR',
	'L..E.....W.........R',
	'L.........W.E......R',
	'L..S......W....S...R',
	'L.........W........R',
	'L.........W........R',
	'MBBBBBBBBBBBBBBBBBBF',
]

# How each level and floor is represented in a global list
HALLOWEEN_LEVELS = [HALLOWEEN_MAIN, HALLOWEEN_BASEMENT]
THANKSGIVING_LEVELS = [THANKSGIVING_MAIN, THANKSGIVING_BASEMENT]
CHRISTMAS_LEVELS = [CHRISTMAS_MAIN, CHRISTMAS_BASEMENT]

LEVELS = [HALLOWEEN_LEVELS, THANKSGIVING_LEVELS, CHRISTMAS_LEVELS]