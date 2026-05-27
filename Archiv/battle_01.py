import random

# ---------- MONSTER ERZEUGEN ----------
def create_monster(player_level):
    """
    Erstellt ein Monster basierend auf Spielerlevel.
    """
    return {
        "level": player_level,
        "max_hp": 35 + player_level * 8,
        "hp": 35 + player_level * 8,
        "str": 6 + player_level * 2,
        "def": 3 + player_level
    }

# ---------- BATTLE START ----------
def start_battle(player):
    """
    Startet einen Kampf gegen ein Monster.
    Gibt Monster-Objekt und Battle-Log zurück.
    """
    monster = create_monster(player["level"])
    battle_log = ["Ein Monster erscheint!"]
    return monster, battle_log

# ---------- SPIELER-AKTIONEN ----------
def player_attack(player, monster, battle_log):
    """
    Spieler greift das Monster an.
    Rückgabe: True, wenn Monster besiegt.
    """
    dmg = max(1, player["str"] - monster["def"] + random.randint(0, 4))
    monster["hp"] -= dmg
    monster["hp"] = max(0, monster["hp"])
    battle_log.append(f"Du verursachst {dmg} Schaden.")
    return monster["hp"] <= 0  # True = Monster tot

# Weitere Aktionen können hier ergänzt werden
# def player_defend(...), def player_magic(...), def player_item(...)

# ---------- MONSTER-AKTION ----------
def monster_attack(player, monster, battle_log):
    """
    Monster greift Spieler an.
    Rückgabe: True, wenn Spieler besiegt.
    """
    dmg = max(1, monster["str"] - player["def"] + random.randint(0, 4))
    player["hp"] -= dmg
    player["hp"] = max(0, player["hp"])
    battle_log.append(f"Monster verursacht {dmg} Schaden.")
    return player["hp"] <= 0  # True = Spieler tot

# ---------- GANZE RUNDEN ----------
def battle_turn(player, monster, battle_log, action, level_up_function):
    """
    Führt eine komplette Kampfrunde aus:
        1. Spieleraktion (attack/defend/magic...)
        2. Monsteraktion
    Rückgabe:
        "victory", "defeat", "continue"
    """
    # ----- Spieleraktion -----
    if action == "attack":
        monster_dead = player_attack(player, monster, battle_log)
        if monster_dead:
            # Belohnungen
            xp_gain = 20 + monster["level"] * 8
            gold_gain = monster["level"] * random.randint(1,4)
            player["xp"] += xp_gain
            player["gold"] += gold_gain
            battle_log.append(f"{xp_gain} XP erhalten, {gold_gain} Gold erhalten.")

            # 10% Heilung
            heal = int(player["max_hp"] * 0.1)
            player["hp"] = min(player["hp"] + heal, player["max_hp"])
            battle_log.append(f"{heal} HP regeneriert.")

            # Level-Up prüfen
            if player["xp"] >= player["xp_to_next"]:
                level_up_function(player)
                battle_log.append("LEVEL UP!")

            return "victory"

    # ----- Monsterzug -----
    player_dead = monster_attack(player, monster, battle_log)
    if player_dead:
        return "defeat"

    return "continue"
