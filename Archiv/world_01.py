import pygame
import random
from config import *

def generate_world():
    """Erstellt die Welt als 2D-Liste"""
    world = []
    for y in range(WORLD_HEIGHT):
        row = []
        for x in range(WORLD_WIDTH):
            r = random.random()
            if r < 0.1:
                row.append("rock")      # unpassierbar
            elif r < 0.2:
                row.append("water")     # unpassierbar
            elif r < 0.4:
                row.append("forest")
            else:
                row.append("grass")
        world.append(row)
    return world

def draw_map(screen, world, player):
    """Zeichnet die Karte inkl. Spieler"""
    camera_x = player["x"] - VISIBLE_WIDTH // 2
    camera_y = player["y"] - VISIBLE_HEIGHT // 2

    camera_x = max(0, min(camera_x, WORLD_WIDTH - VISIBLE_WIDTH))
    camera_y = max(0, min(camera_y, WORLD_HEIGHT - VISIBLE_HEIGHT))

    for y in range(VISIBLE_HEIGHT):
        for x in range(VISIBLE_WIDTH):
            world_x = x + camera_x
            world_y = y + camera_y

            tile = world[world_y][world_x]

            color = (34,177,76)  # Gras
            if tile == "rock":
                color = (80,80,80)
            elif tile == "water":
                color = (0,100,200)
            elif tile == "forest":
                color = (0,120,0)

            rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0,0,0), rect, 1)

    # Spieler zentriert zeichnen
    player_screen_x = (player["x"] - camera_x) * TILE_SIZE
    player_screen_y = (player["y"] - camera_y) * TILE_SIZE
    pygame.draw.rect(screen, (0,162,232),
                     (player_screen_x, player_screen_y, TILE_SIZE, TILE_SIZE))
