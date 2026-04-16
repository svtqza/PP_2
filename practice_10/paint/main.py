import pygame
import sys

# -----------------------------
# INITIALIZATION
# -----------------------------
pygame.init()

# -----------------------------
# SCREEN SETTINGS
# -----------------------------
WIDTH = 1000
HEIGHT = 700
TOOLBAR_HEIGHT = 100
CANVAS_Y = TOOLBAR_HEIGHT

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Paint")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 22)

# -----------------------------
# COLORS
# -----------------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 180, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (160, 32, 240)
ORANGE = (255, 140, 0)

COLOR_OPTIONS = [
    BLACK, RED, GREEN, BLUE, YELLOW, PURPLE, ORANGE, WHITE
]

# -----------------------------
# TOOL SETTINGS
# -----------------------------
current_color = BLACK
brush_size = 6
tool = "brush"   # brush, rect, circle, eraser

# Variables for drawing shapes
drawing = False
start_pos = None
last_pos = None

# -----------------------------
# CANVAS
# Separate surface for drawing
# so toolbar stays unchanged
# -----------------------------
canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
canvas.fill(WHITE)

# -----------------------------
# UI RECTANGLES
# -----------------------------
color_boxes = []
for i, color in enumerate(COLOR_OPTIONS):
    rect = pygame.Rect(20 + i * 55, 20, 40, 40)
    color_boxes.append((rect, color))

tool_buttons = {
    "brush": pygame.Rect(520, 15, 100, 35),
    "rect": pygame.Rect(630, 15, 120, 35),
    "circle": pygame.Rect(760, 15, 100, 35),
    "eraser": pygame.Rect(870, 15, 100, 35),
}

# -----------------------------
# FUNCTION: DRAW TOOLBAR
# -----------------------------
def draw_toolbar():
    """Draw top toolbar with colors, tool buttons, and info text."""
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))
    pygame.draw.line(screen, DARK_GRAY, (0, TOOLBAR_HEIGHT), (WIDTH, TOOLBAR_HEIGHT), 3)

    # Draw color palette
    for rect, color in color_boxes:
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)

        # Highlight selected color
        if color == current_color:
            pygame.draw.rect(screen, DARK_GRAY, rect.inflate(6, 6), 3)

    # Draw tool buttons
    for name, rect in tool_buttons.items():
        if tool == name:
            pygame.draw.rect(screen, DARK_GRAY, rect)
        else:
            pygame.draw.rect(screen, WHITE, rect)

        pygame.draw.rect(screen, BLACK, rect, 2)
        label = font.render(name.capitalize(), True, BLACK)
        screen.blit(
            label,
            (
                rect.centerx - label.get_width() // 2,
                rect.centery - label.get_height() // 2
            )
        )

    # Draw current info
    info1 = font.render(f"Color: {current_color}", True, BLACK)
    info2 = font.render(f"Size: {brush_size}", True, BLACK)
    info3 = font.render("Keys: B=Brush R=Rect C=Circle E=Eraser [ ]=Size SPACE=Clear", True, BLACK)

    screen.blit(info1, (20, 70))
    screen.blit(info2, (250, 70))
    screen.blit(info3, (380, 70))

# -----------------------------
# FUNCTION: DRAW LINE SMOOTHLY
# -----------------------------
def draw_brush(surface, color, start, end, radius):
    """Draw a smooth thick line by connecting circles."""
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    distance = max(abs(dx), abs(dy))

    if distance == 0:
        pygame.draw.circle(surface, color, start, radius)
        return

    for i in range(distance + 1):
        x = int(start[0] + dx * i / distance)
        y = int(start[1] + dy * i / distance)
        pygame.draw.circle(surface, color, (x, y), radius)

