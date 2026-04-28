# racer.py
import pygame
import random
import time
from persistence import save_score

WIDTH = 500
HEIGHT = 700
ROAD_LEFT = 70
ROAD_RIGHT = 430
ROAD_WIDTH = ROAD_RIGHT - ROAD_LEFT
LANES = [115, 205, 295, 385]
PLAYER_Y = HEIGHT - 100
FINISH_DISTANCE = 3000

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (90, 90, 90)
DARK_GRAY = (50, 50, 50)
GREEN = (0, 170, 70)
RED = (220, 20, 60)
YELLOW = (255, 215, 0)
ORANGE = (255, 140, 0)
BLUE = (50, 130, 255)
PURPLE = (160, 32, 240)
CYAN = (0, 220, 220)

CAR_COLORS = {
    "blue": BLUE,
    "red": RED,
    "green": GREEN,
    "yellow": YELLOW,
    "purple": PURPLE
}


class Player:
    """Player car controlled by keyboard."""

    def __init__(self, color_name):
        self.width = 42
        self.height = 70
        self.color = CAR_COLORS.get(color_name, BLUE)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (LANES[1], PLAYER_Y)
        self.shield = False
        self.crashes = 0

    def move(self):
        """Move player inside the road."""
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rect.x -= 6
        if keys[pygame.K_RIGHT]:
            self.rect.x += 6

        if self.rect.left < ROAD_LEFT + 5:
            self.rect.left = ROAD_LEFT + 5
        if self.rect.right > ROAD_RIGHT - 5:
            self.rect.right = ROAD_RIGHT - 5

    def draw(self, surface):
        """Draw player car."""
        pygame.draw.rect(surface, self.color, self.rect, border_radius=8)
        pygame.draw.rect(surface, BLACK, (self.rect.x + 9, self.rect.y + 12, 24, 18), border_radius=4)

        # Wheels
        pygame.draw.circle(surface, BLACK, (self.rect.left + 5, self.rect.top + 18), 5)
        pygame.draw.circle(surface, BLACK, (self.rect.right - 5, self.rect.top + 18), 5)
        pygame.draw.circle(surface, BLACK, (self.rect.left + 5, self.rect.bottom - 18), 5)
        pygame.draw.circle(surface, BLACK, (self.rect.right - 5, self.rect.bottom - 18), 5)

        # Shield circle
        if self.shield:
            pygame.draw.ellipse(surface, CYAN, self.rect.inflate(18, 18), 3)


