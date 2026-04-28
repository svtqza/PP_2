# main.py
import pygame
import sys
from racer import RacerGame, WIDTH, HEIGHT
from ui import Button, draw_center_text
from persistence import load_settings, save_settings, load_leaderboard


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS3 Racer Game")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (230, 230, 230)
BLUE = (50, 130, 255)
RED = (220, 20, 60)
GREEN = (0, 170, 70)

font = pygame.font.SysFont("Verdana", 22)
small_font = pygame.font.SysFont("Verdana", 18)
big_font = pygame.font.SysFont("Verdana", 44)

settings = load_settings()
username = "Player"


def ask_username():
    """Ask username before starting the game."""
    global username

    name = ""
    active = True

    while active:
        screen.fill(WHITE)
        draw_center_text(screen, "Enter your name", big_font, BLACK, 180)

        input_rect = pygame.Rect(100, 280, 300, 50)
        pygame.draw.rect(screen, GRAY, input_rect)
        pygame.draw.rect(screen, BLACK, input_rect, 2)

        text = font.render(name + "|", True, BLACK)
        screen.blit(text, (input_rect.x + 10, input_rect.y + 10))

        draw_center_text(screen, "Press Enter to start", small_font, BLACK, 370)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if name.strip():
                        username = name.strip()
                    else:
                        username = "Player"
                    active = False

                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]

                elif event.key == pygame.K_ESCAPE:
                    active = False

                else:
                    if event.unicode:
                        name += event.unicode

        pygame.display.update()
        clock.tick(60)


def main_menu():
    """Main menu screen."""
    buttons = [
        Button(150, 220, 200, 50, "Play", font),
        Button(150, 290, 200, 50, "Leaderboard", font),
        Button(150, 360, 200, 50, "Settings", font),
        Button(150, 430, 200, 50, "Quit", font)
    ]

    while True:
        screen.fill(WHITE)
        draw_center_text(screen, "TSIS3 Racer", big_font, BLACK, 130)

        mouse_pos = pygame.mouse.get_pos()

        for button in buttons:
            button.draw(screen, mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if buttons[0].is_clicked(event):
                ask_username()
                run_game()

            elif buttons[1].is_clicked(event):
                leaderboard_screen()

            elif buttons[2].is_clicked(event):
                settings_screen()

            elif buttons[3].is_clicked(event):
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(60)


def settings_screen():
    """Settings screen: sound, car color, difficulty."""
    global settings

    colors = ["blue", "red", "green", "yellow", "purple"]
    difficulties = ["easy", "normal", "hard"]

    buttons = [
        Button(120, 200, 260, 45, "Toggle Sound", font),
        Button(120, 270, 260, 45, "Change Car Color", font),
        Button(120, 340, 260, 45, "Change Difficulty", font),
        Button(120, 470, 260, 45, "Back", font)
    ]

    while True:
        screen.fill(WHITE)
        draw_center_text(screen, "Settings", big_font, BLACK, 100)

        sound_text = f"Sound: {'ON' if settings['sound'] else 'OFF'}"
        color_text = f"Car color: {settings['car_color']}"
        difficulty_text = f"Difficulty: {settings['difficulty']}"

        screen.blit(small_font.render(sound_text, True, BLACK), (140, 160))
        screen.blit(small_font.render(color_text, True, BLACK), (140, 235))
        screen.blit(small_font.render(difficulty_text, True, BLACK), (140, 305))

        mouse_pos = pygame.mouse.get_pos()

        for button in buttons:
            button.draw(screen, mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if buttons[0].is_clicked(event):
                settings["sound"] = not settings["sound"]
                save_settings(settings)

            elif buttons[1].is_clicked(event):
                index = colors.index(settings["car_color"])
                settings["car_color"] = colors[(index + 1) % len(colors)]
                save_settings(settings)

            elif buttons[2].is_clicked(event):
                index = difficulties.index(settings["difficulty"])
                settings["difficulty"] = difficulties[(index + 1) % len(difficulties)]
                save_settings(settings)

            elif buttons[3].is_clicked(event):
                return

        pygame.display.update()
        clock.tick(60)


def leaderboard_screen():
    """Display top 10 leaderboard."""
    back_button = Button(150, 610, 200, 45, "Back", font)

    while True:
        screen.fill(WHITE)
        draw_center_text(screen, "Leaderboard Top 10", big_font, BLACK, 70)

        leaderboard = load_leaderboard()

        y = 140

        if not leaderboard:
            draw_center_text(screen, "No scores yet", font, BLACK, 250)
        else:
            header = small_font.render("Rank   Name        Score      Distance", True, BLACK)
            screen.blit(header, (55, 115))

            for i, item in enumerate(leaderboard[:10], start=1):
                line = f"{i:<5} {item['name']:<10} {item['score']:<10} {item['distance']}m"
                text = small_font.render(line, True, BLACK)
                screen.blit(text, (55, y))
                y += 35

        mouse_pos = pygame.mouse.get_pos()
        back_button.draw(screen, mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if back_button.is_clicked(event):
                return

        pygame.display.update()
        clock.tick(60)


def run_game():
    """Run main game loop."""
    game = RacerGame(screen, username, settings)

    while not game.game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        game.update()
        game.draw()

        pygame.display.update()
        clock.tick(60)

    game_over_screen(game)


def game_over_screen(game):
    """Game over screen with retry and main menu buttons."""
    retry_button = Button(150, 450, 200, 50, "Retry", font)
    menu_button = Button(150, 520, 200, 50, "Main Menu", font)

    while True:
        screen.fill(WHITE)

        title = "Finished!" if game.finished else "Game Over"
        draw_center_text(screen, title, big_font, RED, 120)

        stats = [
            f"Name: {username}",
            f"Score: {int(game.score)}",
            f"Distance: {int(game.distance)} m",
            f"Coins: {game.coins}"
        ]

        y = 220
        for stat in stats:
            draw_center_text(screen, stat, font, BLACK, y)
            y += 40

        mouse_pos = pygame.mouse.get_pos()
        retry_button.draw(screen, mouse_pos)
        menu_button.draw(screen, mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if retry_button.is_clicked(event):
                run_game()
                return

            if menu_button.is_clicked(event):
                return

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main_menu()