# -----------------------------
# MAIN LOOP
# -----------------------------
while True:
    # We use preview copy for rectangle/circle while dragging
    preview_canvas = canvas.copy()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # -------------------------
        # KEYBOARD CONTROLS
        # -------------------------
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_b:
                tool = "brush"
            elif event.key == pygame.K_r:
                tool = "rect"
            elif event.key == pygame.K_c:
                tool = "circle"
            elif event.key == pygame.K_e:
                tool = "eraser"
            elif event.key == pygame.K_LEFTBRACKET:
                brush_size = max(1, brush_size - 1)
            elif event.key == pygame.K_RIGHTBRACKET:
                brush_size = min(50, brush_size + 1)
            elif event.key == pygame.K_SPACE:
                canvas.fill(WHITE)

        # -------------------------
        # MOUSE BUTTON DOWN
        # -------------------------
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            # Check if user clicked on color palette
            for rect, color in color_boxes:
                if rect.collidepoint(mx, my):
                    current_color = color

            # Check if user clicked on tool buttons
            for name, rect in tool_buttons.items():
                if rect.collidepoint(mx, my):
                    tool = name

            # Start drawing only if click is inside canvas area
            if my >= CANVAS_Y:
                drawing = True
                start_pos = (mx, my - CANVAS_Y)
                last_pos = (mx, my - CANVAS_Y)

                # If brush or eraser, draw immediately on first click
                if tool == "brush":
                    pygame.draw.circle(canvas, current_color, start_pos, brush_size)
                elif tool == "eraser":
                    pygame.draw.circle(canvas, WHITE, start_pos, brush_size)

        # -------------------------
        # MOUSE MOTION
        # -------------------------
        if event.type == pygame.MOUSEMOTION and drawing:
            mx, my = event.pos

            # Only draw inside canvas
            if my >= CANVAS_Y:
                current_pos = (mx, my - CANVAS_Y)

                # Brush draws continuously
                if tool == "brush":
                    draw_brush(canvas, current_color, last_pos, current_pos, brush_size)

                # Eraser draws continuously with white color
                elif tool == "eraser":
                    draw_brush(canvas, WHITE, last_pos, current_pos, brush_size)

                last_pos = current_pos

        # -------------------------
        # MOUSE BUTTON UP
        # Finalize rectangle/circle
        # -------------------------
        if event.type == pygame.MOUSEBUTTONUP and drawing:
            mx, my = event.pos

            if my >= CANVAS_Y:
                end_pos = (mx, my - CANVAS_Y)

                # Draw rectangle when mouse released
                if tool == "rect":
                    x1, y1 = start_pos
                    x2, y2 = end_pos
                    rect = pygame.Rect(
                        min(x1, x2),
                        min(y1, y2),
                        abs(x2 - x1),
                        abs(y2 - y1)
                    )
                    pygame.draw.rect(canvas, current_color, rect, 2)

                # Draw circle when mouse released
                elif tool == "circle":
                    x1, y1 = start_pos
                    x2, y2 = end_pos

                    # Radius = distance between start and end
                    radius = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
                    pygame.draw.circle(canvas, current_color, start_pos, radius, 2)

            drawing = False
            start_pos = None
            last_pos = None

    # -----------------------------
    # DRAW PREVIEW FOR SHAPES
    # -----------------------------
    if drawing and tool in ["rect", "circle"]:
        mx, my = pygame.mouse.get_pos()
        if my >= CANVAS_Y:
            end_pos = (mx, my - CANVAS_Y)

            if tool == "rect":
                x1, y1 = start_pos
                x2, y2 = end_pos
                rect = pygame.Rect(
                    min(x1, x2),
                    min(y1, y2),
                    abs(x2 - x1),
                    abs(y2 - y1)
                )
                pygame.draw.rect(preview_canvas, current_color, rect, 2)

            elif tool == "circle":
                x1, y1 = start_pos
                x2, y2 = end_pos
                radius = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
                pygame.draw.circle(preview_canvas, current_color, start_pos, radius, 2)

    # -----------------------------
    # RENDER
    # -----------------------------
    screen.fill(WHITE)
    draw_toolbar()

    # Show preview while dragging shapes
    if drawing and tool in ["rect", "circle"]:
        screen.blit(preview_canvas, (0, TOOLBAR_HEIGHT))
    else:
        screen.blit(canvas, (0, TOOLBAR_HEIGHT))

    pygame.display.flip()
    clock.tick(60)