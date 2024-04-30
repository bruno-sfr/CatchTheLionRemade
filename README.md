# Analyse eines Minimax/MCTS Hybriden anhand des Spiels „Catch the Lion“

## Beschreibung

In diesem Repository befindet sich der relevante Code für die Bachelorarbeit "Analyse eines Minimax/MCTS-Hybriden am Beispiel des Spiels 'Catch the Lion'" von Bruno Schaffer, betreut von Prof. Dr. Benjamin Blankertz und Dr.-Ing. Stefan Fricke.

Das Ziel bestand darin, unter den betrachteten Algorithmen den spielstärksten im Spiel "Catch the Lion" zu bestimmen. Dafür wurde das Spiel "Catch the Lion" mit Hilfe von Bitboards implementiert sowie verschiedene MiniMax-Algorithmen, den MCTS-Solver-Algorithmus und MCTS-Minimax-Hybride.

In dem Projekt ist es über eine GUI möglich, die Algorithmen gegeneinander spielen zu lassen oder selbst gegen die Algorithmen anzutreten.

Als Ergebnis hat sich herausgestellt, dass MTD(f) der spielstärkste Algorithmus im Spiel "Catch the Lion" ist.

## Installation

Um das Project auszuführen muss die Umgebung installiert werden:
```python3 -m pip install .```

## Usage

Um die GUI zu nutzen:
```
cd GUI
python3 The_GUI.py
```
