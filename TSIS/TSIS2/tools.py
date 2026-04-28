# tools.py
import pygame
import math
from collections import deque


def normalize_rect(start, end):
    """Create a pygame Rect from any drag direction."""
    x1, y1 = start
    x2, y2 = end

    left = min(x1, x2)
    top = min(y1, y2)
    width = abs(x2 - x1)
    height = abs(y2 - y1)

    return pygame.Rect(left, top, width, height)


def normalize_square(start, end):
    """Create a square from any drag direction."""
    x1, y1 = start
    x2, y2 = end

    size = min(abs(x2 - x1), abs(y2 - y1))

    left = x1 if x2 >= x1 else x1 - size
    top = y1 if y2 >= y1 else y1 - size

    return pygame.Rect(left, top, size, size)


def right_triangle_points(start, end):
    """Return points for a right triangle."""
    return [
        start,
        (start[0], end[1]),
        end
    ]


def equilateral_triangle_points(start, end):
    """Return points for an equilateral triangle."""
    x1, y1 = start
    x2, y2 = end

    side = x2 - x1

    if side == 0:
        side = 1

    height = abs(side) * math.sqrt(3) / 2

    p1 = (x1, y1)
    p2 = (x2, y1)

    if y2 < y1:
        p3 = ((x1 + x2) // 2, y1 - height)
    else:
        p3 = ((x1 + x2) // 2, y1 + height)

    return [p1, p2, p3]


def rhombus_points(start, end):
    """Return points for a rhombus."""
    rect = normalize_rect(start, end)

    center_x = rect.centerx
    center_y = rect.centery

    return [
        (center_x, rect.top),
        (rect.right, center_y),
        (center_x, rect.bottom),
        (rect.left, center_y)
    ]


def draw_shape(surface, tool, start, end, color, brush_size):
    """Draw selected shape with active brush size."""
    if tool == "line":
        pygame.draw.line(surface, color, start, end, brush_size)

    elif tool == "rectangle":
        pygame.draw.rect(surface, color, normalize_rect(start, end), brush_size)

    elif tool == "circle":
        center_x = (start[0] + end[0]) // 2
        center_y = (start[1] + end[1]) // 2

        radius = max(
            abs(end[0] - start[0]) // 2,
            abs(end[1] - start[1]) // 2
        )

        pygame.draw.circle(surface, color, (center_x, center_y), radius, brush_size)

    elif tool == "square":
        pygame.draw.rect(surface, color, normalize_square(start, end), brush_size)

    elif tool == "right_triangle":
        pygame.draw.polygon(surface, color, right_triangle_points(start, end), brush_size)

    elif tool == "equilateral_triangle":
        pygame.draw.polygon(surface, color, equilateral_triangle_points(start, end), brush_size)

    elif tool == "rhombus":
        pygame.draw.polygon(surface, color, rhombus_points(start, end), brush_size)


def flood_fill(surface, start_pos, fill_color):
    """
    Flood fill using get_at and set_at.
    It fills only pixels with the exact same color as the clicked pixel.
    """
    width, height = surface.get_size()

    x, y = start_pos

    if x < 0 or x >= width or y < 0 or y >= height:
        return

    target_color = surface.get_at((x, y))

    # If clicked area already has selected color, do nothing
    if target_color == fill_color:
        return

    queue = deque()
    queue.append((x, y))

    while queue:
        px, py = queue.popleft()

        if px < 0 or px >= width or py < 0 or py >= height:
            continue

        if surface.get_at((px, py)) != target_color:
            continue

        surface.set_at((px, py), fill_color)

        queue.append((px + 1, py))
        queue.append((px - 1, py))
        queue.append((px, py + 1))
        queue.append((px, py - 1))
