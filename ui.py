import pygame


# ==========================================================
# MAP-ANSICHT
# ==========================================================

def draw_map_ui(screen, world, player, current_floor):
    """
    Zeichnet die Dungeon-Karte inklusive Spieler
    und zeigt die aktuelle Ebene oben an.
    """

    TILE_SIZE = 32

    colors = {
        "wall": (40, 40, 40),
        "floor": (100, 100, 100),
        "start": (0, 150, 0),
        "stairs_down": (150, 0, 150)
    }

    for y, row in enumerate(world):
        for x, tile in enumerate(row):
            color = colors.get(tile, (255, 0, 0))
            pygame.draw.rect(
                screen,
                color,
                (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            )

    # Spieler zeichnen
    pygame.draw.rect(
        screen,
        (0, 0, 255),
        (player["x"] * TILE_SIZE,
         player["y"] * TILE_SIZE,
         TILE_SIZE,
         TILE_SIZE)
    )

    # Schrift für Ebenenanzeige
    font = pygame.font.SysFont(None, 28)
    text = font.render(f"Ebene: {current_floor}", True, (255, 255, 255))
    screen.blit(text, (10, 10))


# ==========================================================
# BATTLE-ANSICHT
# ==========================================================

def draw_battle_ui(screen, player, monster, battle_log):
    """
    Zeigt Kampf-Informationen an.
    """

    font = pygame.font.SysFont(None, 28)

    y_offset = 50

    # Spielerwerte
    player_text = font.render(
        f"Spieler HP: {player['hp']} / {player['max_hp']}",
        True,
        (255, 255, 255)
    )
    screen.blit(player_text, (50, y_offset))

    # Monsterwerte
    monster_text = font.render(
        f"Monster HP: {monster['hp']}",
        True,
        (255, 0, 0)
    )
    screen.blit(monster_text, (50, y_offset + 40))

    # Battle Log anzeigen
    for i, line in enumerate(battle_log[-5:]):
        log_text = font.render(line, True, (200, 200, 200))
        screen.blit(log_text, (50, y_offset + 100 + i * 30))

    # Hinweis
    hint = font.render("Drücke A zum Angreifen", True, (255, 255, 0))
    screen.blit(hint, (50, 20))


# ==========================================================
# GAME OVER
# ==========================================================

def draw_gameover_ui(screen, current_floor):
    """
    Zeigt Game-Over-Bildschirm an.
    """

    font = pygame.font.SysFont(None, 48)

    text1 = font.render("GAME OVER", True, (255, 0, 0))
    text2 = font.render(f"Erreichte Ebene: {current_floor}", True, (255, 255, 255))
    text3 = font.render("Drücke R zum Neustart", True, (255, 255, 0))

    screen.blit(text1, (200, 150))
    screen.blit(text2, (200, 220))
    screen.blit(text3, (200, 290))
