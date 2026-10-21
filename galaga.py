import turtle
import random
import sys

# Set up screen
screen = turtle.Screen()
screen.title("Python Space Invaders Mini")
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.tracer(0)

# Player setup
player = turtle.Turtle()
player.shape("square")
player.color("green")
player.shapesize(stretch_wid=1, stretch_len=3)  # 60x20 pixel ship
player.penup()
player.goto(0, -250)

# Bullet setup
bullet = turtle.Turtle()
bullet.shape("square")
bullet.color("yellow")
bullet.shapesize(stretch_wid=0.8, stretch_len=0.2)
bullet.penup()
bullet.hideturtle()
bullet_state = "ready"  # "ready" means ready to fire, "fire" means currently moving
bullet_speed = 15

# Enemy list
enemies = []

# Score display
score = 0
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.hideturtle()
score_pen.goto(-370, 250)
score_pen.write("Score: 0", font=("Arial", 18, "normal"))

# Movement flags
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

def fire_bullet():
    global bullet_state
    if bullet_state == "ready":
        bullet_state = "fire"
        x = player.xcor()
        y = player.ycor() + 20
        bullet.goto(x, y)
        bullet.showturtle()

# Keyboard bindings
screen.listen()
screen.onkeypress(start_left, "Left")
screen.onkeyrelease(stop_left, "Left")
screen.onkeypress(start_right, "Right")
screen.onkeyrelease(stop_right, "Right")
screen.onkeypress(start_left, "a")
screen.onkeyrelease(stop_left, "a")
screen.onkeypress(start_right, "d")
screen.onkeyrelease(stop_right, "d")
screen.onkeypress(fire_bullet, "space")

# Game variables
spawn_timer = 0
enemy_speed = 2.0
game_running = True

def update():
    global bullet_state, score, enemy_speed, spawn_timer, game_running
    if not game_running:
        return

    # Move player smoothly
    x = player.xcor()
    if moving_left and x > -360:
        player.setx(x - 9)
    if moving_right and x < 360:
        player.setx(x + 9)

    # Move the bullet
    if bullet_state == "fire":
        y = bullet.ycor()
        bullet.sety(y + bullet_speed)
        
        # Reset bullet if it goes off the top of the screen
        if bullet.ycor() > 300:
            bullet.hideturtle()
            bullet_state = "ready"

    # Spawn enemies over time
    spawn_timer += 1
    if spawn_timer > 35:
        enemy = turtle.Turtle()
        enemy.shape("square")
        enemy.color("red")
        enemy.shapesize(stretch_wid=1.5, stretch_len=1.5)
        enemy.penup()
        enemy_x = random.randint(-370, 370)
        enemy.goto(enemy_x, 320)
        enemies.append(enemy)
        spawn_timer = 0

    # Move and update enemies
    for enemy in enemies[:]:
        enemy.sety(enemy.ycor() - enemy_speed)

        # Check for collision between bullet and enemy
        if bullet_state == "fire" and bullet.distance(enemy) < 20:
            bullet.hideturtle()
            bullet_state = "ready"
            enemy.hideturtle()
            enemies.remove(enemy)
            score += 1
            enemy_speed += 0.05  # Gets faster as you score more!
            score_pen.clear()
            score_pen.write(f"Score: {score}", font=("Arial", 18, "normal"))
            continue
        # Check if enemy reached the bottom (Game Over)
        if enemy.ycor() < -270:
            game_running = False
            score_pen.clear()
            score_pen.goto(0, 0)
            score_pen.write(f"GAME OVER\nFinal Score: {score}", align="center", font=("Arial", 28, "bold"))
            return
        # Check if enemy hits the player directly
        if player.distance(enemy) < 30:
            game_running = False
            score_pen.clear()
            score_pen.goto(0, 0)
            score_pen.write(f"GAME OVER\nFinal Score: {score}", align="center", font=("Arial", 28, "bold"))
            return

    screen.update()
    screen.ontimer(update, 20)

# Start game loop
screen.ontimer(update, 20)
screen.mainloop()