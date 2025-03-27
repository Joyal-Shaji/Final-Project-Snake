import tkinter
import random
from tkinter import messagebox  # Import for the score keeper
import pygame # for sounds

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
speed = 150  # Initial speed (in ms)
obstacles = []  # list of obstacle blocks
obj_spawn_req = 5

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
bonus_food_sfx = pygame.mixer.Sound("Cartoon Munch Sound Effect [ ezmp3.cc ].mp3")

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


# Update moveSnake to handle bonus food
def moveSnake():
    global snake, food, snakeBody, endGame, score, food_count, level, speed, bonus_food, bonus_timer, \
        obstacle, obj_spawn_req
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
        bonus_food_sfx.play()
        score += 5  # Bonus food gives extra points
        bonus_food = None  # Remove bonus food after it's eaten

    # Collision with regular food
    if snake.x == food.x and snake.y == food.y:
        eat_sfx.play()  # play the eating sfx
        score += 1  # Increment score
        food_count += 1  # Increment food count
        # Add a new block to the tail of the snake
        if snakeBody:
            last_block = snakeBody[-1]
            snakeBody.append(block(last_block.x, last_block.y))
        else:
            snakeBody.append(block(snake.x, snake.y))     # Add a block if the body is empty

        # Reposition the food
        food.x = random.randint(0, columns - 1) * tileSize
        food.y = random.randint(0, rows - 1) * tileSize

        # Increase speed and level up after 5 pieces of food
        if food_count >= 5:
            level_up_sfx.play()
            level += 1
            food_count = 0  # Reset food count after level up
            speed -= 10  # Increase speed by reducing delay (faster snake)

        # Randomly generate bonus food
        if random.randint(1, 5) == 1:  # 20% chance to spawn bonus food
            generate_bonus_food()

        # spawning the obstacles
        if food_count % obj_spawn_req == 0:  # if the snake eats 5 food it will spawn and obstacle
            spawn_obstacle()
    # collision with obstacle
    for obstacle in obstacles:
        if snake.x == obstacle.x and snake.y == obstacle.y:
            endGame = True
            display_game_over()
            return

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

    # Handle bonus timer
    if bonus_food:
        bonus_timer -= 1
        if bonus_timer <= 0:
            bonus_food = None  # Remove bonus food when timer runs out


def spawn_obstacle():
    global obstacle
    while True:
        obstacle = block(random.randint(0, columns - 1) * tileSize, random.randint(0, rows - 1) * tileSize)
        # Making sure that the obstacle does not overlap with the snake
        if ((obstacle.x != food.x or obstacle.y != food.y)
                and all(obstacle.x != segment.x or obstacle.y != segment.y for segment in snakeBody)):
            obstacles.append(obstacle)
            break


# Update draw function to render bonus food
def draw():
    global snake, obstacle
    moveSnake()
    canvas.delete("all")    # clears the non significant squares being created on each move

    # Draw score and level
    canvas.create_text(10, 10, anchor="nw", text=f"Score: {score}", font=("Arial", 16), fill="black")
    canvas.create_text(window_size // 2, 10, anchor="n", text=f"Level: {level}", font=("Arial", 16), fill="black")

    # Draw the food
    canvas.create_rectangle(food.x, food.y, food.x + tileSize, food.y + tileSize, fill="red")

    # Draw the bonus food
    if bonus_food:
        canvas.create_oval(bonus_food.x, bonus_food.y, bonus_food.x + tileSize, bonus_food.y + tileSize, fill="gold")

    # Draw the obstacles
    for obstacle in obstacles:
        canvas.create_rectangle(obstacle.x, obstacle.y, obstacle.x + tileSize, obstacle.y + tileSize, fill="#916d0a",
                                outline="black")
    # Draw the snake
    canvas.create_rectangle(snake.x, snake.y, snake.x + tileSize, snake.y + tileSize, fill="lime green")
    for tile in snakeBody:
        canvas.create_rectangle(tile.x, tile.y, tile.x + tileSize, tile.y + tileSize, fill="lime green")

    if not endGame:
        window.after(speed, draw)


# Display Game Over message
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
