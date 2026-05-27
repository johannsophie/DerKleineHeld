# Der kleine Held – Projektdokumentation

## Uebersicht

**Der kleine Held** ist ein Dungeon-Crawler-Spiel, geschrieben in Python mit [Pygame](https://www.pygame.org/).
Der Spieler erkundet prozedural generierte Labyrinthe, kaempft rundenbasiert gegen Monster und steigt dabei im Level auf.

---

## Projektstruktur

```
DerKleineHeld/
├── main.py        # Einstiegspunkt – Game-Loop und Spielzustaende
├── config.py      # Zentrale Konstanten (Tile-Groesse, Welt-Dimensionen, Viewport)
├── player.py      # Spieler-Erzeugung und Level-Up-System
├── battle.py      # Kampfsystem (Monster-Erzeugung, Schadensberechnung)
├── ui.py          # Rendering der drei Bildschirme (Map, Battle, Game Over)
├── world.py       # Dungeon-Generierung (Recursive-Backtracker-Labyrinth)
└── Archiv/        # Aeltere Versionen der Module (Backup)
```

---

## Module im Detail

### `main.py` – Game-Loop

Zentraler Einstiegspunkt. Initialisiert Pygame und das Spielfenster, erzeugt den Spieler
und die erste Dungeon-Ebene. Die Hauptschleife (`while True`) verwaltet drei Zustaende:

| Zustand    | Beschreibung                                         | Steuerung       |
|------------|------------------------------------------------------|-----------------|
| `map`      | Erkundung des Labyrinths                             | Pfeiltasten     |
| `battle`   | Rundenbasierter Kampf gegen ein zufaelliges Monster  | Taste **A**     |
| `gameover` | Endbildschirm mit Neustart-Option                    | Taste **R**     |

**Ablauf pro Frame:**
1. Events abfragen (Tasteneingaben, Fenster schliessen)
2. Je nach `game_state` die passende Logik ausfuehren
3. Bildschirm leeren und den aktuellen Zustand zeichnen (`draw_*_ui`)
4. Display-Update und Frame-Rate begrenzen (60 FPS)

---

### `config.py` – Konfiguration

Enthaelt globale Konstanten, die an mehreren Stellen im Projekt verwendet werden:

- **`TILE_SIZE`** – Pixelgroesse eines einzelnen Kartenfeldes
- **`WORLD_WIDTH` / `WORLD_HEIGHT`** – Gesamtgroesse der Dungeon-Ebene in Tiles
- **`VISIBLE_WIDTH` / `VISIBLE_HEIGHT`** – Sichtbarer Kartenausschnitt (Viewport)
- **`UI_HEIGHT`** – Hoehe der unteren UI-Leiste in Pixeln
- **`WIDTH` / `HEIGHT`** – Resultierende Fenstergroesse in Pixeln

> **Hinweis:** `main.py` definiert aktuell eigene lokale Konstanten (`TILE_SIZE = 32`, etc.),
> die die Werte aus `config.py` noch nicht verwenden. Eine Konsolidierung steht noch aus.

---

### `player.py` – Spieler-Logik

| Funktion         | Beschreibung                                                                 |
|------------------|-----------------------------------------------------------------------------|
| `create_player()`| Erzeugt ein Spieler-Dictionary mit Startattributen (HP, Angriff, Verteidigung, XP, Gold). Position wird spaeter von `main.py` gesetzt. |
| `level_up(player)` | Prueft, ob genug XP fuer ein Level-Up vorhanden sind. Falls ja: Level erhoehen, Attribute verbessern, HP voll heilen. |

**Level-Up-Formel:** `benoetigte_XP = Level * 20`

---

### `battle.py` – Kampfsystem

| Funktion | Beschreibung |
|----------|-------------|
| `start_battle(player, current_floor)` | Erstellt ein Monster-Dictionary mit skalierten Werten und gibt es zusammen mit einem initialen Battle-Log zurueck. |
| `battle_turn(player, monster, battle_log, action, level_up_function)` | Fuehrt eine Kampfrunde aus: Spieler greift an, dann (falls Monster ueberlebt) greift Monster an. Gibt `"victory"`, `"defeat"` oder `"continue"` zurueck. |

**Monster-Skalierung:** Alle Basiswerte werden mit dem Faktor `(1 + rate * Ebene)` multipliziert,
wobei `rate` pro Attribut unterschiedlich ist (z. B. HP +12 %/Ebene, Angriff +8 %/Ebene).

**Schadensformel:** `Schaden = max(1, Angriff_Angreifer - Verteidigung_Verteidiger)`

---

### `ui.py` – Darstellung

Drei reine Zeichen-Funktionen, die direkt auf das Pygame-`screen`-Objekt zeichnen:

| Funktion | Beschreibung |
|----------|-------------|
| `draw_map_ui(screen, world, player, current_floor)` | Zeichnet das Dungeon-Grid farbkodiert (Wand=dunkelgrau, Boden=grau, Start=gruen, Treppe=lila), den Spieler (blau) und die aktuelle Ebenennummer. |
| `draw_battle_ui(screen, player, monster, battle_log)` | Zeigt Spieler-HP, Monster-HP, die letzten 5 Log-Eintraege und einen Eingabe-Hinweis. |
| `draw_gameover_ui(screen, current_floor)` | Zeigt "GAME OVER", die erreichte Ebene und den Neustart-Hinweis. |

---

### `world.py` – Dungeon-Generierung

**Algorithmus:** Recursive Backtracker (Tiefensuche mit zufaelliger Richtungswahl).

**Ablauf von `generate_dungeon_floor(width, height, floor_number)`:**

1. Breite/Hoehe auf ungerade Werte korrigieren (Voraussetzung fuer den Algorithmus)
2. 2D-Grid komplett mit `"wall"` fuellen
3. Startpunkt in der Mitte berechnen und als `"floor"` markieren
4. Rekursiv Gaenge graben (`carve`-Funktion):
   - Von der aktuellen Position 2 Felder in eine zufaellige Richtung pruefen
   - Falls dort noch Wand steht: Wand dazwischen und Zielfeld oeffnen, rekursiv weiter
5. Startfeld als `"start"` markieren (sicherer Bereich / zukuenftiger Shop)
6. Zufaelliges Bodenfeld als `"stairs_down"` markieren (Treppe zur naechsten Ebene)

**Debug:** `print_world(world)` gibt das Labyrinth als ASCII-Art im Terminal aus
(`#` = Wand, `.` = Boden, `S` = Start, `>` = Treppe).

---

## Spielmechaniken auf einen Blick

| Mechanik           | Details                                                   |
|--------------------|-----------------------------------------------------------|
| Bewegung           | Pfeiltasten, tile-basiert, keine diagonale Bewegung       |
| Zufallskaempfe     | 10 % Chance pro Schritt auf einem normalen Bodenfeld      |
| Kampf              | Rundenbasiert, Taste A = Angriff                          |
| Level-Up           | Automatisch bei genuegend XP; heilt HP komplett           |
| Dungeon-Abstieg    | Treppe betreten erzeugt neue, schwerere Ebene             |
| Game Over          | Bei 0 HP; Neustart mit Taste R                            |

---

## Starten

```bash
# Voraussetzung: Python 3 und Pygame installiert
pip install pygame

# Spiel starten
python main.py
```
