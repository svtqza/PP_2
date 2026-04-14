import os
import pygame


class MusicPlayer:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = self.screen.get_size()

        self.font_title = pygame.font.SysFont("Arial", 34)
        self.font_text = pygame.font.SysFont("Arial", 24)
        self.font_small = pygame.font.SysFont("Arial", 20)

        self.music_folder = "music"
        self.playlist = self.load_playlist()
        self.current_index = 0
        self.is_playing = False

    def load_playlist(self):
        if not os.path.exists(self.music_folder):
            os.makedirs(self.music_folder)

        files = []
        for file_name in os.listdir(self.music_folder):
            if file_name.lower().endswith((".mp3", ".wav", ".ogg")):
                files.append(os.path.join(self.music_folder, file_name))

        files.sort()
        return files

    def get_current_track(self):
        if not self.playlist:
            return None
        return self.playlist[self.current_index]

    def get_current_track_name(self):
        track = self.get_current_track()
        if track is None:
            return "No track"
        return os.path.basename(track)

    def play(self):
        if not self.playlist:
            return

        track = self.get_current_track()
        pygame.mixer.music.load(track)
        pygame.mixer.music.play()
        self.is_playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def next_track(self):
        if not self.playlist:
            return

        self.current_index = (self.current_index + 1) % len(self.playlist)
        self.play()

    def previous_track(self):
        if not self.playlist:
            return

        self.current_index = (self.current_index - 1) % len(self.playlist)
        self.play()

    def get_track_position_seconds(self):
        pos_ms = pygame.mixer.music.get_pos()
        if pos_ms < 0:
            return 0
        return pos_ms // 1000

    def update(self):
        if self.is_playing and not pygame.mixer.music.get_busy():
            if self.playlist:
                self.next_track()

    def draw_progress_bar(self, x, y, w, h):
        pygame.draw.rect(self.screen, (120, 120, 120), (x, y, w, h), border_radius=6)

        seconds = self.get_track_position_seconds()
        progress_width = min(w, seconds * 12)

        pygame.draw.rect(self.screen, (70, 200, 120), (x, y, progress_width, h), border_radius=6)

    def draw(self):
        self.screen.fill((25, 25, 30))

        title = self.font_title.render("Music Player", True, (255, 255, 255))
        self.screen.blit(title, (290, 30))

        if self.playlist:
            playlist_text = self.font_text.render(
                f"Current track: {self.get_current_track_name()}",
                True,
                (230, 230, 230)
            )
        else:
            playlist_text = self.font_text.render(
                "No music files found in /music folder",
                True,
                (230, 80, 80)
            )

        self.screen.blit(playlist_text, (60, 110))

        status = "Playing" if self.is_playing and pygame.mixer.music.get_busy() else "Stopped"
        status_text = self.font_text.render(f"Status: {status}", True, (230, 230, 230))
        self.screen.blit(status_text, (60, 160))

        pos_text = self.font_text.render(
            f"Position: {self.get_track_position_seconds()} sec",
            True,
            (230, 230, 230)
        )
        self.screen.blit(pos_text, (60, 210))

        self.draw_progress_bar(60, 260, 680, 25)

        controls = [
            "Controls:",
            "P = Play",
            "S = Stop",
            "N = Next track",
            "B = Previous track",
            "Q = Quit"
        ]

        y = 320
        for line in controls:
            text_surface = self.font_small.render(line, True, (200, 200, 200))
            self.screen.blit(text_surface, (60, y))
            y += 30