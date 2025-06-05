# Second Person Shooter

This repository contains two versions of a second-person shooter demo.

1. **Terminal version.** Implemented in Python using the built-in `curses` library.
2. **Web version.** Implemented in HTML5 Canvas and JavaScript.

You play from the enemy's perspective. The terminal game features colored pseudo‑3D graphics while the web version offers a simple top–down view. Both provide scoring and multiple lives. After losing all lives you can restart.

## Running the game

### Terminal version

This game requires a terminal that supports the Python `curses` module. On
Windows, you may need to run it inside WSL or another Unix-like environment.

Run the game with:

```bash
python3 second_person_shooter.py
```

Controls:

- **Left/Right arrows** – move the enemy
- **Space** – shoot upward
- **Q** – quit
- **R** – restart after game over

For the best experience, use a terminal window with at least 80x24 characters.
If arrow keys do not respond, ensure your terminal supports them or use a compatible curses environment.


Obstacles appear in the distance and grow larger as they approach to give a 3D effect. Shooting them yields extra points while letting them pass costs you a life. Hitting "YOU" ends the game.

### Web version

Open `index.html` in a modern web browser. Use the left and right arrow keys to move the enemy at the bottom, `Space` to shoot upward, and `Q` to quit. The player at the top moves automatically while obstacles descend. Avoid losing all lives and try to achieve a high score.
