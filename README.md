# Second Person Shooter

This repository contains a second-person shooter demo implemented in Python using the built-in `curses` library.

You play from the enemy's perspective. The latest version uses colors and a simple pseudo‑3D corridor with obstacles moving toward you. A scoring system and multiple lives are provided. After losing all lives you can restart without leaving the program.

## Running the game

This demo requires a terminal that supports the Python `curses` module. On
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
