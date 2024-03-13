import pygame

# Inits.
pygame.init()
pygame.mixer.init()
pygame.font.init()

# Essentials.
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 800
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
CLOCK = pygame.time.Clock()
DATA_FILE_PATH = "./data.json"

# Assets.
SFX_DIE = pygame.mixer.Sound("./assets/audio/die.wav")
SFX_HIT = pygame.mixer.Sound("./assets/audio/hit.wav")
SFX_POINT = pygame.mixer.Sound("./assets/audio/point.wav")
SFX_SWOOSH = pygame.mixer.Sound("./assets/audio/swoosh.wav")
SFX_WING = pygame.mixer.Sound("./assets/audio/wing.wav")
HEADING = pygame.font.Font("./assets/fonts/FlappyBirdRegular-9Pq0.ttf", 60)
HEADING.set_bold(True)
BODY = pygame.font.Font("./assets/fonts/FlappyBirdRegular-9Pq0.ttf", 30)
ICON = pygame.image.load("./assets/icons/icon.ico").convert_alpha()
BACKGROUND = pygame.image.load(
    "./assets/sprites/backgrounds/background-day.png"
).convert()
GROUND = pygame.image.load("./assets/sprites/miscs/base.png").convert()

# Gameplay.
FPS = 60
GRAVITY_VEL = 0.5
GROUND_VEL = 4
GROUND_Y = SCREEN_HEIGHT / (4 / 3)
PLAYER_FLAP_GRAVITY = -8
PLAYER_TRANSFORM_SCALE = 1.75
PLAYER_FLAP_COOLDOWN = 100
PLAYER_CENTER_X = SCREEN_WIDTH / 4
PLAYER_FLOATING_VEL = 1
GAP_HEIGHT = SCREEN_HEIGHT / 6
PIPE_WIDTH = SCREEN_WIDTH / 8
SPAWN_PIPE_INTERVAL = 1000

# Events.
PLAYER_COLLIDED_WITH_PIPE = pygame.USEREVENT + 1
PLAYER_COLLIDED_WITH_GROUND = pygame.USEREVENT + 2
SPAWN_PIPE = pygame.USEREVENT + 3
SCORE_INCREMENT = pygame.USEREVENT + 4
