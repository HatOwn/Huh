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
    center = width // 2
    for y in range(height):
        ratio = y / height
        left = int(center * ratio)
        right = width - left - 1
        if 0 <= left < width:
            stdscr.addch(y, left, '/')
        if 0 <= right < width:
            stdscr.addch(y, right, '\\')


def bullet_hit(y: int, x: int, obstacles, player_x: int, height: int) -> bool:
    """Check if a bullet hits an obstacle or the player."""
    for i, (depth, ox) in enumerate(obstacles):
        oy = int(3 + depth * (height - 6))
        size = 1 + int(depth * 3)
        if oy <= y < oy + size and ox <= x < ox + size:
            del obstacles[i]
            return True
    return False


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    height, width = stdscr.getmaxyx()

    if height < 20 or width < 40:
        stdscr.addstr(0, 0, "Terminal too small for 3D mode")
        stdscr.refresh()
        time.sleep(2)
        return

    enemy_x = width // 2
    player_x = width // 2
    bullets = []  # list[(int,int)]
    obstacles = []  # list[(float,int)] -> depth [0..1], x position
    score = 0
    lives = 3
    frame = 0

    instructions = "LEFT/RIGHT move enemy, SPACE shoot, Q quit"

    while lives > 0:
        stdscr.erase()
        stdscr.addstr(0, max(0, (width - len(instructions)) // 2), instructions)
        stdscr.addstr(1, 2, f"Score: {score}")
        stdscr.addstr(1, width - 15, f"Lives: {lives}")

        draw_corridor(stdscr, height, width)

        player_str = "YOU"
        stdscr.addstr(3, max(0, min(width - len(player_str), player_x)), player_str)

        enemy_str = "ENEMY"
        stdscr.addstr(height - 2, max(0, min(width - len(enemy_str), enemy_x)), enemy_str)

        # Draw obstacles with pseudo 3D size scaling
        new_obs = []
        for depth, ox in obstacles:
            y = int(3 + depth * (height - 6))
            size = 1 + int(depth * 3)
            for i in range(size):
                if 2 < y + i < height - 3:
                    for j in range(size):
                        if 0 <= ox + j < width:
                            stdscr.addch(y + i, ox + j, '#')
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
                stdscr.addch(new_y, x, '|')
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
    stdscr.addstr(height // 2, max(0, width // 2 - 10), f"Game Over! Score: {score}")
    stdscr.getch()

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except curses.error:
        print("This demo requires a terminal that supports curses.")
