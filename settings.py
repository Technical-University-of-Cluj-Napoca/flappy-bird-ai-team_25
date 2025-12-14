import os

SCREEN_WIDTH = 576
SCREEN_HEIGHT = 800
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (0, 128, 255) 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')

BG_IMAGE = os.path.join(ASSETS_DIR, 'day.png')
GROUND_IMAGE = os.path.join(ASSETS_DIR, 'ground.png')
TITLE_IMAGE = os.path.join(ASSETS_DIR, 'title.png')
BIRD_IMAGES = [
    os.path.join(ASSETS_DIR, 'bird1.png'),
    os.path.join(ASSETS_DIR, 'bird2.png'),
    os.path.join(ASSETS_DIR, 'bird3.png'),
    os.path.join(ASSETS_DIR, 'bird4.png'),
    os.path.join(ASSETS_DIR, 'bird5.png'),
    os.path.join(ASSETS_DIR, 'bird6.png')
]

BTN_MANUAL = os.path.join(ASSETS_DIR, 'manual_btn.png')
BTN_AUTO = os.path.join(ASSETS_DIR, 'auto_btn.png')
BTN_START = os.path.join(ASSETS_DIR, 'start_btn.png')
BTN_HIGHSCORE = os.path.join(ASSETS_DIR, 'highscore_btn.png')
BTN_TOP3 = os.path.join(ASSETS_DIR, 'high_btn.png')
BTN_BACK = os.path.join(ASSETS_DIR, 'back_btn.png')

GET_READY_IMAGE = os.path.join(ASSETS_DIR, 'get_ready.png')
TUTORIAL_TAP = os.path.join(ASSETS_DIR, 'tap_tut.png')
TUTORIAL_AUTO = os.path.join(ASSETS_DIR, 'auto_tut.jpg')
GAME_OVER_IMAGE = os.path.join(ASSETS_DIR, 'game_over.png')

PIPE_TOP = os.path.join(ASSETS_DIR, 'pipe_top.png')
PIPE_BOTTOM = os.path.join(ASSETS_DIR, 'pipe_bottom.png')

MEDAL_BRONZE = os.path.join(ASSETS_DIR, 'bronze_medal.png')
MEDAL_SILVER = os.path.join(ASSETS_DIR, 'silver_medal.png')
MEDAL_GOLD = os.path.join(ASSETS_DIR, 'gold_medal.png')
MEDAL_PLATINUM = os.path.join(ASSETS_DIR, 'platinum_medal.png')

POPUP_SCORE = os.path.join(ASSETS_DIR, 'medal_score.png') 


GRAVITY = 0.25
BIRD_MOVEMENT = 0
SCROLL_SPEED = 4
JUMP_STRENGTH = -6
PIPE_GAP = 160
PIPE_FREQUENCY = 1500 


COPYRIGHT_TEXT = "Copyright (c) Team25 <3 :D"

FONT_PATH = os.path.join(ASSETS_DIR, 'ByteBounce.ttf')
