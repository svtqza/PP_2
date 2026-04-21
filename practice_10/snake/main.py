import pygame
import random
import sys

pygame.init()

# Screen settings
WIDTH = 600
HEIGHT = 600
CELL = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
GRAY = (100, 100, 100)
BLUE = (0, 0, 200)

# Fonts
font = pygame.font.SysFont("Verdana", 20)
game_over_font = pygame.font.SysFont("Verdana", 50)

# Game area borders
WALL_THICKNESS = CELL

# Snake settings
snake = [(100, 100), (80, 100), (60, 100)]
dx = CELL
dy = 0

# Food settings
food = None

# Score and level
score = 0
level = 1
foods_eaten = 0
base_speed = 7

def draw_walls():
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, WALL_THICKNESS))  # top
    pygame.draw.rect(screen, GRAY, (0, HEIGHT - WALL_THICKNESS, WIDTH, WALL_THICKNESS))  # bottom
    pygame.draw.rect(screen, GRAY, (0, 0, WALL_THICKNESS, HEIGHT))  # left
    pygame.draw.rect(screen, GRAY, (WIDTH - WALL_THICKNESS, 0, WALL_THICKNESS, HEIGHT))  # right

def draw_snake():
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0], segment[1], CELL, CELL))

def draw_food():
    pygame.draw.rect(screen, RED, (food[0], food[1], CELL, CELL))

def draw_info():
    score_text = font.render(f"Score: {score}", True, BLACK)
    level_text = font.render(f"Level: {level}", True, BLACK)
    speed_text = font.render(f"Speed: {base_speed + level - 1}", True, BLACK)

    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 35))
    screen.blit(speed_text, (10, 60))

def generate_food():
    while True:
        x = random.randrange(CELL, WIDTH - CELL, CELL)
        y = random.randrange(CELL, HEIGHT - CELL, CELL)

        # Food must not appear on snake
        if (x, y) not in snake:
            return (x, y)

def check_wall_collision(position):
    x, y = position
    if x < CELL or x >= WIDTH - CELL:
        return True
    if y < CELL or y >= HEIGHT - CELL:
        return True
    return False

def check_self_collision():
    head = snake[0]
    return head in snake[1:]

def update_level():
    global level
    # New level every 4 foods
    level = foods_eaten // 4 + 1

def show_game_over():
    screen.fill(WHITE)
    text = game_over_font.render("Game Over", True, RED)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))

    final_score = font.render(f"Final Score: {score}", True, BLACK)
    score_rect = final_score.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))

    screen.blit(text, text_rect)
    screen.blit(final_score, score_rect)
    pygame.display.flip()
    pygame.time.delay(3000)

food = generate_food()

running = True
while running:
    clock.tick(base_speed + level - 1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and dy == 0:
                dx = 0
                dy = -CELL
            elif event.key == pygame.K_DOWN and dy == 0:
                dx = 0
                dy = CELL
            elif event.key == pygame.K_LEFT and dx == 0:
                dx = -CELL
                dy = 0
            elif event.key == pygame.K_RIGHT and dx == 0:
                dx = CELL
                dy = 0

    # Move snake
    head_x, head_y = snake[0]
    new_head = (head_x + dx, head_y + dy)

    # Check border collision
    if check_wall_collision(new_head):
        show_game_over()
        break

    snake.insert(0, new_head)

    # Check if food is eaten
    if new_head == food:
        score += 1
        foods_eaten += 1
        update_level()
        food = generate_food()
    else:
        snake.pop()

    # Check self collision
    if check_self_collision():
        show_game_over()
        break

    # Draw everything
    screen.fill(WHITE)
    draw_walls()
    draw_snake()
    draw_food()
    draw_info()
    pygame.display.flip()

pygame.quit()
sys.exit()