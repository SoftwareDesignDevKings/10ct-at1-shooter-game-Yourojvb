# app.py
import pygame
import os

# --------------------------------------------------------------------------
#                               CONSTANTS
# --------------------------------------------------------------------------

WIDTH = 800
HEIGHT = 600
FPS = 60

PLAYER_SPEED = 3
DEFAULT_ENEMY_SPEED = 1

SPAWN_MARGIN = 50

ENEMY_SCALE_FACTOR = 2
PLAYER_SCALE_FACTOR = 2
FLOOR_TILE_SCALE_FACTOR = 2
HEALTH_SCALE_FACTOR = 3

PUSHBACK_DISTANCE = 200
ENEMY_KNOCKBACK_SPEED = 20

# --------------------------------------------------------------------------
#                       ASSET LOADING FUNCTIONS
# --------------------------------------------------------------------------

def load_frames(prefix, frame_count, scale_factor=1, folder="assets"):
    frames = []
    for i in range(frame_count):
        image_path = os.path.join(folder, f"{prefix}_{i}.png") #prefix is file names; 
        #this is getting the picture
        img = pygame.image.load(image_path).convert_alpha()

        if scale_factor != 1:
            w = img.get_width() * scale_factor #re-scales the img
            h = img.get_height() * scale_factor
            img = pygame.transform.scale(img, (w, h)) #re-scaled img

        frames.append(img)
    return frames

def load_floor_tiles(folder="assets"):
    floor_tiles = [] #creates empty list
    for i in range(8):
        path = os.path.join(folder, f"floor_{i}.png") #goes through the pre-determined imges
        tile = pygame.image.load(path).convert()

        if FLOOR_TILE_SCALE_FACTOR != 1: #if the scale isnt one
            tw = tile.get_width() * FLOOR_TILE_SCALE_FACTOR
            th = tile.get_height() * FLOOR_TILE_SCALE_FACTOR
            tile = pygame.transform.scale(tile, (tw, th))

        floor_tiles.append(tile) #brings it into the list of floor tiles
    return floor_tiles

def load_assets():
    assets = {}

    # Enemies
    assets["enemies"] = {
        "orc":  load_frames("orc",    4, scale_factor=ENEMY_SCALE_FACTOR),
        "undead": load_frames("undead", 4, scale_factor=ENEMY_SCALE_FACTOR),
        "demon":  load_frames("demon",  4, scale_factor=ENEMY_SCALE_FACTOR),
        "frame": load_frames("frame", 10, scale_factor=0.25), #new enemy type 
        
    }

    # Player
    assets["player"] = {
        "idle": load_frames("player_idle", 4, scale_factor=PLAYER_SCALE_FACTOR),
        "run":  load_frames("player_run",  4, scale_factor=PLAYER_SCALE_FACTOR),
    }

    # Floor tiles
    assets["floor_tiles"] = load_floor_tiles()



    # Health images
    assets["health"] = load_frames("health", 6, scale_factor=HEALTH_SCALE_FACTOR)

    return assets