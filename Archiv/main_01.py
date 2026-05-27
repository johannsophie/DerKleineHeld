import pygame
import sys
import random

pygame.init()

# ---------- IMPORTS ----------
from config import *
from player import create_player, level_up
from battle import start_battle, battle_turn
from world import generate_world, draw_map
from ui import draw_ui, draw_battle, draw_gameover  # UI Modul importieren

# ---------- FENSTER INITIALISIERUNG ----------
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Eisenkrone")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 22)

# ---------- SPIELSTATUS ----------
game_state = "map"       # Aktueller Zustand: map, battle, gameover
battle_log = []          # Pro Kampf
current_monster = None

# ---------- SPIELER ERSTELLEN ----------
player = create_player(WORLD_WIDTH, WORLD_HEIGHT)

# ---------- WELT ERZEUGEN ----------
world = generate_world()

# ---------- MAIN LOOP ----------
while True:
    clock.tick(60)          # Maximal 60 Frames pro Sekunde
    screen.fill((0,0,0))    # Hintergrund schwarz

    # ---------- EVENT-HANDLING ----------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()  # Spiel sauber beenden

        if event.type == pygame.KEYDOWN:

            # ----- MAP-STEUERUNG -----
            if game_state == "map":
                dx, dy = 0, 0
                if event.key == pygame.K_UP: dy = -1
                if event.key == pygame.K_DOWN: dy = 1
                if event.key == pygame.K_LEFT: dx = -1
                if event.key == pygame.K_RIGHT: dx = 1

                # Neue Position prüfen und bewegen
                new_x = player["x"] + dx
                new_y = player["y"] + dy
                if 0 <= new_x < WORLD_WIDTH and 0 <= new_y < WORLD_HEIGHT:
                    if world[new_y][new_x] not in ["rock", "water"]:
                        player["x"] = new_x
                        player["y"] = new_y

                        # 10% Chance auf Kampf
                        if random.random() < 0.10:
                            current_monster, battle_log = start_battle(player)
                            game_state = "battle"

                        # 1% Chance auf Schatz
                        if random.random() < 0.01:
                            treasure = random.randint(1, 100)
                            player["gold"] += treasure

            # ----- BATTLE-STEUERUNG -----
            elif game_state == "battle":
                # Nur Kampf-Tasten akzeptieren (keine Pfeile)
                if event.key == pygame.K_a:
                    # Spieleraktion: Angriff
                    result = battle_turn(player, current_monster, battle_log, "attack", level_up)

                    # Prüfen ob Kampf beendet
                    if result == "victory":
                        game_state = "map"
                    elif result == "defeat":
                        game_state = "gameover"

                # Hier können später weitere Aktionen wie Defend, Magic, Item ergänzt werden

            # ----- GAMEOVER-STEUERUNG -----
            elif game_state == "gameover":
                if event.key == pygame.K_r:
                    # Neustart: volle HP und zurück zur Map
                    player["hp"] = player["max_hp"]
                    game_state = "map"

    # ---------- RENDERN ----------
    if game_state == "map":
        draw_map(screen, world, player)                 # Karte zeichnen
        draw_ui(screen, font, player, VISIBLE_HEIGHT)   # Spieler-UI
    elif game_state == "battle":
        draw_battle(screen, font, player, current_monster, battle_log)  # Kampf-UI
    elif game_state == "gameover":
        draw_gameover(screen, font)                     # Game-Over-UI

    pygame.display.flip()  # Alles auf dem Bildschirm anzeigen
