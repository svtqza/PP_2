import pygame
import random
import sys

# -----------------------------
# INITIALIZATION
# -----------------------------
pygame.init()

# -----------------------------
# GAME SETTINGS
# -----------------------------
CELL_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 20

SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 180, 0)
DARK_GREEN = (0, 120, 0)
RED = (220, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
BLUE = (50, 120, 255)

# Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# Clock
clock = pygame.time.Clock()

# Font
font = pygame.font.SysFont("Verdana", 20)
big_font = pygame.font.SysFont("Verdana", 42)

# -----------------------------
# GAME VARIABLES
# -----------------------------
# Snake starts in the middle of the screen
snake = [(10, 10), (9, 10), (8, 10)]

# Initial movement direction
direction = (1, 0)

# Score and level
score = 0
level = 1

# Initial speed
speed = 7

# Number of foods eaten on current level
foods_eaten = 0

# Example: next level every 4 foods
FOODS_PER_LEVEL = 4

# Thickness of walls (in cells)
WALL_THICKNESS = 1


# -----------------------------
# FUNCTION: DRAW TEXT
# -----------------------------
def draw_text():
    """Draw score and level on the screen."""
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)

    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (SCREEN_WIDTH - level_text.get_width() - 10, 10))


# -----------------------------
# FUNCTION: DRAW WALLS
# Walls are along the screen border
# -----------------------------
def draw_walls():
    """Draw gray border walls around the playing area."""
    # Top wall
    pygame.draw.rect(screen, GRAY, (0, 0, SCREEN_WIDTH, CELL_SIZE * WALL_THICKNESS))

    # Bottom wall
    pygame.draw.rect(
        screen,
        GRAY,
        (0, SCREEN_HEIGHT - CELL_SIZE * WALL_THICKNESS, SCREEN_WIDTH, CELL_SIZE * WALL_THICKNESS)
    )

    # Left wall
    pygame.draw.rect(screen, GRAY, (0, 0, CELL_SIZE * WALL_THICKNESS, SCREEN_HEIGHT))

    # Right wall
    pygame.draw.rect(
        screen,
        GRAY,
        (SCREEN_WIDTH - CELL_SIZE * WALL_THICKNESS, 0, CELL_SIZE * WALL_THICKNESS, SCREEN_HEIGHT)
    )


# -----------------------------
# FUNCTION: CHECK IF CELL IS WALL
# -----------------------------
def is_wall(position):
    """Return True if the given cell is part of the wall."""
    x, y = position

    if x < WALL_THICKNESS or x >= GRID_WIDTH - WALL_THICKNESS:
        return True
    if y < WALL_THICKNESS or y >= GRID_HEIGHT - WALL_THICKNESS:
        return True

    return False


# -----------------------------
# FUNCTION: GENERATE FOOD
# Food must not appear on wall or snake
# -----------------------------
def generate_food():
    """Generate random food position not on wall and not on snake."""
    while True:
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        food_position = (x, y)

        if not is_wall(food_position) and food_position not in snake:
            return food_position


# Create first food
food = generate_food()


# -----------------------------
# FUNCTION: DRAW SNAKE
# -----------------------------
def draw_snake():
    """Draw the snake on the screen."""
    for i, segment in enumerate(snake):
        x, y = segment
        rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

        # Head has a different color
        if i == 0:
            pygame.draw.rect(screen, DARK_GREEN, rect)
        else:
            pygame.draw.rect(screen, GREEN, rect)

        # Optional border for nicer look
        pygame.draw.rect(screen, BLACK, rect, 1)


# -----------------------------
# FUNCTION: DRAW FOOD
# -----------------------------
def draw_food():
    """Draw the food on the screen."""
    x, y = food
    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, RED, rect)
    pygame.draw.rect(screen, BLACK, rect, 1)


# -----------------------------
# FUNCTION: GAME OVER SCREEN
# -----------------------------
def game_over():
    """Show game over text and quit."""
    screen.fill(BLACK)

    over_text = big_font.render("Game Over", True, RED)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    level_text = font.render(f"Level Reached: {level}", True, WHITE)

    screen.blit(
        over_text,
        (SCREEN_WIDTH // 2 - over_text.get_width() // 2,
         SCREEN_HEIGHT // 2 - 70)
    )
    screen.blit(
        score_text,
        (SCREEN_WIDTH // 2 - score_text.get_width() // 2,
         SCREEN_HEIGHT // 2)
    )
    screen.blit(
        level_text,
        (SCREEN_WIDTH // 2 - level_text.get_width() // 2,
         SCREEN_HEIGHT // 2 + 35)
    )

    pygame.display.update()
    pygame.time.wait(2500)
    pygame.quit()
    sys.exit()


# -----------------------------
# MAIN GAME LOOP
# -----------------------------
while True:
    # -------------------------
    # HANDLE EVENTS
    # -------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Change snake direction with arrow keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, 1):
                direction = (0, -1)
            elif event.key == pygame.K_DOWN and direction != (0, -1):
                direction = (0, 1)
            elif event.key == pygame.K_LEFT and direction != (1, 0):
                direction = (-1, 0)
            elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                direction = (1, 0)

    # -------------------------
    # MOVE SNAKE
    # -------------------------
    head_x, head_y = snake[0]
    dx, dy = direction
    new_head = (head_x + dx, head_y + dy)

    # -------------------------
    # CHECK BORDER / WALL COLLISION
    # Snake dies if it leaves the area
    # or hits the wall
    # -------------------------
    if (
        new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
        new_head[1] < 0 or new_head[1] >= GRID_HEIGHT or
        is_wall(new_head)
    ):
        game_over()

    # -------------------------
    # CHECK SELF COLLISION
    # -------------------------
    if new_head in snake:
        game_over()

    # Add new head
    snake.insert(0, new_head)

    # -------------------------
    # CHECK IF FOOD IS EATEN
    # -------------------------
    if new_head == food:
        score += 1
        foods_eaten += 1

        # Generate new food in a safe place
        food = generate_food()

        # LEVEL SYSTEM:
        # every 4 foods -> next level
        if foods_eaten == FOODS_PER_LEVEL:
            level += 1
            foods_eaten = 0
            speed += 2  # increase game speed
    else:
        # Remove tail if food was not eaten
        snake.pop()

    # -------------------------
    # DRAW EVERYTHING
    # -------------------------
    screen.fill(BLACK)
    draw_walls()
    draw_snake()
    draw_food()
    draw_text()

    pygame.display.update()
    clock.tick(speed)