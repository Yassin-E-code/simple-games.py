import turtle
import random
import sys

# Set up screen
screen = turtle.Screen()
screen.title("Python Dodge Game")
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.tracer(0)  # Turns off automatic screen updates for smooth rendering

# Player setup
player = turtle.Turtle()
player.shape("square")
player.color("blue")
player.shapesize(stretch_wid=1, stretch_len=4)  # 80x20 pixel bar
player.penup()
player.goto(0, -250)

# Movement flags for smooth holding keys
moving_left = False
moving_right = False

def start_left():
    global moving_left
    moving_left = True

def stop_left():
    global moving_left
    moving_left = False

def start_right():
    global moving_right
    moving_right = True

def stop_right():
    global moving_right
    moving_right = False

# Keyboard bindings (Supports Arrow keys and A/D keys)
screen.listen()
screen.onkeypress(start_left, "Left")
screen.onkeyrelease(stop_left, "Left")
screen.onkeypress(start_right, "Right")
screen.onkeyrelease(stop_right, "Right")
screen.onkeypress(start_left, "a")
screen.onkeyrelease(stop_left, "a")
screen.onkeypress(start_right, "d")
screen.onkeyrelease(stop_right, "d")

# Score display
score = 0
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.hideturtle()
score_pen.goto(-370, 250)
score_pen.write("Score: 0", font=("Arial", 18, "normal"))

# Game variables
enemies = []
enemy_speed = 3.0   # Regular, comfortable starting speed
spawn_timer = 0
game_running = True

def update():
    global score, enemy_speed, spawn_timer, game_running
    if not game_running:
        return

    # Move player smoothly based on keys held down
    x = player.xcor()
    if moving_left and x > -360:
        player.setx(x - 9)
    if moving_right and x < 360:
        player.setx(x + 9)

    # Spawn enemies over time
    spawn_timer += 1
    if spawn_timer > 30:  # Spawn roughly every 0.5 seconds
        enemy = turtle.Turtle()
        enemy.shape("square")
        enemy.color("red")
        enemy.shapesize(stretch_wid=2, stretch_len=2)  # 40x40 pixel enemy
        enemy.penup()
        enemy_x = random.randint(-370, 370)
        enemy.goto(enemy_x, 320)
        enemies.append(enemy)
        spawn_timer = 0

    # Move and update enemies
    for enemy in enemies[:]:
        enemy.sety(enemy.ycor() - enemy_speed)
        
        # Remove enemies that fall off screen, increase score, and accelerate speed
        if enemy.ycor() < -320:
            enemy.hideturtle()
            enemies.remove(enemy)
            score += 1
            enemy_speed += 0.05  # Gradually speeds up as score increases!
            score_pen.clear()
            score_pen.write(f"Score: {score}", font=("Arial", 18, "normal"))

        # Collision detection
        if player.distance(enemy) < 35:
            game_running = False
            score_pen.clear()
            score_pen.goto(0, 0)
            score_pen.write(f"GAME OVER\nFinal Score: {score}", align="center", font=("Arial", 28, "bold"))
            return

    screen.update()
    screen.ontimer(update, 20)  # Refresh loop (~50 frames per second)

# Start the game loop
screen.ontimer(update, 20)
screen.mainloop()