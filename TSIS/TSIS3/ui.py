# ui.py
import pygame


class Button:
    """Simple Pygame button without external UI libraries."""

    def __init__(self, x, y, width, height, text, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font

    def draw(self, surface, mouse_pos):
        """Draw button and highlight it when mouse is over it."""
        if self.rect.collidepoint(mouse_pos):
            color = (180, 180, 180)
        else:
            color = (220, 220, 220)

        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2, border_radius=10)

        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, event):
        """Return True if button is clicked."""
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)


def draw_center_text(surface, text, font, color, y):
    """Draw centered text on screen."""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(surface.get_width() // 2, y))
    surface.blit(text_surface, text_rect)
