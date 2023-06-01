import os
TICK = round(1000 / 60)  # Frame rate in milliseconds

FIELD_WIDTH = 600       # main window width and height
FIELD_HEIGHT = 700

PLAYER_WIDTH = 50
PLAYER_HEIGHT = 30
FLOOR_SIZE = 10         # bottom zone size

DEFAULT_ENEMIES_NUMBER = 10

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))
IMAGES_DIR = os.path.join(PROJECT_DIR, 'images')                # local path to images
SCORES_DIR_NAME = os.path.join(PROJECT_DIR ,"topscores.txt")    # path to scores file
DATA_DIR_NAME = os.path.join(PROJECT_DIR, 'game.txt')    # path to data file


ENEMY_IMAGE_LIGHT = 'light_alien.png'       # setting images names
ENEMY_IMAGE_MEDIUM = 'medium_alien.png'
ENEMY_IMAGE_HEAVY = 'heavy_alien.png'
ENEMY_IMAGE_BOSS = 'boss.png'
PLAYER1_IMAGE = 'ship-red-39x30.png'
PLAYER2_IMAGE = 'ship-purple-39x30.png'

