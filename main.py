import tkinter
import random
from tkinter import messagebox  # Import for the score keeper
import pygame

# Forming the grid that I first worked out on paper
rows = 25
columns = 25
tileSize = 25

# Calculate window dimensions
window_size = tileSize * rows  # Use the same value for width and height to make the window square


class block:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# Creating the game window
window = tkinter.Tk()
window.title("SNAKE GAME")
window.resizable(False, False)  # Prevent resizing of the window

# Create a canvas and pack it into the window
canvas = tkinter.Canvas(window, bg="light green", width=window_size, height=window_size, borderwidth=0,
                        highlightthickness=0)
canvas.pack()

# Update window to get accurate dimensions
window.update()

# Centers the window on the screen
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_x = int((screen_width / 2) - (window_size / 2))
window_y = int((screen_height / 2) - (window_size / 2))

window.geometry(f"{window_size}x{window_size}+{window_x}+{window_y}")

# Initialize the game
snake = block(5 * tileSize, 5 * tileSize)
food = block(10 * tileSize, 10 * tileSize)
snakeBody = []  # multiple blocks
velocityX = 0
velocityY = 0
endGame = False
score = 0  # Initialize the score
level = 1  # Start at level 1
food_count = 0  # To keep track of how much food has been eaten
speed = 100  # Initial speed (in ms)

# SFX
pygame.init()
background_song = (pygame.mixer.music.load
                   ("Take On Me (8 Bit Remix Cover Version) [Tribute to A-ha] - 8 Bit Universe [ ezmp3.cc ].mp3"))
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0)
change_direction_sfx = pygame.mixer.Sound("sound3.mp3")
eat_sfx = pygame.mixer.Sound("zapsplat_cartoon_bite_eat_crunch_single_002_58271.mp3")
die_sfx = pygame.mixer.Sound("zapsplat_multimedia_game_sound_8_bit_blip_descending_negative_die_112015.mp3")
level_up_sfx = pygame.mixer.Sound("sound2.wav")



def change_direction(e):  # e for event
    global velocityX, velocityY
    if endGame:
        return

    if (e.keysym == "Up" and velocityY != 1):  # != 1 makes sure that we are not travelling downwards
        change_direction_sfx.play()
        velocityX = 0  # 0 because we are not moving horizontally
        velocityY = -1
    elif (e.keysym == "Down" and velocityY != -1):  # != to -1 makes sure that we are not travelling up
        change_direction_sfx.play()
        velocityX = 0
        velocityY = 1
    elif (e.keysym == "Left" and velocityX != 1):  # != to 1 makes sure that we are not travelling to the right
        change_direction_sfx.play()
        velocityX = -1
        velocityY = 0
    elif (e.keysym == "Right" and velocityX != -1):  # != to -1 makes sure that we are not travelling to the left
        change_direction_sfx.play()
        velocityX = 1
        velocityY = 0


def moveSnake():
    global snake, food, snakeBody, endGame, score, food_count, level, speed
    if endGame:
        return

    # Collision with walls
    if snake.x < 0 or snake.x >= window_size or snake.y < 0 or snake.y >= window_size:
        endGame = True
        display_game_over()
        return

    # Collision with itself
    for segment in snakeBody:
        if snake.x == segment.x and snake.y == segment.y:
            endGame = True
            display_game_over()
            return

    # Collision with food
    if snake.x == food.x and snake.y == food.y:
        eat_sfx.play()  # plays the eating sfx
        score += 1  # Increment score
        food_count += 1  # Increment food count
        # Add a new block to the tail of the snake
        if snakeBody:
            last_block = snakeBody[-1]
            snakeBody.append(block(last_block.x, last_block.y))
        else:
            snakeBody.append(block(snake.x, snake.y))  # Add a block if the body is empty

        # Reposition the food
        food.x = random.randint(0, columns - 1) * tileSize
        food.y = random.randint(0, rows - 1) * tileSize

        # Increase speed and level up after 6 pieces of food
        if food_count >= 5:
            level_up_sfx.play()
            level += 1
            food_count = 0  # Reset food count after level up
            speed -= 10  # Increase speed by reducing delay (faster snake)

    # Move the snake's body
    for i in range(len(snakeBody) - 1, 0, -1):
        snakeBody[i].x = snakeBody[i - 1].x
        snakeBody[i].y = snakeBody[i - 1].y

    if snakeBody:
        snakeBody[0].x = snake.x
        snakeBody[0].y = snake.y

    # Move the snake's head
    snake.x += velocityX * tileSize
    snake.y += velocityY * tileSize


