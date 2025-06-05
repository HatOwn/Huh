import curses
import time
import random

# Simple second-person shooter demonstration using curses

def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(True)  # Non-blocking input
    height, width = stdscr.getmaxyx()

    # Basic check for a minimally sized terminal
    if height < 5 or width < 20:
        stdscr.addstr(0, 0, "Terminal too small")
        stdscr.refresh()
        time.sleep(2)
        return

    enemy_x = width // 2  # Controlled by user
    player_x = width // 2  # Automated opponent
    bullets = []  # Bullets fired by the enemy (user)
    frame = 0

    instructions = "Use LEFT/RIGHT to move enemy, SPACE to shoot, Q to quit"

    while True:
        stdscr.clear()
        stdscr.addstr(0, max(0, (width - len(instructions)) // 2), instructions)

        # Draw player ("you") at the top, facing the enemy
        player_str = "YOU"
        stdscr.addstr(2, max(0, min(width - len(player_str), player_x)), player_str)

        # Draw enemy at the bottom of the screen
        enemy_str = "ENEMY"  # from whose eyes we see
        stdscr.addstr(height - 2, max(0, min(width - len(enemy_str), enemy_x)), enemy_str)

        # Draw bullets
        for y, x in bullets:
            if 0 < y < height - 1:
                stdscr.addstr(y, x, "|")

        stdscr.refresh()
        time.sleep(0.05)

        # Move bullets upward
        bullets = [(y - 1, x) for y, x in bullets if y - 1 > 1]

        # Move player automatically for some challenge
        frame += 1
        if frame % 5 == 0:
            player_x += random.choice([-1, 1])
            player_x = max(0, min(width - len(player_str), player_x))

        # Check collisions
        for y, x in bullets:
            if y == 2 and player_x <= x < player_x + len(player_str):
                stdscr.addstr(height // 2, width // 2 - 5, "HIT! Press any key.")
                stdscr.nodelay(False)
                stdscr.getch()
                return

        # Handle user input
        try:
            key = stdscr.getch()
        except curses.error:
            key = -1

        if key == ord('q') or key == ord('Q'):
            break
        elif key == curses.KEY_LEFT:
            enemy_x = max(0, enemy_x - 1)
        elif key == curses.KEY_RIGHT:
            enemy_x = min(width - len(enemy_str), enemy_x + 1)
        elif key == ord(' '):
            bullets.append((height - 3, enemy_x + len(enemy_str) // 2))

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except curses.error:
        print("This demo requires a terminal that supports curses.")
