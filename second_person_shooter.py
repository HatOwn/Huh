import curses
import time
import random

"""More advanced second-person shooter with a pseudo 3D effect.

This version keeps the original idea of viewing "YOU" from the enemy's
perspective but adds a basic sense of depth. Obstacles spawn in the
distance and move toward the player, growing in size to simulate 3D.
The enemy (the user) can move left and right and shoot bullets upward.
The game tracks score and lives.
"""

def draw_corridor(stdscr, height: int, width: int) -> None:
    """Draw simple converging lines to give a 3D corridor effect."""
    attr = curses.color_pair(1)
    center = width // 2
    for y in range(height):
        ratio = y / height
        left = int(center * ratio)
        right = width - left - 1
        if 0 <= left < width:
            stdscr.addch(y, left, '/', attr)
        if 0 <= right < width:
            stdscr.addch(y, right, '\\', attr)


def bullet_hit(y: int, x: int, obstacles, player_x: int, height: int) -> bool:
    """Check if a bullet hits an obstacle or the player."""
    for i, (depth, ox) in enumerate(obstacles):
        oy = int(3 + depth * (height - 6))
        size = 1 + int(depth * 3)
        if oy <= y < oy + size and ox <= x < ox + size:
            del obstacles[i]
            return True
    return False


def play_game(stdscr) -> int:
    """Run one game loop and return the final score."""
    height, width = stdscr.getmaxyx()
    enemy_x = width // 2
    player_x = width // 2
    bullets = []
    obstacles = []
    score = 0
    lives = 3
    frame = 0
    instructions = "LEFT/RIGHT move enemy, SPACE shoot, Q quit"

    while lives > 0:
        stdscr.erase()
        stdscr.addstr(0, max(0, (width - len(instructions)) // 2), instructions, curses.color_pair(5))
        stdscr.addstr(1, 2, f"Score: {score}", curses.color_pair(5))
        stdscr.addstr(1, width - 15, f"Lives: {lives}", curses.color_pair(5))

        draw_corridor(stdscr, height, width)

        player_str = "YOU"
        stdscr.addstr(3, max(0, min(width - len(player_str), player_x)), player_str, curses.color_pair(4) | curses.A_BOLD)

        enemy_str = "ENEMY"
        stdscr.addstr(height - 2, max(0, min(width - len(enemy_str), enemy_x)), enemy_str, curses.color_pair(4) | curses.A_BOLD)

        # Draw obstacles with pseudo 3D size scaling
        new_obs = []
        for depth, ox in obstacles:
            y = int(3 + depth * (height - 6))
            size = 1 + int(depth * 3)
            for i in range(size):
                if 2 < y + i < height - 3:
                    for j in range(size):
                        if 0 <= ox + j < width:
                            stdscr.addch(y + i, ox + j, '#', curses.color_pair(2) | curses.A_BOLD)
            new_depth = depth + 0.02
            if new_depth < 1:
                new_obs.append((new_depth, ox))
            else:
                lives -= 1
        obstacles = new_obs

        # Draw bullets
        new_bullets = []
        for y, x in bullets:
            new_y = y - 1
            if new_y <= 3:
                if player_x <= x < player_x + len(player_str):
                    score += 1
                    lives -= 1
                    continue
            if bullet_hit(new_y, x, obstacles, player_x, height):
                score += 10
                continue
            if new_y > 1:
                stdscr.addch(new_y, x, '|', curses.color_pair(3))
                new_bullets.append((new_y, x))
        bullets = new_bullets

        # Move player automatically
        frame += 1
        if frame % 5 == 0:
            player_x += random.choice([-1, 1])
            player_x = max(0, min(width - len(player_str), player_x))

        # Spawn obstacles occasionally
        if random.random() < 0.1:
            obstacles.append((0.0, random.randint(1, width - 4)))

        stdscr.refresh()
        time.sleep(0.05)

        try:
            key = stdscr.getch()
        except curses.error:
            key = -1

        if key in (ord('q'), ord('Q')):
            break
        elif key == curses.KEY_LEFT:
            enemy_x = max(0, enemy_x - 2)
        elif key == curses.KEY_RIGHT:
            enemy_x = min(width - len(enemy_str), enemy_x + 2)
        elif key == ord(' '):
            bullets.append((height - 3, enemy_x + len(enemy_str) // 2))

    stdscr.nodelay(False)
    return score


def main(stdscr):
    curses.curs_set(0)
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    if curses.has_colors():
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_CYAN, -1)
        curses.init_pair(2, curses.COLOR_RED, -1)
        curses.init_pair(3, curses.COLOR_YELLOW, -1)
        curses.init_pair(4, curses.COLOR_GREEN, -1)
        curses.init_pair(5, curses.COLOR_WHITE, -1)

    height, width = stdscr.getmaxyx()
    if height < 20 or width < 40:
        stdscr.addstr(0, 0, "Terminal too small for 3D mode")
        stdscr.refresh()
        time.sleep(2)
        return

    while True:
        stdscr.nodelay(True)
        score = play_game(stdscr)
        stdscr.nodelay(False)
        msg = f"Game Over! Score: {score}"
        stdscr.addstr(height // 2, max(0, (width - len(msg)) // 2), msg, curses.color_pair(5) | curses.A_BOLD)
        prompt = "Press R to restart or Q to quit"
        stdscr.addstr(height // 2 + 1, max(0, (width - len(prompt)) // 2), prompt, curses.color_pair(5))
        stdscr.refresh()
        while True:
            key = stdscr.getch()
            if key in (ord('r'), ord('R')):
                stdscr.clear()
                break
            if key in (ord('q'), ord('Q')):
                return

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except curses.error:
        print("This demo requires a terminal that supports curses.")