def draw():
    global snake
    moveSnake()

    canvas.delete("all")  # clears the non significant squares being created on each move

    # Draw the score and level
    canvas.create_text(10, 10, anchor="nw", text=f"Score: {score}", font=("Arial", 16), fill="black")
    canvas.create_text(window_size // 2, 10, anchor="n", text=f"Level: {level}", font=("Arial", 16), fill="black")

    # Draw the food
    canvas.create_rectangle(food.x, food.y, food.x + tileSize, food.y + tileSize, fill="red")

    # Draw the snake
    canvas.create_rectangle(snake.x, snake.y, snake.x + tileSize, snake.y + tileSize, fill="lime green")

    for tile in snakeBody:
        canvas.create_rectangle(tile.x, tile.y, tile.x + tileSize, tile.y + tileSize, fill="lime green")

    if not endGame:
        window.after(speed, draw)  # draws the rectangle every X ms (speed control)


def display_game_over():
    pygame.mixer.music.stop()
    pygame.time.delay(100)
    die_sfx.play()
    global score
    messagebox.showinfo("Game Over", f"Game Over!\nYour final score: {score}\nLevel: {level}")
    window.destroy()  # Close the game window


draw()
# Run the Tkinter event loop
window.bind("<KeyPress>", change_direction)  # Everytime a key is released
window.mainloop()

# Define a new class for power-ups
class PowerUp:
    def __init__(self, x, y, effect_type):
        self.x = x
        self.y = y
        self.effect_type = effect_type  # e.g., "slow", "score_boost", "invincible"

# Initialize power-ups
power_up = None  # Initially, no power-up is on the grid
power_up_duration = 0  # Track duration of the current power-up effect
active_effect = None  # Track the current active effect

def spawn_power_up():
    global power_up
    if random.random() < 0.1:  # 10% chance of spawning a power-up after food is eaten
        effect_type = random.choice(["slow", "score_boost", "invincible"])
        power_up_x = random.randint(0, columns - 1) * tileSize
        power_up_y = random.randint(0, rows - 1) * tileSize
        power_up = PowerUp(power_up_x, power_up_y, effect_type)

def apply_power_up():
    global speed, score, power_up_duration, active_effect
    if power_up.effect_type == "slow":
        speed += 30  # Slow down the snake temporarily
    elif power_up.effect_type == "score_boost":
        score += 5  # Grant an instant score boost
    elif power_up.effect_type == "invincible":
        active_effect = "invincible"  # Make the snake invincible temporarily
    power_up_duration = 50  # Set duration for the power-up effect

def check_power_up_collision():
    global power_up
    if power_up and snake.x == power_up.x and snake.y == power_up.y:
        apply_power_up()
        power_up = None  # Remove the power-up after collision

def update_power_up_effect():
    global power_up_duration, active_effect, speed
    if power_up_duration > 0:
        power_up_duration -= 1
    else:
        if active_effect == "invincible":
            active_effect = None  # Reset invincibility after duration
        elif speed > 100:
            speed -= 30  # Reset speed if slowed down
        active_effect = None

# Modify the moveSnake function to include power-up collision checks
def moveSnake():
    global snake, food, snakeBody, endGame, score, food_count, level, speed
    if endGame:
        return

    # Collision with walls (unless invincible)
    if not active_effect == "invincible":
        if snake.x < 0 or snake.x >= window_size or snake.y < 0 or snake.y >= window_size:
            endGame = True
            display_game_over()
            return

    # Collision with itself (unless invincible)
    if not active_effect == "invincible":
        for segment in snakeBody:
            if snake.x == segment.x and snake.y == segment.y:
                endGame = True
                display_game_over()
                return

    # Collision with food
    if snake.x == food.x and snake.y == food.y:
        score += 1
        food_count += 1
        if snakeBody:
            last_block = snakeBody[-1]
            snakeBody.append(block(last_block.x, last_block.y))
        else:
            snakeBody.append(block(snake.x, snake.y))
        food.x = random.randint(0, columns - 1) * tileSize
        food.y = random.randint(0, rows - 1) * tileSize

        if food_count >= 5:
            level += 1
            food_count = 0
            speed -= 10
        
        spawn_power_up()  # Attempt to spawn a power-up after food is eaten

    # Check collision with power-up
    check_power_up_collision()

    # Update power-up effect duration
    update_power_up_effect()

    # Move the snake's body
    for i in range(len(snakeBody) - 1, 0, -1):
        snakeBody[i].x = snakeBody[i - 1].x
        snakeBody[i].y = snakeBody[i - 1].y

    if snakeBody:
        snakeBody[0].x = snake.x
        snakeBody[0].y = snake.y

    # Move the snake's head
    snake.x += velocityX * tileSize
    snake.y += velocityY * tileSize

# Modify the draw function to include power-ups
def draw():
    global snake
    moveSnake()

    canvas.delete("all")

    canvas.create_text(10, 10, anchor="nw", text=f"Score: {score}", font=("Arial", 16), fill="black")
    canvas.create_text(window_size // 2, 10, anchor="n", text=f"Level: {level}", font=("Arial", 16), fill="black")

    canvas.create_rectangle(food.x, food.y, food.x + tileSize, food.y + tileSize, fill="red")

    if power_up:
        color = "blue" if power_up.effect_type == "slow" else "gold" if power_up.effect_type == "score_boost" else "purple"
        canvas.create_rectangle(power_up.x, power_up.y, power_up.x + tileSize, power_up.y + tileSize, fill=color)

    canvas.create_rectangle(snake.x, snake.y, snake.x + tileSize, snake.y + tileSize, fill="lime green")

    for tile in snakeBody:
        canvas.create_rectangle(tile.x, tile.y, tile.x + tileSize, tile.y + tileSize, fill="lime green")

    if not endGame:
        window.after(speed, draw)
