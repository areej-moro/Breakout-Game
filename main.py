import turtle 
import random
import math
import pygame.mixer
import time
import os
import threading

class MouseTracker:
    def __init__(self, screen):
        self.screen = screen
        self.mouse_x = None
        self.running = True
        self.thread = threading.Thread(target=self._track_mouse)
        self.thread.daemon = True
        self.thread.start()

    def _track_mouse(self):
        while self.running:
            try:
                # Get mouse position relative to the window
                canvas = self.screen.getcanvas()
                root_x = canvas.winfo_rootx()  # Window's x position on screen
                mouse_x = canvas.winfo_pointerx()  # Mouse's x position on screen
                # Convert to Turtle coordinates (-400 to 400)
                relative_x = mouse_x - root_x - 400  # Adjust for window offset and center
                self.mouse_x = max(-400, min(400, relative_x))  # Clamp to game bounds
                time.sleep(0.01)  # Small sleep to prevent excessive CPU usage
            except:
                continue

    def get_mouse_x_position(self):
        return self.mouse_x

    def stop(self):
        self.running = False
        self.thread.join()

pygame.mixer.init(buffer=512)

try:
    paddle_hit_sound = pygame.mixer.Sound("paddle_hit.wav")
    brick_break_sound = pygame.mixer.Sound("brick_break.wav")
    game_over_sound = pygame.mixer.Sound("game_over.wav")
    game_win_sound = pygame.mixer.Sound("game_win.wav")
    start_game_sound = pygame.mixer.Sound("start_game.wav")
    intro_sound = pygame.mixer.Sound("game_sound.wav.mp3")
except FileNotFoundError as e:
    print(f"Warning: Sound file missing - {e}. Sounds will be disabled.")
    paddle_hit_sound = brick_break_sound = game_over_sound = game_win_sound = start_game_sound = None

screen = turtle.Screen()
screen.title("Breakout Game")
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.tracer(0)
screen.register_shape("power.gif")

try:
    screen.bgpic("background.gif")
except turtle.TurtleGraphicsError:
    print("Warning: background.gif not found or invalid. Using black background.")

background_turtle = turtle.Turtle()
background_turtle.hideturtle()
background_turtle.color("gray20")
background_turtle.penup()
background_turtle.speed(0)
for _ in range(100):
    x = random.randint(-400, 400)
    y = random.randint(-300, 300)
    background_turtle.goto(x, y)
    background_turtle.dot(2)

FPS = 80
PINK = "pink"
WHITE = "white"
WIDTH, HEIGHT = 800, 600

planet_colors = [
    "#f8f0ff", "#d6b3ff", "#b56dff", "#9441e3", "#6a24b6", "#3f1061"
]

