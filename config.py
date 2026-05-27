"""
config.py – Zentrale Konfigurationskonstanten für das Spiel.

Definiert Tile-Größe, Welt-Dimensionen, den sichtbaren Kartenausschnitt
(Viewport) sowie die Höhe der UI-Leiste. Alle Bildschirmabmessungen
werden aus diesen Grundwerten abgeleitet.
"""

# ---------- WELT ----------
TILE_SIZE = 40

WORLD_WIDTH = 80
WORLD_HEIGHT = 60

VISIBLE_WIDTH = 20
VISIBLE_HEIGHT = 15

UI_HEIGHT = 40

WIDTH = VISIBLE_WIDTH * TILE_SIZE
HEIGHT = VISIBLE_HEIGHT * TILE_SIZE + UI_HEIGHT
