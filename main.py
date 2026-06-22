"""
Snake-spel för terminalen.

Kör med:
    uv run main.py

Styr ormen med piltangenterna. Ät mat (*) för att växa och få poäng.
Spelet tar slut om ormen krockar med väggen eller sig själv.
Tryck R för att spela igen eller Q för att avsluta.

Använder endast standardbiblioteket (curses + random).
"""

import curses
import random

# Speltakt: lägre värde = snabbare orm (millisekunder per steg).
TICK_MS = 120

# Riktningar som (dy, dx).
UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

KEY_TO_DIR = {
    curses.KEY_UP: UP,
    curses.KEY_DOWN: DOWN,
    curses.KEY_LEFT: LEFT,
    curses.KEY_RIGHT: RIGHT,
}


def init_screen(stdscr):
    """Konfigurera curses-skärmen för spelet."""
    curses.curs_set(0)          # Göm markören.
    stdscr.nodelay(True)        # Blockera inte på input.
    stdscr.keypad(True)         # Tolka piltangenter.
    stdscr.timeout(TICK_MS)     # Speltakt via getch-timeout.


def place_food(snake, height, width):
    """Slumpa en ledig ruta (inte på ormen) innanför spelplanen."""
    while True:
        y = random.randint(1, height - 2)
        x = random.randint(1, width - 2)
        if (y, x) not in snake:
            return (y, x)


def is_opposite(a, b):
    """Sant om riktning a är raka motsatsen till b (180°-vändning)."""
    return a[0] == -b[0] and a[1] == -b[1]


def next_direction(key, current):
    """Returnera ny riktning för knappen (eller oförändrad)."""
    new_dir = KEY_TO_DIR.get(key)
    if new_dir and not is_opposite(new_dir, current):
        return new_dir
    return current


def draw(stdscr, snake, food, score):
    """Rita poäng, ram, mat och orm."""
    stdscr.erase()
    stdscr.addstr(0, 0, f"Poäng: {score}   (Q for att avsluta)")
    stdscr.box()
    fy, fx = food
    stdscr.addch(fy, fx, "*")
    for i, (y, x) in enumerate(snake):
        stdscr.addch(y, x, "@" if i == 0 else "o")
    stdscr.refresh()


def play_game(stdscr):
    """Kör en spelomgång och returnera slutpoängen."""
    height, width = stdscr.getmaxyx()
    start = (height // 2, width // 2)
    snake = [start, (start[0], start[1] - 1), (start[0], start[1] - 2)]
    direction = RIGHT
    food = place_food(snake, height, width)
    score = 0

    while True:
        key = stdscr.getch()  # En läsning per steg (timeout styr takten).
        if key in (ord("q"), ord("Q")):
            return score
        direction = next_direction(key, direction)

        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        # Kollision med vägg eller egen kropp.
        hit_wall = not (0 < head[0] < height - 1 and 0 < head[1] < width - 1)
        if hit_wall or head in snake:
            return score

        snake.insert(0, head)
        if head == food:
            score += 1
            food = place_food(snake, height, width)
        else:
            snake.pop()  # Väx bara när vi ätit, annars flytta svansen.

        draw(stdscr, snake, food, score)


def game_over_screen(stdscr, score):
    """Visa Game Over och vänta på R (om igen) eller Q (avsluta)."""
    stdscr.nodelay(False)
    height, width = stdscr.getmaxyx()
    lines = [
        "GAME OVER",
        f"Slutpoäng: {score}",
        "Tryck R for att spela igen, Q for att avsluta",
    ]
    stdscr.erase()
    stdscr.box()
    for i, text in enumerate(lines):
        y = height // 2 - 1 + i
        x = max(1, (width - len(text)) // 2)
        stdscr.addstr(y, x, text)
    stdscr.refresh()

    while True:
        key = stdscr.getch()
        if key in (ord("r"), ord("R")):
            return True
        if key in (ord("q"), ord("Q")):
            return False


def run(stdscr):
    """Yttre loop: spela, visa game over, eventuellt starta om."""
    while True:
        init_screen(stdscr)
        score = play_game(stdscr)
        if not game_over_screen(stdscr, score):
            return


def main():
    curses.wrapper(run)


if __name__ == "__main__":
    main()
