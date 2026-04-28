# paint.py
import pygame
import sys
from datetime import datetime
from tools import draw_shape, flood_fill


def main():
    pygame.init()

    # -----------------------------
    # WINDOW SETTINGS
    # -----------------------------
    WIDTH, HEIGHT = 1000, 700
    TOOLBAR_HEIGHT = 120

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("TSIS2 Extended Paint Application")
    clock = pygame.time.Clock()

    # -----------------------------
    # COLORS
    # -----------------------------
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (220, 220, 220)
    DARK_GRAY = (80, 80, 80)
    RED = (255, 0, 0)
    GREEN = (0, 180, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    PURPLE = (160, 32, 240)
    ORANGE = (255, 140, 0)

    colors = [WHITE, BLACK, RED, GREEN, BLUE, YELLOW, PURPLE, ORANGE]

    # -----------------------------
    # FONTS
    # -----------------------------
    font = pygame.font.SysFont("Verdana", 18)
    small_font = pygame.font.SysFont("Verdana", 14)
    text_font = pygame.font.SysFont("Verdana", 28)

    # -----------------------------
    # CANVAS
    # -----------------------------
    canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
    canvas.fill(WHITE)

    # -----------------------------
    # STATE VARIABLES
    # -----------------------------
    current_color = BLACK
    brush_size = 5
    tool = "pencil"

    drawing = False
    start_pos = None
    last_pos = None
    preview_pos = None

    # Text tool state
    text_active = False
    text_position = None
    text_value = ""

    # Color buttons
    color_rects = []
    for i, color in enumerate(colors):
        rect = pygame.Rect(20 + i * 45, 15, 32, 32)
        color_rects.append((rect, color))

    # Brush size buttons
    size_buttons = [
        (pygame.Rect(370, 15, 80, 30), 2, "Small"),
        (pygame.Rect(460, 15, 90, 30), 5, "Medium"),
        (pygame.Rect(560, 15, 80, 30), 10, "Large")
    ]

    def canvas_pos(mouse_pos):
        """Convert screen coordinates to canvas coordinates."""
        return (mouse_pos[0], mouse_pos[1] - TOOLBAR_HEIGHT)

    def is_on_canvas(mouse_pos):
        """Check if mouse is below toolbar."""
        return mouse_pos[1] >= TOOLBAR_HEIGHT

    def draw_toolbar():
        """Draw toolbar with instructions, colors, and size buttons."""
        pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))

        # Color selection buttons
        for rect, color in color_rects:
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)

            if color == current_color:
                pygame.draw.rect(screen, DARK_GRAY, rect.inflate(6, 6), 3)

        # Brush size buttons
        for rect, size, label in size_buttons:
            pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)

            if brush_size == size:
                pygame.draw.rect(screen, DARK_GRAY, rect.inflate(4, 4), 3)

            text = small_font.render(label, True, BLACK)
            screen.blit(text, (rect.x + 8, rect.y + 6))

        line1 = font.render(
            "Tools: P-Pencil  L-Line  R-Rectangle  O-Circle  S-Square  T-RightTriangle",
            True,
            BLACK
        )
        line2 = font.render(
            "Q-EquilateralTriangle  H-Rhombus  F-Fill  X-Text  E-Eraser  C-Clear",
            True,
            BLACK
        )
        line3 = font.render(
            "Sizes: 1-Small  2-Medium  3-Large | Ctrl+S Save | Enter confirm text | Esc cancel text",
            True,
            BLACK
        )

        status = small_font.render(
            f"Current tool: {tool} | Brush size: {brush_size}",
            True,
            BLACK
        )

        screen.blit(line1, (20, 55))
        screen.blit(line2, (20, 78))
        screen.blit(line3, (20, 100))
        screen.blit(status, (680, 22))

    def save_canvas():
        """Save canvas as timestamped PNG file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"paint_{timestamp}.png"

        pygame.image.save(canvas, filename)
        print(f"Canvas saved as {filename}")

    def draw_text_preview():
        """Draw text cursor and typed text before confirmation."""
        if text_active and text_position:
            preview_text = text_font.render(text_value + "|", True, current_color)
            screen.blit(preview_text, (text_position[0], text_position[1] + TOOLBAR_HEIGHT))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # -----------------------------
            # KEYBOARD CONTROLS
            # -----------------------------
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()

                # Ctrl + S saves canvas
                if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                    if event.key == pygame.K_s:
                        save_canvas()
                        continue

                # If text tool is active, keyboard input becomes text
                if text_active:
                    if event.key == pygame.K_RETURN:
                        # Confirm text and render it permanently
                        final_text = text_font.render(text_value, True, current_color)
                        canvas.blit(final_text, text_position)

                        text_active = False
                        text_value = ""
                        text_position = None

                    elif event.key == pygame.K_ESCAPE:
                        # Cancel text input
                        text_active = False
                        text_value = ""
                        text_position = None

                    elif event.key == pygame.K_BACKSPACE:
                        text_value = text_value[:-1]

                    else:
                        if event.unicode:
                            text_value += event.unicode

                    continue

                # Tool shortcuts
                if event.key == pygame.K_p:
                    tool = "pencil"
                elif event.key == pygame.K_l:
                    tool = "line"
                elif event.key == pygame.K_r:
                    tool = "rectangle"
                elif event.key == pygame.K_o:
                    tool = "circle"
                elif event.key == pygame.K_s:
                    tool = "square"
                elif event.key == pygame.K_t:
                    tool = "right_triangle"
                elif event.key == pygame.K_q:
                    tool = "equilateral_triangle"
                elif event.key == pygame.K_h:
                    tool = "rhombus"
                elif event.key == pygame.K_f:
                    tool = "fill"
                elif event.key == pygame.K_x:
                    tool = "text"
                elif event.key == pygame.K_e:
                    tool = "eraser"
                elif event.key == pygame.K_c:
                    canvas.fill(WHITE)

                # Brush size shortcuts
                elif event.key == pygame.K_1:
                    brush_size = 2
                elif event.key == pygame.K_2:
                    brush_size = 5
                elif event.key == pygame.K_3:
                    brush_size = 10

            # -----------------------------
            # MOUSE BUTTON DOWN
            # -----------------------------
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos

                # Toolbar clicks
                if my < TOOLBAR_HEIGHT:
                    for rect, color in color_rects:
                        if rect.collidepoint(event.pos):
                            current_color = color
                            if tool == "eraser":
                                tool = "pencil"

                    for rect, size, label in size_buttons:
                        if rect.collidepoint(event.pos):
                            brush_size = size

                    continue

                pos = canvas_pos(event.pos)

                # Flood fill
                if tool == "fill":
                    flood_fill(canvas, pos, current_color)
                    continue

                # Text tool starts typing at clicked point
                if tool == "text":
                    text_active = True
                    text_position = pos
                    text_value = ""
                    continue

                # Start drawing
                drawing = True
                start_pos = pos
                last_pos = pos
                preview_pos = pos

                if tool == "pencil":
                    pygame.draw.circle(canvas, current_color, pos, brush_size)

                elif tool == "eraser":
                    pygame.draw.circle(canvas, WHITE, pos, brush_size)

            # -----------------------------
            # MOUSE MOTION
            # -----------------------------
            if event.type == pygame.MOUSEMOTION and drawing:
                if not is_on_canvas(event.pos):
                    continue

                pos = canvas_pos(event.pos)

                # Pencil draws continuously while mouse is held
                if tool == "pencil":
                    pygame.draw.line(canvas, current_color, last_pos, pos, brush_size)
                    last_pos = pos

                # Eraser is the same as pencil, but with white color
                elif tool == "eraser":
                    pygame.draw.line(canvas, WHITE, last_pos, pos, brush_size)
                    last_pos = pos

                # Shapes and straight line use live preview
                elif tool in (
                    "line",
                    "rectangle",
                    "circle",
                    "square",
                    "right_triangle",
                    "equilateral_triangle",
                    "rhombus"
                ):
                    preview_pos = pos

            # -----------------------------
            # MOUSE BUTTON UP
            # -----------------------------
            if event.type == pygame.MOUSEBUTTONUP and drawing:
                if is_on_canvas(event.pos):
                    end_pos = canvas_pos(event.pos)

                    # Draw final line or shape
                    if tool in (
                        "line",
                        "rectangle",
                        "circle",
                        "square",
                        "right_triangle",
                        "equilateral_triangle",
                        "rhombus"
                    ):
                        draw_shape(canvas, tool, start_pos, end_pos, current_color, brush_size)

                drawing = False
                start_pos = None
                last_pos = None
                preview_pos = None

        # -----------------------------
        # DRAW SCREEN
        # -----------------------------
        screen.fill(WHITE)
        draw_toolbar()
        screen.blit(canvas, (0, TOOLBAR_HEIGHT))

        # Live preview for line and shapes
        if drawing and tool in (
            "line",
            "rectangle",
            "circle",
            "square",
            "right_triangle",
            "equilateral_triangle",
            "rhombus"
        ) and start_pos and preview_pos:
            preview_surface = canvas.copy()
            draw_shape(preview_surface, tool, start_pos, preview_pos, current_color, brush_size)
            screen.blit(preview_surface, (0, TOOLBAR_HEIGHT))

        # Text preview
        draw_text_preview()

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
