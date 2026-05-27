import random


# ==========================================================
# WORLD / DUNGEON GENERATION
# ==========================================================
#
# Diese Datei ist dafür zuständig, eine neue Dungeon-Ebene
# zu erzeugen.
#
# Jede Ebene besteht aus:
# - Wänden ("wall")
# - normalen begehbaren Feldern ("floor")
# - einem Startfeld ("start")
# - einer Treppe nach unten ("stairs_down")
#
# Der Dungeon wird automatisch als Labyrinth erzeugt.
# Der Spieler startet immer in der Mitte.
#
# ==========================================================


def generate_dungeon_floor(width, height, floor_number=1):
    """
    Diese Funktion erzeugt eine komplette Dungeon-Ebene.

    Parameter:
        width  -> Breite der Karte
        height -> Höhe der Karte
        floor_number -> aktuelle Dungeon-Ebene (wird später
                        für Schwierigkeit benutzt)

    Rückgabe:
        world   -> 2D-Liste mit allen Feldern
        start_x -> Startposition X für den Spieler
        start_y -> Startposition Y für den Spieler
    """

    # ------------------------------------------------------
    # WICHTIG:
    # Der Maze-Algorithmus funktioniert nur korrekt,
    # wenn Breite und Höhe ungerade Zahlen sind.
    #
    # Falls gerade Zahlen übergeben werden,
    # machen wir sie automatisch ungerade.
    # ------------------------------------------------------
    if width % 2 == 0:
        width -= 1
    if height % 2 == 0:
        height -= 1

    # ------------------------------------------------------
    # Schritt 1:
    # Erstelle eine komplett mit Wänden gefüllte Welt.
    #
    # world[y][x]
    #
    # Beispiel:
    # [
    #   ["wall", "wall", "wall"],
    #   ["wall", "wall", "wall"],
    #   ["wall", "wall", "wall"]
    # ]
    # ------------------------------------------------------
    world = [["wall" for _ in range(width)] for _ in range(height)]

    # ------------------------------------------------------
    # Schritt 2:
    # Maze-Algorithmus (Recursive Backtracker)
    #
    # Diese Funktion gräbt Gänge in die Wände.
    #
    # Funktionsweise:
    # - Von einer Position aus
    # - In zufällige Richtungen prüfen
    # - Zwei Felder weitergehen
    # - Wenn dort noch eine Wand ist:
    #     - Verbindung öffnen
    #     - Rekursiv weitergraben
    # ------------------------------------------------------
    def carve(x, y):

        # Mögliche Richtungen (2 Felder Abstand!)
        directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]

        # Richtungen zufällig mischen,
        # damit jedes Labyrinth anders aussieht
        random.shuffle(directions)

        for dx, dy in directions:

            # Zielposition berechnen
            nx = x + dx
            ny = y + dy

            # Prüfen, ob Ziel im gültigen Bereich liegt
            if 1 <= nx < width - 1 and 1 <= ny < height - 1:

                # Nur graben, wenn dort noch eine Wand ist
                if world[ny][nx] == "wall":

                    # Die Wand zwischen Start und Ziel entfernen
                    world[y + dy // 2][x + dx // 2] = "floor"

                    # Ziel selbst zu Boden machen
                    world[ny][nx] = "floor"

                    # Von dort aus weitergraben (Rekursion!)
                    carve(nx, ny)

    # ------------------------------------------------------
    # Schritt 3:
    # Startpunkt in der Mitte berechnen
    # ------------------------------------------------------
    start_x = width // 2
    start_y = height // 2

    # Mittelpunkt zunächst als begehbar markieren
    world[start_y][start_x] = "floor"

    # Maze von der Mitte aus generieren
    carve(start_x, start_y)

    # ------------------------------------------------------
    # Schritt 4:
    # Startfeld setzen
    #
    # Dieses Feld ist später:
    # - Spawnpunkt
    # - Shop
    # - Monsterfreie Zone
    # ------------------------------------------------------
    world[start_y][start_x] = "start"

    # ------------------------------------------------------
    # Schritt 5:
    # Treppe nach unten platzieren
    #
    # Wir suchen alle normalen Bodenfelder
    # und wählen zufällig eines aus.
    #
    # Wichtig:
    # Die Treppe darf NICHT auf dem Startfeld sein.
    # ------------------------------------------------------
    floor_tiles = [
        (x, y)
        for y in range(height)
        for x in range(width)
        if world[y][x] == "floor"
    ]

    if floor_tiles:
        stairs_x, stairs_y = random.choice(floor_tiles)
        world[stairs_y][stairs_x] = "stairs_down"

    # ------------------------------------------------------
    # Fertige Welt zurückgeben
    # ------------------------------------------------------
    return world, start_x, start_y


# ==========================================================
# DEBUG-FUNKTION
# ==========================================================
#
# Diese Funktion gibt die Welt im Terminal aus.
# Sehr hilfreich zum Testen ohne Grafik.
#
# ==========================================================

def print_world(world):
    """
    Wandelt die Tile-Namen in Symbole um
    und gibt das Labyrinth im Terminal aus.
    """

    tile_symbols = {
        "wall": "#",
        "floor": ".",
        "start": "S",
        "stairs_down": ">"
    }

    for row in world:
        print("".join(tile_symbols.get(tile, "?") for tile in row))
