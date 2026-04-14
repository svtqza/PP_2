import pygame
from player import MusicPlayer


def main():
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((800, 400))
    pygame.display.set_caption("Music Player")

    app = MusicPlayer(screen)
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    app.play()
                elif event.key == pygame.K_s:
                    app.stop()
                elif event.key == pygame.K_n:
                    app.next_track()
                elif event.key == pygame.K_b:
                    app.previous_track()
                elif event.key == pygame.K_q:
                    running = False

        app.update()
        app.draw()
        pygame.display.flip()
        clock.tick(30)

    pygame.mixer.music.stop()
    pygame.quit()


if __name__ == "__main__":
    main()