Breakout Game - Computer Graphics Project
Overview
This project is a classic Breakout game implemented using Python's turtle graphics library, with additional sound effects powered by pygame.mixer. The game features a paddle controlled by mouse movement, a bouncing ball, breakable bricks, a starry background with a nebula effect, and an animated title screen. The objective is to break all bricks by bouncing the ball off the paddle while collecting power-ups to gain extra lives.
Features

Gameplay Mechanics:
Move the paddle using mouse X-position to bounce the ball.
Break bricks to score points (10 points per brick).
Collect power-ups (life charges) to gain up to 3 lives.
Ball speed increases every 100 points.
Lives are lost when the ball falls below the paddle.
Win by breaking all bricks; lose if all lives are depleted.


Visuals:
Starfield background with twinkling stars and nebula lines.
Animated title screen with fading "BREAKOUT GAME!" text.
Custom paddle and ball rendering using turtle graphics.
Life icons displayed as custom shapes (power.gif).


Audio:
Sound effects for paddle hits, brick breaks, game start, win, and loss.
Background music during the intro animation.


Mouse Tracking:
Real-time mouse tracking for paddle control using a separate thread.


Power-Ups:
Life charge power-ups spawn periodically and fall from the top.
Collecting a power-up increases lives (max 3).



Requirements
To run the game, ensure you have the following installed:

Python 3.x
Required Python libraries:
turtle (built-in with Python)
pygame (for sound effects)
random, math, time, os, threading (built-in with Python)


Asset files:
Sound files: paddle_hit.wav, brick_break.wav, game_over.wav, game_win.wav, start_game.wav, game_sound.wav.mp3
Image files: background.gif, power.gif, life_charge.gif, powerup.gif



Installation

Install Python 3.x from python.org.
Install pygame using pip:pip install pygame


Place the required sound and image files in the same directory as main.py.

How to Run

Save the provided code as main.py.
Ensure all required asset files are in the same directory.
Run the script:python main.py


The game starts with an intro animation, followed by the title screen.
Click the "Start" button to begin playing, or the "Restart" button after a game over or win.
Move the mouse left or right to control the paddle.
Close the window to exit the game.

File Structure

main.py: Main game script containing all game logic, graphics, and sound handling.
Asset files:
paddle_hit.wav: Sound for ball hitting the paddle.
brick_break.wav: Sound for breaking a brick.
game_over.wav: Sound for game over.
game_win.wav: Sound for winning the game.
start_game.wav: Sound for starting the game.
game_sound.wav.mp3: Background music for the intro.
background.gif: Optional background image.
power.gif: Icon for lives display.
life_charge.gif: Shape for life charge power-ups.
powerup.gif: Shape for power-up items.



Known Issues

If asset files (sounds or images) are missing, warnings are printed, and the game falls back to default visuals (black background) or disables sounds.
Mouse tracking may fail if the window is moved rapidly; the game clamps paddle movement to prevent out-of-bounds issues.
The game is not optimized for high-resolution displays, which may affect mouse coordinate accuracy.

Controls

Mouse X-axis: Move the paddle left or right.
Left Mouse Click: Click the "Start" or "Restart" button on the title or end screen.

Future Improvements

Add more power-up types (e.g., paddle size increase, multi-ball).
Implement a high-score system with persistent storage.
Enhance graphics with additional animations or particle effects.
Optimize mouse tracking for better responsiveness.
Add difficulty levels or adjustable game speed.

Credits

Built using Python's turtle and pygame.mixer libraries.
Designed as a computer graphics project to demonstrate 2D rendering, collision detection, and animation.

For issues or suggestions, please contact the project maintainer.