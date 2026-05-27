import pygame

from config import *  # TILE_SIZE, WIDTH, HEIGHT, etc. importieren

# ---------- UI-FUNKTIONEN ----------
def draw_ui(screen, font, player, visible_height):
    """
    Zeigt die Spielerinformationen am unteren Rand an.
    Parameter:
        screen : pygame.Surface  -> Das Hauptfenster
        font   : pygame.font.Font -> Schriftart
        player : dict            -> Spieler-Daten
        visible_height : int     -> Höhe der Karte in Tiles
    """
    text = f"Lvl:{player['level']} HP:{player['hp']}/{player['max_hp']} Gold:{player['gold']}"
    screen.blit(font.render(text, True, (255,255,255)),
                (10, visible_height * TILE_SIZE + 5))


def draw_battle(screen, font, player, current_monster, battle_log):
    """
    Zeigt den Kampfbildschirm an: Spieler-HP, Monster-HP, Battle-Log und Steuerhinweise.
    Parameter:
        screen          : pygame.Surface
        font            : pygame.font.Font
        player          : dict
        current_monster : dict
        battle_log      : list
    """
    screen.fill((60,60,60))  # Hintergrund dunkelgrau

    # Spieler-HP
    screen.blit(font.render(f"HP: {player['hp']}", True, (255,255,255)), (100,200))
    # Monster-HP
    screen.blit(font.render(f"Monster HP: {current_monster['hp']}", True, (255,255,255)), (600,200))

    # Battle-Log (nur die letzten 5 Nachrichten)
    y = 300
    for line in battle_log[-5:]:
        screen.blit(font.render(line, True, (255,255,255)), (50,y))
        y += 25

    # Steuerhinweis
    screen.blit(font.render("A = Angreifen", True, (255,255,255)), (50,500))


def draw_gameover(screen, font):
    """
    Zeigt den Game-Over-Bildschirm an.
    Parameter:
        screen : pygame.Surface
        font   : pygame.font.Font
    """
    screen.fill((150,0,0))  # Hintergrund rot
    screen.blit(font.render("GAME OVER - R Neustart", True, (255,255,255)), (300,300))
