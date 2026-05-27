# player.py

def create_player(world_width, world_height):
    return {
        "x": world_width // 2,
        "y": world_height // 2,
        "level": 1,
        "xp": 0,
        "xp_to_next": 50,
        "max_hp": 100,
        "hp": 100,
        "gold": 0,
        "str": 10,
        "def": 5
    }


def level_up(player):
    player["level"] += 1
    player["xp"] -= player["xp_to_next"]
    player["xp_to_next"] = int(player["xp_to_next"] * 1.5)
    player["max_hp"] += 15
    player["hp"] = player["max_hp"]
    player["str"] += 2
    player["def"] += 1


