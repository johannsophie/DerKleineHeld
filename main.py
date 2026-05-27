import pygame
import sys
import random

# Eigene Module importieren
from world import generate_dungeon_floor
from battle import start_battle, battle_turn
from player import create_player, level_up
from ui import draw_map_ui, draw_battle_ui, draw_gameover_ui


# ==========================================================
# GRUNDEINSTELLUNGEN
# ==========================================================

pygame.init()

TILE_SIZE = 32
WORLD_WIDTH = 21     # MUSS ungerade sein (Maze!)
WORLD_HEIGHT = 21    # MUSS ungerade sein (Maze!)

SCREEN_WIDTH = WORLD_WIDTH * TILE_SIZE
SCREEN_HEIGHT = WORLD_HEIGHT * TILE_SIZE

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Der kleine Held")

clock = pygame.time.Clock()


# ==========================================================
# SPIELER UND DUNGEON INITIALISIEREN
# ==========================================================

player = create_player()

current_floor = 1  # Aktuelle Dungeon-Ebene

# Erste Ebene erzeugen
world, player["x"], player["y"] = generate_dungeon_floor(
    WORLD_WIDTH,
    WORLD_HEIGHT,
    current_floor
)

game_state = "map"   # mögliche States: map, battle, gameover
current_monster = None
battle_log = []


# ==========================================================
# HAUPTSCHLEIFE
# ==========================================================

while True:

    # ------------------------------------------------------
    # EVENTS ABFRAGEN (Tasteneingaben, Fenster schließen)
    # ------------------------------------------------------
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # --------------------------------------------------
        # TASTEN-EVENTS
        # --------------------------------------------------
        if event.type == pygame.KEYDOWN:

            # ==================================================
            # MAP-LOGIK (Bewegung nur auf der Map erlaubt)
            # ==================================================
            if game_state == "map":

                dx, dy = 0, 0

                if event.key == pygame.K_UP:
                    dy = -1
                if event.key == pygame.K_DOWN:
                    dy = 1
                if event.key == pygame.K_LEFT:
                    dx = -1
                if event.key == pygame.K_RIGHT:
                    dx = 1

                new_x = player["x"] + dx
                new_y = player["y"] + dy

                # Prüfen, ob Position im Spielfeld liegt
                if 0 <= new_x < WORLD_WIDTH and 0 <= new_y < WORLD_HEIGHT:

                    tile = world[new_y][new_x]

                    # Bewegung nur erlaubt, wenn es keine Wand ist
                    if tile != "wall":

                        player["x"] = new_x
                        player["y"] = new_y

                        # --------------------------------------
                        # 1️⃣ Wenn Treppe betreten → neue Ebene
                        # --------------------------------------
                        if tile == "stairs_down":
                            current_floor += 1

                            world, player["x"], player["y"] = generate_dungeon_floor(
                                WORLD_WIDTH,
                                WORLD_HEIGHT,
                                current_floor
                            )

                        # --------------------------------------
                        # 2️⃣ Kampfchance nur auf normalen Feldern
                        # --------------------------------------
                        if tile == "floor":

                            # 10% Chance auf Kampf
                            if random.random() < 0.10:

                                current_monster, battle_log = start_battle(
                                    player,
                                    current_floor   # Monster skalieren
                                )

                                game_state = "battle"

                        # --------------------------------------
                        # 3️⃣ Startfeld = sicherer Bereich
                        # --------------------------------------
                        if tile == "start":
                            # Hier später Shop öffnen
                            pass

            # ==================================================
            # BATTLE-LOGIK
            # ==================================================
            elif game_state == "battle":

                # Nur A-Taste erlaubt (Angriff)
                if event.key == pygame.K_a:

                    result = battle_turn(
                        player,
                        current_monster,
                        battle_log,
                        "attack",
                        level_up
                    )

                    if result == "victory":
                        game_state = "map"

                    elif result == "defeat":
                        game_state = "gameover"

            # ==================================================
            # GAMEOVER-LOGIK
            # ==================================================
            elif game_state == "gameover":

                if event.key == pygame.K_r:

                    # Spieler wiederherstellen
                    player = create_player()
                    current_floor = 1

                    world, player["x"], player["y"] = generate_dungeon_floor(
                        WORLD_WIDTH,
                        WORLD_HEIGHT,
                        current_floor
                    )

                    game_state = "map"

    # ==========================================================
    # ZEICHNEN (RENDERING)
    # ==========================================================

    screen.fill((0, 0, 0))

    if game_state == "map":
        draw_map_ui(screen, world, player, current_floor)

    elif game_state == "battle":
        draw_battle_ui(screen, player, current_monster, battle_log)

    elif game_state == "gameover":
        draw_gameover_ui(screen, current_floor)

    pygame.display.flip()
    clock.tick(60)
