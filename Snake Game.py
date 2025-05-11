import pygame
import time
import random

# Initialize pygame
pygame.init()

# Define colors
white = (255, 255, 255)       # Snake color (white)
golden = (255, 215, 0)        # Golden color (instead of yellow)
black = (0, 0, 0)
red = (213, 50, 80)           # Food color (red, will be replaced by apple image)
green = (0, 255, 0)           # Obstacle color (green)
blue = (50, 153, 213)
deep_dark_blue = (0, 0, 50)   # Background color (deep dark blue)

# Set display width and height
width = 600
height = 400

# Create display window
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')

# Set clock to control game speed
clock = pygame.time.Clock()

# Set snake block size and speed
block_size = 10
snake_speed = 15

# Define font and size for the score and messages
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Load the apple image
apple_image = pygame.image.load('apple.jpg')  # Make sure 'apple.png' is in the same directory
apple_image = pygame.transform.scale(apple_image, (block_size, block_size))  # Resize it to fit the block size

# Function to display the current score
def your_score(score):
    value = score_font.render("Your Score: " + str(score), True, golden)
    screen.blit(value, [0, 0])

# Function to draw the snake (as white block)
def our_snake(block_size, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, white, [x[0], x[1], block_size, block_size])  # Snake color is white

# Function to display messages
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [width / 6, height / 3])

# Function to draw obstacles (now green)
def draw_obstacles(obstacles):
    for obs in obstacles:
        pygame.draw.rect(screen, green, [obs[0], obs[1], block_size, block_size])  # Draw obstacles in green

# Check for collision with obstacles
def check_obstacle_collision(snake_head, obstacles):
    for obs in obstacles:
        if snake_head[0] == obs[0] and snake_head[1] == obs[1]:
            return True
    return False

# Game loop
def gameLoop():
    game_over = False
    game_close = False

    # Starting position of the snake
    x1 = width / 2
    y1 = height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    # Random position for the food
    foodx = round(random.randrange(0, width - block_size) / 10.0) * 10.0
    foody = round(random.randrange(0, height - block_size) / 10.0) * 10.0

    # Define obstacles (list of positions)
    obstacles = []
    for _ in range(5):  # Add 5 random obstacles
        obs_x = round(random.randrange(0, width - block_size) / 10.0) * 10.0
        obs_y = round(random.randrange(0, height - block_size) / 10.0) * 10.0
        while (obs_x == x1 and obs_y == y1):  # Avoid the snake's starting position
            obs_x = round(random.randrange(0, width - block_size) / 10.0) * 10.0
            obs_y = round(random.randrange(0, height - block_size) / 10.0) * 10.0
        obstacles.append([obs_x, obs_y])

    # Main game loop
    while not game_over:

        while game_close:
            screen.fill(deep_dark_blue)  # Set background color to deep dark blue
            message("You Lost! Press Q-Quit or C-Play Again", red)
            your_score(Length_of_snake - 1)
            pygame.display.update()

            # Handle game over actions
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        # Check for events like key presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -block_size
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = block_size
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -block_size
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = block_size
                    x1_change = 0

        # Check for boundaries (snake colliding with walls)
        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True

        # Move the snake
        x1 += x1_change
        y1 += y1_change
        screen.fill(deep_dark_blue)  # Set background color to deep dark blue

        # Draw food (use the apple image here instead of a rectangle)
        screen.blit(apple_image, (foodx, foody))  # Draw the apple image as food

        # Draw obstacles (now green)
        draw_obstacles(obstacles)

        # Update snake body
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Check if snake hits itself
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        # Check for collision with obstacles
        if check_obstacle_collision(snake_Head, obstacles):
            game_close = True

        # Draw the snake
        our_snake(block_size, snake_List)
        your_score(Length_of_snake - 1)

        pygame.display.update()

        # Check if snake eats food
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - block_size) / 10.0) * 10.0
            foody = round(random.randrange(0, height - block_size) / 10.0) * 10.0
            Length_of_snake += 1

        # Set game speed
        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Run the game
gameLoop()