class FallingObject:
    """Base class for traffic, obstacles, coins, and power-ups."""

    def __init__(self, kind, lane, y, speed, color, value=0):
        self.kind = kind
        self.lane = lane
        self.speed = speed
        self.value = value
        self.color = color

        if kind == "traffic":
            self.rect = pygame.Rect(0, y, 45, 75)
        elif kind in ("barrier", "oil", "pothole", "bump"):
            self.rect = pygame.Rect(0, y, 55, 35)
        elif kind == "nitro_strip":
            self.rect = pygame.Rect(0, y, 70, 25)
        else:
            self.rect = pygame.Rect(0, y, 30, 30)

        self.rect.centerx = lane
        self.spawn_time = time.time()
        self.timeout = 6

    def update(self, boost=0):
        """Move object downward."""
        self.rect.y += self.speed + boost

    def is_off_screen(self):
        return self.rect.top > HEIGHT

    def is_expired(self):
        """Power-ups disappear if not collected."""
        if self.kind in ("nitro", "shield", "repair"):
            return time.time() - self.spawn_time > self.timeout
        return False

    def draw(self, surface, font):
        """Draw object depending on its kind."""
        if self.kind == "traffic":
            pygame.draw.rect(surface, self.color, self.rect, border_radius=8)
            pygame.draw.rect(surface, BLACK, (self.rect.x + 10, self.rect.y + 12, 25, 15), border_radius=4)

        elif self.kind == "barrier":
            pygame.draw.rect(surface, ORANGE, self.rect)
            pygame.draw.line(surface, BLACK, self.rect.topleft, self.rect.bottomright, 3)
            pygame.draw.line(surface, BLACK, self.rect.topright, self.rect.bottomleft, 3)

        elif self.kind == "oil":
            pygame.draw.ellipse(surface, BLACK, self.rect)

        elif self.kind == "pothole":
            pygame.draw.ellipse(surface, DARK_GRAY, self.rect)
            pygame.draw.ellipse(surface, BLACK, self.rect, 2)

        elif self.kind == "bump":
            pygame.draw.rect(surface, YELLOW, self.rect, border_radius=8)
            pygame.draw.line(surface, BLACK, self.rect.midleft, self.rect.midright, 2)

        elif self.kind == "nitro_strip":
            pygame.draw.rect(surface, CYAN, self.rect, border_radius=6)
            text = font.render("BOOST", True, BLACK)
            surface.blit(text, (self.rect.x + 4, self.rect.y + 4))

        elif self.kind == "coin":
            pygame.draw.circle(surface, self.color, self.rect.center, self.rect.width // 2)
            text = font.render(str(self.value), True, BLACK)
            text_rect = text.get_rect(center=self.rect.center)
            surface.blit(text, text_rect)

        elif self.kind in ("nitro", "shield", "repair"):
            pygame.draw.circle(surface, self.color, self.rect.center, self.rect.width // 2)
            label = {"nitro": "N", "shield": "S", "repair": "R"}[self.kind]
            text = font.render(label, True, BLACK)
            text_rect = text.get_rect(center=self.rect.center)
            surface.blit(text, text_rect)


class RacerGame:
    """Main game class."""

    def __init__(self, screen, username, settings):
        self.screen = screen
        self.username = username
        self.settings = settings

        self.font = pygame.font.SysFont("Verdana", 18)
        self.big_font = pygame.font.SysFont("Verdana", 44)

        self.player = Player(settings["car_color"])

        self.objects = []
        self.road_offset = 0

        self.coins = 0
        self.coin_score = 0
        self.distance = 0
        self.score = 0

        self.game_over = False
        self.finished = False

        self.active_power = None
        self.power_end_time = 0
        self.power_boost = 0

        self.last_spawn_time = 0
        self.last_power_spawn_time = 0
        self.last_event_spawn_time = 0

        self.difficulty = settings["difficulty"]

        if self.difficulty == "easy":
            self.base_speed = 4
            self.spawn_delay = 1.2
        elif self.difficulty == "hard":
            self.base_speed = 7
            self.spawn_delay = 0.6
        else:
            self.base_speed = 5
            self.spawn_delay = 0.9

    def safe_lane(self):
        """Choose a lane that is not directly on top of the player."""
        possible = [lane for lane in LANES if abs(lane - self.player.rect.centerx) > 60]

        if not possible:
            possible = LANES

        return random.choice(possible)

    def current_difficulty_bonus(self):
        """Increase difficulty as distance grows."""
        return int(self.distance // 500)

    def spawn_traffic_or_obstacle(self):
        """Spawn traffic and obstacles with safe spawn logic."""
        now = time.time()
        delay = max(0.3, self.spawn_delay - self.current_difficulty_bonus() * 0.08)

        if now - self.last_spawn_time < delay:
            return

        self.last_spawn_time = now

        lane = self.safe_lane()
        speed = self.base_speed + self.current_difficulty_bonus()

        roll = random.random()

        if roll < 0.45:
            obj = FallingObject("traffic", lane, -90, speed, RED)
        elif roll < 0.65:
            obj = FallingObject("barrier", lane, -50, speed, ORANGE)
        elif roll < 0.8:
            obj = FallingObject("oil", lane, -50, speed, BLACK)
        elif roll < 0.92:
            obj = FallingObject("pothole", lane, -50, speed, DARK_GRAY)
        else:
            obj = FallingObject("bump", lane, -50, speed, YELLOW)

        self.objects.append(obj)

        # Weighted coins from Practice 11
        if random.random() < 0.7:
            coin_lane = random.choice(LANES)
            coin_type = random.choice([
                (1, YELLOW),
                (2, ORANGE),
                (3, PURPLE)
            ])
            self.objects.append(FallingObject("coin", coin_lane, -130, speed, coin_type[1], coin_type[0]))

    def spawn_powerup(self):
        """Spawn one collectible power-up with timeout."""
        now = time.time()

        if now - self.last_power_spawn_time < 7:
            return

        self.last_power_spawn_time = now

        if random.random() < 0.7:
            lane = self.safe_lane()
            speed = self.base_speed + self.current_difficulty_bonus()

            power_type = random.choice([
                ("nitro", CYAN),
                ("shield", BLUE),
                ("repair", GREEN)
            ])

            self.objects.append(FallingObject(power_type[0], lane, -60, speed, power_type[1]))

    def spawn_road_event(self):
        """Spawn dynamic road events like boost strips."""
        now = time.time()

        if now - self.last_event_spawn_time < 5:
            return

        self.last_event_spawn_time = now

        if random.random() < 0.5:
            lane = self.safe_lane()
            speed = self.base_speed + self.current_difficulty_bonus()
            self.objects.append(FallingObject("nitro_strip", lane, -70, speed, CYAN))

    def update_powerup(self):
        """Update active power-up timer."""
        if self.active_power == "nitro":
            remaining = self.power_end_time - time.time()

            if remaining <= 0:
                self.active_power = None
                self.power_boost = 0

    def activate_powerup(self, kind):
        """Activate collected power-up. Only one timed power-up can be active."""
        if kind == "nitro":
            self.active_power = "nitro"
            self.power_end_time = time.time() + 4
            self.power_boost = 3

        elif kind == "shield":
            self.active_power = "shield"
            self.player.shield = True

        elif kind == "repair":
            self.active_power = "repair"
            self.player.crashes = max(0, self.player.crashes - 1)

            # Repair also removes one obstacle from the road
            for obj in self.objects:
                if obj.kind in ("barrier", "oil", "pothole", "bump"):
                    self.objects.remove(obj)
                    break

            self.active_power = None

    def handle_collision(self, obj):
        """Handle player collision with any object."""
        if obj.kind == "coin":
            self.coins += obj.value
            self.coin_score += obj.value * 10
            self.objects.remove(obj)

        elif obj.kind in ("nitro", "shield", "repair"):
            # Only one power-up active at a time
            if self.active_power is None or obj.kind == "repair":
                self.activate_powerup(obj.kind)
            self.objects.remove(obj)

        elif obj.kind == "nitro_strip":
            self.active_power = "nitro"
            self.power_end_time = time.time() + 3
            self.power_boost = 3
            self.objects.remove(obj)

        elif obj.kind in ("traffic", "barrier", "pothole"):
            if self.player.shield:
                self.player.shield = False
                self.active_power = None
                self.objects.remove(obj)
            else:
                self.end_game()

        elif obj.kind == "oil":
            # Oil spill slows and moves the car slightly
            self.player.rect.x += random.choice([-35, 35])
            if self.player.rect.left < ROAD_LEFT:
                self.player.rect.left = ROAD_LEFT
            if self.player.rect.right > ROAD_RIGHT:
                self.player.rect.right = ROAD_RIGHT
            self.objects.remove(obj)

        elif obj.kind == "bump":
            # Speed bump briefly reduces distance gain
            self.distance = max(0, self.distance - 30)
            self.objects.remove(obj)

    def update(self):
        """Update game logic."""
        self.player.move()

        self.spawn_traffic_or_obstacle()
        self.spawn_powerup()
        self.spawn_road_event()
        self.update_powerup()

        speed_bonus = self.power_boost

        self.distance += self.base_speed + speed_bonus
        self.score = self.coin_score + int(self.distance / 5)

        if self.distance >= FINISH_DISTANCE:
            self.finished = True
            self.end_game()

        for obj in self.objects[:]:
            obj.update(speed_bonus)

            if obj.is_off_screen() or obj.is_expired():
                self.objects.remove(obj)
                continue

            if self.player.rect.colliderect(obj.rect):
                self.handle_collision(obj)

        self.road_offset += self.base_speed + speed_bonus

        if self.road_offset >= 40:
            self.road_offset = 0

    def draw_road(self):
        """Draw scrolling road."""
        self.screen.fill(GREEN)
        pygame.draw.rect(self.screen, GRAY, (ROAD_LEFT, 0, ROAD_WIDTH, HEIGHT))

        pygame.draw.line(self.screen, WHITE, (ROAD_LEFT, 0), (ROAD_LEFT, HEIGHT), 4)
        pygame.draw.line(self.screen, WHITE, (ROAD_RIGHT, 0), (ROAD_RIGHT, HEIGHT), 4)

        for x in [160, 250, 340]:
            for y in range(-40, HEIGHT, 40):
                pygame.draw.rect(self.screen, WHITE, (x, y + self.road_offset, 8, 25))

    def draw_hud(self):
        """Draw score, distance, coins, and active power-up."""
        remaining = max(0, FINISH_DISTANCE - int(self.distance))

        texts = [
            f"Player: {self.username}",
            f"Score: {int(self.score)}",
            f"Coins: {self.coins}",
            f"Distance: {int(self.distance)} m",
            f"Remaining: {remaining} m",
            f"Difficulty: {self.difficulty}"
        ]

        y = 10
        for text in texts:
            surface = self.font.render(text, True, WHITE)
            self.screen.blit(surface, (10, y))
            y += 24

        if self.active_power == "nitro":
            time_left = max(0, int(self.power_end_time - time.time()))
            power_text = f"Power-up: Nitro {time_left}s"
        elif self.player.shield:
            power_text = "Power-up: Shield active"
        else:
            power_text = "Power-up: None"

        surface = self.font.render(power_text, True, YELLOW)
        self.screen.blit(surface, (260, 10))

    def draw(self):
        """Draw whole game."""
        self.draw_road()

        for obj in self.objects:
            obj.draw(self.screen, self.font)

        self.player.draw(self.screen)
        self.draw_hud()

    def end_game(self):
        """Save score and finish game."""
        if not self.game_over:
            self.game_over = True
            save_score(self.username, self.score, self.distance)
