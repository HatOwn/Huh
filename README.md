# Second Person Shooter

This repository contains a minimal second-person shooter demo implemented in Python using the built-in `curses` library.

The game illustrates a perspective where you view yourself from the eyes of an enemy. You control the enemy at the bottom of the screen and attempt to shoot "YOU" at the top.

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

For the best experience, use a terminal window with at least 80x24 characters.

When a bullet reaches "YOU" at the top, the game displays a hit message and exits.
