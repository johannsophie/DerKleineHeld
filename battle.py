"""
battle.py – Kampfsystem des Spiels.

Verwaltet die gesamte Kampf-Logik: Erstellen von Monstern, deren
Skalierung basierend auf der aktuellen Dungeon-Ebene, sowie die
rundenbasierte Kampfmechanik (Spieler- und Monster-Angriffe,
Schadensberechnung, Belohnungen und Level-Ups).
"""

import random


# ==========================================================
# KAMPF STARTEN
# ==========================================================

def start_battle(player, current_floor):
    """
    Erstellt ein neues Monster für den Kampf.

    Die Werte des Monsters skalieren mit der aktuellen
    Dungeon-Ebene.
    """

    # Basiswerte
    base_hp = 30
    base_attack = 8
    base_defense = 3
    base_gold = 10
    base_xp = 10

    # --------------------------------------------
    # Skalierung mit Dungeon-Ebene
    # --------------------------------------------
    monster = {
        "hp": int(base_hp * (1 + 0.12 * current_floor)),
        "attack": int(base_attack * (1 + 0.08 * current_floor)),
        "defense": int(base_defense * (1 + 0.05 * current_floor)),
        "gold": int(base_gold * (1 + 0.15 * current_floor)),
        "xp": int(base_xp * (1 + 0.15 * current_floor))
    }

    battle_log = []
    battle_log.append(f"Ein Monster erscheint! (Ebene {current_floor})")

    return monster, battle_log


# ==========================================================
# KAMPFRUNDE
# ==========================================================

def battle_turn(player, monster, battle_log, action, level_up_function):
    """
    Führt eine Kampfrunde aus.

    action = "attack"
    """

    # ------------------------------------------------------
    # SPIELER GREIFT AN
    # ------------------------------------------------------
    if action == "attack":

        damage = max(1, player["attack"] - monster["defense"])
        monster["hp"] -= damage

        battle_log.append(f"Du verursachst {damage} Schaden!")

        if monster["hp"] <= 0:
            battle_log.append("Monster besiegt!")

            # Belohnung
            player["gold"] += monster["gold"]
            player["xp"] += monster["xp"]

            battle_log.append(f"+{monster['gold']} Gold")
            battle_log.append(f"+{monster['xp']} XP")

            # Level-Up prüfen
            result = level_up_function(player)
            if result == "level_up":
                battle_log.append("Level-Up!")

            return "victory"

    # ------------------------------------------------------
    # MONSTER GREIFT AN
    # ------------------------------------------------------
    damage = max(1, monster["attack"] - player["defense"])
    player["hp"] -= damage

    battle_log.append(f"Monster verursacht {damage} Schaden!")

    if player["hp"] <= 0:
        battle_log.append("Du wurdest besiegt...")
        return "defeat"

    return "continue"
