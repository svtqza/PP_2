import pygame
import math
from datetime import datetime


class MickeyClock:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.center = (width // 2, height // 2)

        self.face = pygame.image.load("images/clock_face.png").convert_alpha()
        self.face = pygame.transform.smoothscale(self.face, (700, 700))

        self.right_hand = pygame.image.load("images/right_hand.png").convert_alpha()
        self.left_hand = pygame.image.load("images/left_hand.png").convert_alpha()

        self.right_hand = pygame.transform.smoothscale(self.right_hand, (220, 80))
        self.left_hand = pygame.transform.smoothscale(self.left_hand, (220, 80))

        self.minute_angle = 0
        self.second_angle = 0

    def update(self):
        now = datetime.now()
        minutes = now.minute
        seconds = now.second

        self.minute_angle = -(minutes * 6)
        self.second_angle = -(seconds * 6)

    def rotate_hand(self, image, angle, pivot, offset):
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_offset = offset.rotate(-angle)
        rect = rotated_image.get_rect(center=(pivot[0] + rotated_offset.x, pivot[1] + rotated_offset.y))
        return rotated_image, rect

    def draw(self):
        self.screen.fill((240, 240, 240))

        face_rect = self.face.get_rect(center=self.center)
        self.screen.blit(self.face, face_rect)

        pivot = self.center

        minute_offset = pygame.math.Vector2(70, -20)
        second_offset = pygame.math.Vector2(-70, -20)

        minute_img, minute_rect = self.rotate_hand(
            self.right_hand,
            self.minute_angle,
            pivot,
            minute_offset
        )

        second_img, second_rect = self.rotate_hand(
            self.left_hand,
            self.second_angle,
            pivot,
            second_offset
        )

        self.screen.blit(second_img, second_rect)
        self.screen.blit(minute_img, minute_rect)