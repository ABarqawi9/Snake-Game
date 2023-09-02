from tkinter import *
import random

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 50
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#C0C0C0"
FOOD_COLOR = "#FFD700"
BACKGROUND_COLOR = "#000000"

class Snake:

    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE)
            self.squares.append(square)

class Food:

    def __init__(self):
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE)-1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def next_turn(snake, food):
    global direction

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score:{}".format(score))
        canvas.delete("food")
        food = Food()
        # Change snake color to gold
        canvas.itemconfig(snake.squares[0], fill="#FFD700")
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)

def change_direction(event):
    global direction

    key = event.keysym.lower()  # Get the lowercase key symbol

    if key == 'a':
        if direction != 'right':
            direction = 'left'
    elif key == 'd':
        if direction != 'left':
            direction = 'right'
    elif key == 'w':
        if direction != 'down':
            direction = 'up'
    elif key == 's':
        if direction != 'up':
            direction = 'down'

def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")

def start_game(event):
    global score, direction

    # Reset the score and direction
    score = 0
    direction = 'down'
    label.config(text="Score:{}".format(score))

    # Delete any existing game over message
    canvas.delete("gameover")

    # Clear the canvas
    canvas.delete(ALL)

    # Create a new snake and food
    snake = Snake()
    food = Food()

    # Start the game loop
    next_turn(snake, food)

window = Tk()
window.title("Snake game")
window.resizable(False, False)

score = 0
direction = 'down'

# Add label for "Press <Left Mouse Button> to play"
play_label = Label(window, text="Press <Left Mouse Button> to play", font=('consolas', 20))
play_label.pack()

label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

# Bind left mouse button click event to start_game function
canvas.bind("<Button-1>", start_game)

# Bind W, A, S, D keys to change_direction function
window.bind('<Key>', change_direction)

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.mainloop()
