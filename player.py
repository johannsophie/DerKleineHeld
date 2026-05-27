import random


# ==========================================================
# SPIELER ERZEUGEN
# ==========================================================

def create_player():
    """
    Erstellt ein neues Spieler-Dictionary.

    Die Position (x, y) wird NICHT hier gesetzt,
    sondern später von main.py durch die
    Dungeon-Generierung.
    """

    player = {
        "x": 0,
        "y": 0,
        "level": 1,
        "xp": 0,
        "gold": 0,
        "max_hp": 100,
        "hp": 100,
        "attack": 10,
        "defense": 5
    }

    return player


# ==========================================================
# LEVEL-UP SYSTEM
# ==========================================================

def level_up(player):
    """
    Prüft, ob der Spieler genug XP für ein Level-Up hat.
    Wenn ja, werden Werte verbessert.
    """

    required_xp = player["level"] * 20

    if player["xp"] >= required_xp:

        player["xp"] -= required_xp
        player["level"] += 1

        # Werte verbessern
        player["max_hp"] += 20
        player["attack"] += 3
        player["defense"] += 2

        # Spieler komplett heilen beim Level-Up
        player["hp"] = player["max_hp"]

        return "level_up"

    return None


