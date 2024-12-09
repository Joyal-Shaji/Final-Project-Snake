import tkinter
import random
from tkinter import messagebox  # Import for the score keeper

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

# Add global variable for bonus food
bonus_food = None
bonus_timer = 0

# Function to generate bonus food
def generate_bonus_food():
    global bonus_food, bonus_timer
    bonus_food = block(random.randint(0, columns - 1) * tileSize, random.randint(0, rows - 1) * tileSize)
    bonus_timer = 50  # Bonus food will disappear after 50 frames

# Function to change snake direction
def change_direction(e):  # e for event
    global velocityX, velocityY
    if endGame:
        return

    if (e.keysym == "Up" and velocityY != 1):  # != 1 makes sure that we are not travelling downwards
        velocityX = 0  # 0 because we are not moving horizontally
        velocityY = -1
    elif (e.keysym == "Down" and velocityY != -1):  # != to -1 makes sure that we are not travelling up
        velocityX = 0
        velocityY = 1
    elif (e.keysym == "Left" and velocityX != 1):  # != to 1 makes sure that we are not travelling to the right
        velocityX = -1
        velocityY = 0
    elif (e.keysym == "Right" and velocityX != -1):  # != to -1 makes sure that we are not travelling to the left
        velocityX = 1
        velocityY = 0

# Update moveSnake to handle bonus food
def moveSnake():
    global snake, food, snakeBody, endGame, score, food_count, level, speed, bonus_food, bonus_timer
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

    # Collision with bonus food
    if bonus_food and snake.x == bonus_food.x and snake.y == bonus_food.y:
        score += 5  # Bonus food gives extra points
        bonus_food = None  # Remove bonus food after it's eaten

    # Collision with regular food
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
            speed = max(50, speed - 10)

        # Randomly generate bonus food
        if random.randint(1, 5) == 1:  # 20% chance to spawn bonus food
            generate_bonus_food()

    # Move the snake's body
    for i in range(len(snakeBody) - 1, 0, -1):
        snakeBody[i].x = snakeBody[i - 1].x
        snakeBody[i].y = snakeBody[i - 1].y

    if snakeBody:
        snakeBody[0].x = snake.x
        snakeBody[0].y = snake.y

    snake.x += velocityX * tileSize
    snake.y += velocityY * tileSize

    # Handle bonus timer
    if bonus_food:
        bonus_timer -= 1
        if bonus_timer <= 0:
            bonus_food = None  # Remove bonus food when timer runs out

# Update draw function to render bonus food
def draw():
    global snake
    moveSnake()
    canvas.delete("all")

    # Draw score and level
    canvas.create_text(10, 10, anchor="nw", text=f"Score: {score}", font=("Arial", 16), fill="black")
    canvas.create_text(window_size // 2, 10, anchor="n", text=f"Level: {level}", font=("Arial", 16), fill="black")

    # Draw the food
    canvas.create_rectangle(food.x, food.y, food.x + tileSize, food.y + tileSize, fill="red")

    # Draw the bonus food
    if bonus_food:
        canvas.create_oval(bonus_food.x, bonus_food.y, bonus_food.x + tileSize, bonus_food.y + tileSize, fill="gold")

    # Draw the snake
    canvas.create_rectangle(snake.x, snake.y, snake.x + tileSize, snake.y + tileSize, fill="lime green")
    for tile in snakeBody:
        canvas.create_rectangle(tile.x, tile.y, tile.x + tileSize, tile.y + tileSize, fill="lime green")

    if not endGame:
        window.after(speed, draw)

# Display Game Over message
def display_game_over():
    global score
    messagebox.showinfo("Game Over", f"Game Over!\nYour final score: {score}\nLevel: {level}")
    window.destroy()  # Close the game window

draw()
# Run the Tkinter event loop
window.bind("<KeyPress>", change_direction)  # Everytime a key is released
window.mainloop()