class Star:
    def __init__(self):
        self.x = random.randint(-WIDTH // 2, WIDTH // 2)
        self.y = random.randint(-HEIGHT // 2, HEIGHT // 2)
        self.size = random.uniform(1.0, 3.0)
        self.twinkle_speed = random.uniform(0.05, 0.2)
        self.phase = random.uniform(0, 2 * math.pi)

    def draw(self, turtle_obj, frame):
        size = self.size + math.sin(self.phase + frame * self.twinkle_speed) * 0.3
        turtle_obj.penup()
        turtle_obj.goto(self.x, self.y)
        turtle_obj.dot(int(size), WHITE)

class NebulaLine:
    def __init__(self):
        self.start = (random.randint(-WIDTH // 2, WIDTH // 2),
                      random.randint(-HEIGHT // 2, HEIGHT // 2))
        self.end = (self.start[0] + random.randint(-100, 100),
                    self.start[1] + random.randint(-100, 100))
        self.color = PINK

    def draw(self, turtle_obj):
        turtle_obj.penup()
        turtle_obj.goto(self.start)
        turtle_obj.pendown()
        turtle_obj.color(self.color)
        turtle_obj.goto(self.end)

class TitleLetter:
    def __init__(self, char, x, y):
        self.char = char
        self.x = x
        self.y = y

    def draw(self, turtle_obj, opacity=1.0):
        turtle_obj.penup()
        turtle_obj.goto(self.x, self.y)
        r, g, b = 255 * opacity, 255 * opacity, 255 * opacity
        turtle_obj.color((r/255, g/255, b/255))
        turtle_obj.write(self.char, align="center", font=("Courier", 24, "bold"))

def play_intro_animation(stars):
    if intro_sound:
        intro_sound.play()
    nebula_lines = [NebulaLine() for _ in range(30)]
    title_letters = [TitleLetter(char, -30 * len("BREAKOUT") + i * 70, 50) for i, char in enumerate("BREAKOUT")]
    title_letters.extend([TitleLetter(char, -35 * len("GAME!") + i * 70, -20) for i, char in enumerate("GAME!")])
    time.sleep(1)
    drawer = turtle.Turtle()
    drawer.hideturtle()
    drawer.speed(0)

    frame = 0
    anim_frame = 0
    total_frames = 240
    while anim_frame < total_frames:
        screen.update()
        drawer.clear()

        for star in stars:
            star.draw(drawer, frame)

        if 30 <= anim_frame < 120:
            for line in nebula_lines:
                if random.random() < 0.3:
                    line.draw(drawer)

        if 90 <= anim_frame < 210:
            title_frame = anim_frame - 90
            for i, letter in enumerate(title_letters):
                letter_start = i * 5
                if title_frame > letter_start:
                    fade_progress = min((title_frame - letter_start) / 30, 1.0)
                    letter.draw(drawer, opacity=fade_progress)

        if 210 <= anim_frame:
            for letter in title_letters:
                letter.draw(drawer, opacity=1.0)
            for line in nebula_lines:
                if random.random() < 0.3:
                    line.draw(drawer)

        frame += 1
        anim_frame += 1
        time.sleep(1 / FPS)
    drawer.clear()
    intro_sound.stop()

life_icons = []
def init_life_icons():
    global life_icons
    for icon in life_icons:
        icon.hideturtle()
    life_icons.clear()
    for i in range(lives):
        life = turtle.Turtle()
        life.shape("power.gif")
        life.penup()
        life.goto(300 + (i * 40), 260)
        life_icons.append(life)

game_started = False
last_speed_increase = 0

title_display = turtle.Turtle()
title_display.color("white")
title_display.penup()
title_display.hideturtle()

score_display = turtle.Turtle()
score_display.color("yellow")
score_display.penup()
score_display.hideturtle()

button_turtle = turtle.Turtle()
button_turtle.hideturtle()
button_turtle.color("white", "blue4")
button_turtle.penup()

paddle_turtle = turtle.Turtle()
paddle_turtle.hideturtle()
paddle_turtle.color("white")
paddle_turtle.fillcolor("white")
paddle_turtle.penup()

paddle_vertices = [
    (-50, -260),
    (-50, -240),
    (50, -240),
    (50, -260)
]
paddle_center = (0, -250)

ball_center = [0, 0]
ball_dx = 7
ball_dy = -7
ball_radius = 5

ball_pixels = turtle.Turtle()
ball_pixels.hideturtle()
ball_pixels.color("white")
ball_pixels.fillcolor("white")
ball_pixels.penup()

bricks = []
brick_rows = 5
brick_cols = 10
brick_width = 70
brick_height = 30
brick_spacing = 10
brick_start_y = 150

score = 0
lives = 3

def translate_rectangle(vertices, tx, ty):
    return [(x + tx, y + ty) for x, y in vertices]

def translate_circle(center_x, center_y, tx, ty):
    return center_x + tx, center_y + ty

X_MIN, X_MAX = -400, 400
Y_MIN, Y_MAX = -300, 300

INSIDE = 0
LEFT = 1
RIGHT = 2
BOTTOM = 4
TOP = 8

def compute_outcode(x, y):
    code = INSIDE
    if x < X_MIN:
        code |= LEFT
    elif x > X_MAX:
        code |= RIGHT
    if y < Y_MIN:
        code |= BOTTOM
    elif y > Y_MAX:
        code |= TOP
    return code

def cohen_sutherland_clip(x1, y1, x2, y2):
    outcode1 = compute_outcode(x1, y1)
    outcode2 = compute_outcode(x2, y2)
    accept = False
    done = False
    
    while not done:
        if outcode1 == 0 and outcode2 == 0:
            accept = True
            done = True
        elif outcode1 & outcode2 != 0:
            done = True
        else:
            outcode = outcode1 if outcode1 != 0 else outcode2
            if outcode & TOP:
                x = x1 + (x2 - x1) * (Y_MAX - y1) / (y2 - y1)
                y = Y_MAX
            elif outcode & BOTTOM:
                x = x1 + (x2 - x1) * (Y_MIN - y1) / (y2 - y1)
                y = Y_MIN
            elif outcode & RIGHT:
                y = y1 + (y2 - y1) * (X_MAX - x1) / (x2 - x1)
                x = X_MAX
            elif outcode & LEFT:
                y = y1 + (y2 - y1) * (X_MIN - x1) / (x2 - x1)
                x = X_MIN
            
            if outcode == outcode1:
                x1, y1 = x, y
                outcode1 = compute_outcode(x1, y1)
            else:
                x2, y2 = x, y
                outcode2 = compute_outcode(x2, y2)
    
    if accept:
        return (x1, y1), (x2, y2)
    return None

def midpoint_circle(x_center, y_center, radius):
    pixels = []
    x = 0
    y = radius
    d = 1 - radius
    
    pixels.extend([
        (x_center + x, y_center + y),
        (x_center + x, y_center - y),
        (x_center - x, y_center + y),
        (x_center - x, y_center - y),
        (x_center + y, y_center + x),
        (x_center + y, y_center - x),
        (x_center - y, y_center + x),
        (x_center - y, y_center - x)
    ])
    
    while x < y:
        x += 1
        if d < 0:
            d += 2 * x + 1
        else:
            y -= 1
            d += 2 * (x - y) + 1
        pixels.extend([
            (x_center + x, y_center + y),
            (x_center + x, y_center - y),
            (x_center - x, y_center + y),
            (x_center - x, y_center - y),
            (x_center + y, y_center + x),
            (x_center + y, y_center - x),
            (x_center - y, y_center + x),
            (x_center - y, y_center - x)
        ])
    
    pixels = list(set(pixels))
    sorted_pixels = sorted(pixels, key=lambda p: math.atan2(p[1] - y_center, p[0] - x_center))
    target_points = 24
    step = max(1, len(sorted_pixels) // target_points)
    ordered_pixels = sorted_pixels[::step]
    if ordered_pixels:
        ordered_pixels.append(ordered_pixels[0])
    return ordered_pixels

def draw_paddle():
    paddle_turtle.clear()
    if paddle_vertices:
        paddle_turtle.fillcolor("white")
        paddle_turtle.begin_fill()
        paddle_turtle.goto(paddle_vertices[0])
        for x, y in paddle_vertices[1:]:
            paddle_turtle.goto(x, y)
        paddle_turtle.goto(paddle_vertices[0])
        paddle_turtle.end_fill()

def draw_ball(x, y):
    ball_pixels.clear()
    pixels = midpoint_circle(x, y, ball_radius)
    if pixels:
        clipped_pixels = []
        for i in range(len(pixels) - 1):
            x1, y1 = pixels[i]
            x2, y2 = pixels[i + 1]
            clipped = cohen_sutherland_clip(x1, y1, x2, y2)
            if clipped:
                (cx1, cy1), (cx2, cy2) = clipped
                if not clipped_pixels or clipped_pixels[-1] != (cx1, cy1):
                    clipped_pixels.append((cx1, cy1))
                clipped_pixels.append((cx2, cy2))
        
        if clipped_pixels:
            clipped_pixels.append(clipped_pixels[0])
            ball_pixels.fillcolor("white")
            ball_pixels.begin_fill()
            ball_pixels.goto(clipped_pixels[0])
            for px, py in clipped_pixels[1:]:
                ball_pixels.goto(px, py)
            ball_pixels.goto(clipped_pixels[0])
            ball_pixels.end_fill()

def draw_button(x, y, width, height, text):
    button_turtle.clear()
    button_turtle.goto(x - width/2, y - height/2)
    button_turtle.begin_fill()
    button_turtle.goto(x - width/2, y + height/2)
    button_turtle.goto(x + width/2, y + height/2)
    button_turtle.goto(x + width/2, y - height/2)
    button_turtle.goto(x - width/2, y - height/2)
    button_turtle.end_fill()
    button_turtle.goto(x, y - 10)
    button_turtle.write(text, align="center", font=("Fridericka the Great", 16, "bold"))

def move_paddle(x, y):
    if game_started:
        global paddle_vertices, paddle_center
        tx = x - paddle_center[0]
        ty = 0
        new_center_x = paddle_center[0] + tx
        if new_center_x < -350:
            tx = -350 - paddle_center[0]
        elif new_center_x > 350:
            tx = 350 - paddle_center[0]
        paddle_vertices = translate_rectangle(paddle_vertices, tx, ty)
        paddle_center = (paddle_center[0] + tx, paddle_center[1] + ty)
        draw_paddle()

def init_bricks():
    global bricks
    bricks = []
    for row in range(brick_rows):
        for col in range(brick_cols):
            brick = turtle.Turtle()
            brick.shape("square")
            brick.color("red3")
            brick.shapesize(stretch_wid=brick_height/20, stretch_len=brick_width/20)
            brick.penup()
            x = -395 + col * (brick_width + brick_spacing) + brick_width / 2
            y = brick_start_y - row * (brick_height + brick_spacing)
            brick.goto(x, y)
            bricks.append(brick)

def show_title_screen():
    title_display.clear()
    title_display.goto(0, 50)
    title_display.write("Breakout Game\n", align="center", font=("Fridericka the Great", 36, "bold"))
    title_display.goto(0, -10)
    title_display.write(" Move mouse to control paddle\n             Break all bricks", align="center", font=("Fridericka the Great", 16, "normal"))
    draw_button(0, -100, 100, 40, "Start")
    screen.onclick(check_button_click)
    screen.update()

def check_button_click(x, y):
    if not game_started:
        if -50 <= x <= 50 and -120 <= y <= -80:
            if start_game_sound:
                start_game_sound.play()
            start_game()
    elif lives == 0 or not bricks:
        if -50 <= x <= 50 and -120 <= y <= -80:
            restart_game()

def start_game():
    global game_started, score, lives, ball_dx, ball_dy
    if not game_started:
        game_started = True
        title_display.clear()
        button_turtle.clear()
        screen.onclick(None)
        init_bricks()
        score = 0
        lives = 3
        ball_dx = 7
        ball_dy = -7
        init_life_icons()
        score_display.goto(-350, 250)
        score_display.write(f"Score: {score}", font=("Fridericka the Great", 16, "bold"))
        draw_paddle()
        screen.listen()
        game_loop()

def restart_game():
    global game_started, score, lives, ball_center, ball_dx, ball_dy, last_speed_increase, life_icons, powerups, powerup_turtles, mouse_tracker
    game_started = False
    score = 0
    lives = 3
    ball_center = [0, 0]
    ball_dx = 7
    ball_dy = -7
    last_speed_increase = 0
    
    for icon in life_icons:
        icon.hideturtle()
    life_icons.clear()
    
    score_display.clear()
    button_turtle.clear()
    paddle_turtle.clear()
    ball_pixels.clear()
    for brick in bricks:
        brick.hideturtle()
    bricks.clear()
    screen.onclick(None)
    
    # Stop and reinitialize mouse tracker
    mouse_tracker.stop()
    mouse_tracker = MouseTracker(screen)
    
    for powerup in powerups:
        powerup.turtle.hideturtle()
    powerups = []
    powerup_turtles = []
    show_title_screen()

mouse_tracker = MouseTracker(screen)
screen.onscreenclick(None)

LIFE_CHARGE_SHAPE = "life_charge.gif"
CHARGE_SPAWN_RATE = 300
CHARGE_FALL_SPEED = 2
CHARGE_DURATION = 180

life_charges = []
charge_spawn_timer = 0

class LifeCharge:
    def __init__(self):
        self.x = random.randint(-350, 350)
        self.y = 300
        self.turtle = turtle.Turtle()
        self.turtle.shape(LIFE_CHARGE_SHAPE)
        self.turtle.penup()
        self.turtle.goto(self.x, self.y)
        self.collected = False
        self.lifetime = CHARGE_DURATION

POWERUP_SPEED = 3
POWERUP_CHANCE = 0.3
POWERUP_SHAPE = "powerup.gif"

powerups = []
powerup_turtles = []

def update_life_display():
    global life_icons
    for icon in life_icons:
        icon.hideturtle()
    life_icons.clear()
    for i in range(lives):
        life = turtle.Turtle()
        life.shape("power.gif")
        life.penup()
        life.goto(350 + (i * 40), 260)
        life_icons.append(life)
    score_display.clear()
    score_display.goto(-350, 250)
    score_display.write(f"Score: {score}", font=("Fridericka the Great", 16, "bold"))

def spawn_powerup():
    powerup = PowerUp()
    powerups.append(powerup)
    powerup_turtles.append(powerup.turtle)
    charrge = LifeCharge()
    life_charges.append(charrge)

class PowerUp:
    def __init__(self):
        self.x = random.randint(-350, 350)
        self.y = 300
        self.speed = POWERUP_SPEED
        self.turtle = turtle.Turtle()
        self.turtle.shape(POWERUP_SHAPE)
        self.turtle.penup()
        self.turtle.goto(self.x, self.y)
        self.active = True

def lose_life():
    global lives, life_charges
    lives -= 1
    update_life_display()
    spawn_powerup()

def update_powerups():
    global powerups, powerup_turtles
    to_remove = []
    for i, powerup in enumerate(powerups):
        if powerup.active:
            powerup.y -= powerup.speed
            powerup.turtle.goto(powerup.x, powerup.y)
            if powerup.y < -300:
                powerup.turtle.hideturtle()
                to_remove.append(i)
    for i in sorted(to_remove, reverse=True):
        powerups.pop(i)
        powerup_turtles.pop(i)

def check_powerup_collisions():
    global lives, powerups, powerup_turtles
    to_remove = []
    paddle_left = paddle_vertices[0][0]
    paddle_right = paddle_vertices[2][0]
    for i, powerup in enumerate(powerups):
        if (powerup.active and
            -260 <= powerup.y <= -240 and
            paddle_left <= powerup.x <= paddle_right):
            lives = min(lives + 1, 3)
            update_life_display()
            powerup.turtle.hideturtle()
            to_remove.append(i)
    for i in sorted(to_remove, reverse=True):
        powerups.pop(i)
        powerup_turtles.pop(i)

def update_charges():
    global life_charges
    charges_to_remove = []
    for i, charge in enumerate(life_charges):
        if not charge.collected:
            charge.y -= CHARGE_FALL_SPEED
            charge.turtle.goto(charge.x, charge.y)
            if charge.y < -320:
                charge.turtle.hideturtle()
                charges_to_remove.append(i)
    for i in sorted(charges_to_remove, reverse=True):
        life_charges.pop(i)

def check_charge_collisions():
    global lives, life_charges
    paddle_left = paddle_vertices[0][0]
    paddle_right = paddle_vertices[2][0]
    for charge in life_charges:
        if not charge.collected:
            if (-260 <= charge.y <= -240 and 
                paddle_left <= charge.x <= paddle_right):
                charge.collected = True
                charge.turtle.hideturtle()
                lives = min(lives + 1, 3)
                update_life_display()

def game_loop():
    if not game_started:
        return
    mouse_x = mouse_tracker.get_mouse_x_position()
    if mouse_x is not None:
        move_paddle(mouse_x, 0)

    global score, lives, ball_center, ball_dx, ball_dy, last_speed_increase, powerups, powerup_turtles, life_charges, charge_spawn_timer
    ball_center = translate_circle(ball_center[0], ball_center[1], ball_dx, ball_dy)
    draw_ball(ball_center[0], ball_center[1])
    update_powerups()
    check_powerup_collisions()

    # Wall collisions
    if ball_center[0] > 390 or ball_center[0] < -390:
        ball_dx *= -1
    if ball_center[1] > 290:
        ball_dy *= -1
    
    # Paddle collision
    paddle_left = paddle_vertices[0][0]
    paddle_right = paddle_vertices[2][0]
    hit_paddle = False
    if -260 <= ball_center[1] <= -240 and paddle_left < ball_center[0] < paddle_right:
        ball_dy *= -1
        if paddle_hit_sound:
            paddle_hit_sound.play()
        hit_paddle = True
    
    # Brick collisions
    for brick in bricks[:]:
        bx, by = brick.xcor(), brick.ycor()
        if (by - brick_height/2 < ball_center[1] < by + brick_height/2 and
            bx - brick_width/2 < ball_center[0] < bx + brick_width/2):
            ball_dy *= -1
            bricks.remove(brick)
            brick.hideturtle()
            score += 10
            if brick_break_sound:
                brick_break_sound.play()
            if score // 100 > last_speed_increase // 100:
                ball_dx *= 1.1
                ball_dy *= 1.1
                last_speed_increase = score
                print(f"Speed increased at score {score}! ball_dx: {ball_dx:.2f}, ball_dy: {ball_dy:.2f}")
            score_display.clear()
            score_display.write(f"Score: {score}", font=("Fridericka the Great", 16, "bold"))
            break

    # Life loss if ball goes below paddle
    if ball_center[1] < -260 and not hit_paddle:
        lives -= 1
        if life_icons:
            life_icons[-1].hideturtle()
            life_icons.pop()
        score_display.clear()
        score_display.write(f"Score: {score}", font=("Fridericka the Great", 16, "bold"))
        ball_center = [0, 0]  # Reset to center
        ball_dx = random.choice([7, -7]) * (1.1 ** (last_speed_increase // 100))
        ball_dy = -7 * (1.1 ** (last_speed_increase // 100))
    
    # Game over
    if lives == 0:
        for brick in bricks:
            brick.hideturtle()
        ball_pixels.clear()
        paddle_turtle.clear()
        score_display.clear()
        score_display.goto(0, 0)
        score_display.write("    Game Over!\n Final Score: {}".format(score), align="center", font=("Fridericka the Great", 36, "bold"))
        if game_over_sound:
            game_over_sound.play()
        draw_button(0, -100, 100, 40, "Restart")
        screen.onclick(check_button_click)
        screen.update()
        return
    
    # Win condition
    if not bricks:
        for brick in bricks:
            brick.hideturtle()
        ball_pixels.clear()
        paddle_turtle.clear()
        score_display.clear()
        score_display.goto(0, 0)
        score_display.write("       You Win! \n Final Score: {}".format(score), align="center", font=("Fridericka the Great", 36, "bold"))
        if game_win_sound:
            game_win_sound.play()
        draw_button(0, -100, 100, 40, "Restart")
        screen.onclick(check_button_click)
        screen.update()
        return
    
    screen.update()
    screen.ontimer(game_loop, 1000 // 60)

    for charge in life_charges:
        charge.turtle.hideturtle()
    life_charges = []
    charge_spawn_timer = 0

def on_close():
    global game_started
    game_started = False
    mouse_tracker.stop()
    screen.bye()

screen.getcanvas().winfo_toplevel().protocol("WM_DELETE_WINDOW", on_close)
stars = [Star() for _ in range(100)]
play_intro_animation(stars)
show_title_screen()
screen.mainloop()