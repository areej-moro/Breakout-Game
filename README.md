# 🎮 Breakout Game - Computer Graphics Project

This project is a classic **Breakout game** implemented in Python using the **Turtle Graphics** library, with additional sound effects powered by **pygame.mixer**.  

The game features a paddle controlled by mouse movement, a bouncing ball, breakable bricks, a starry background with nebula effects, and an animated title screen. The objective is to break all bricks while collecting power-ups and avoiding lives loss.

---

## 🚀 Features

### 🎮 Gameplay Mechanics
- Control the paddle with **mouse X-position** to bounce the ball.  
- Break bricks to score points (**+10 points per brick**).  
- Collect **power-ups** to gain extra lives (up to **3 lives max**).  
- Ball speed increases every **100 points**.  
- Lose a life if the ball falls below the paddle.  
- **Win** by breaking all bricks; **Lose** if all lives are depleted.  

### 🌌 Visuals
- Starfield background with twinkling stars and **nebula lines**.  
- Animated **title screen** with fading “BREAKOUT GAME!” text.  
- Custom paddle and ball rendering using Turtle graphics.  
- **Life icons** displayed as custom shapes (`power.gif`).  

### 🔊 Audio
- Sound effects for:
  - Paddle hits  
  - Brick breaks  
  - Game start  
  - Win & Loss events  
- Background music during the intro animation.  

### 🖱️ Mouse Tracking
- Real-time mouse tracking for paddle control using a separate thread.  

### 💡 Power-Ups
- Life charge power-ups **spawn periodically** and fall from the top.  
- Collecting a power-up increases lives (max 3).  

---

## 📦 Requirements

To run the game, make sure you have:

- **Python 3.x**  
- Required libraries:  
  - `turtle` (built-in with Python)  
  - `pygame` (for sound effects)  
  - `random`, `math`, `time`, `os`, `threading` (built-in with Python)  

- **Asset files** (placed in the same directory as `main.py`):  
  - Sounds:  
    - `paddle_hit.wav`  
    - `brick_break.wav`  
    - `game_over.wav`  
    - `game_win.wav`  
    - `start_game.wav`  
    - `game_sound.wav.mp3`  
  - Images:  
    - `background.gif`  
    - `power.gif`  
    - `life_charge.gif`  
    - `powerup.gif`  

---

## ⚙️ Installation

1. Install [Python 3.x](https://www.python.org/).  
2. Install `pygame`:  
   ```bash
   pip install pygame
