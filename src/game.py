import pygame
import sys
from time import time
import numpy as np
from src.physics import Physics
from src.tetrino import Tetrino
from src.controls import Controls
from src.board import Board

class Game:
    def __init__(self, screen, config):
        self.screen = screen
        self.config = config
        self.running = True
        self.paused = False
        self.clock = pygame.time.Clock()
        self.play_area_rect = config['play_area_rect']
        self.physics = Physics(self)
        self.board = Board(self)
        self.spawn_location = config['spawn_location']
        self.controls = Controls(self)
        self.tetrinos = []
        self.spawn_new_tetrino()
        self.elapsed_time = 0

        # UI Elements
        self.ui_font = pygame.font.Font(None, config['text_size'])
        self.pause_button_rect = pygame.Rect(config['UI_rect'][0], config['UI_rect'][1], config['button_size'][0], config['button_size'][1])
        self.reset_button_rect = pygame.Rect(config['UI_rect'][0], config['UI_rect'][1] + 60, config['button_size'][0], config['button_size'][1])

        self.slider_rect = pygame.Rect(config['slider_rect'])
        self.slider_button_rect = pygame.Rect(self.slider_rect.x, self.slider_rect.y - 5, 10, self.slider_rect.height + 10)  # Slider button
        self.slider_value = 1.0  # Default gravity multiplier
        self.dragging_slider = False


        # Score Management
        self.current_score = 0
        self.high_score = 0

    def spawn_new_tetrino(self):
        self.current_tetrino = Tetrino(*self.spawn_location, self)
        self.tetrinos.append(self.current_tetrino)
        self.physics.add_tetrino(self.current_tetrino)

    def update(self):
        self.physics.space.step(1/60.0)        

    def calculate_score(self):
        self.current_score = np.around((len(self.tetrinos) / self.elapsed_time) * 10, 2 )

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.draw_ui()
        self.board.draw()  # Draw the play area and its border
        for tetrino in self.tetrinos:
            tetrino.draw(self.screen)

    def run(self):
        while self.running:
            self.controls.handle_events()
            if not self.paused:
                self.update()
                self.elapsed_time += 1/60
            self.draw()
            pygame.display.flip()
            self.calculate_score()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()


    def draw_ui(self):
        # Draw Pause Button
        pygame.draw.rect(self.screen, (200, 200, 200), self.pause_button_rect)
        pause_text = self.ui_font.render('Pause' if not self.paused else 'Resume', True, (0, 0, 0))
        self.screen.blit(pause_text, pause_text.get_rect(center=self.pause_button_rect.center))

        # Draw Reset Button
        pygame.draw.rect(self.screen, (200, 200, 200), self.reset_button_rect)
        reset_text = self.ui_font.render('Reset', True, (0, 0, 0))
        self.screen.blit(reset_text, reset_text.get_rect(center=self.reset_button_rect.center))

        # Draw Score
        score_text = self.ui_font.render(f'Score: {self.current_score}', True, (255, 255, 255))
        self.screen.blit(score_text, (self.config['UI_rect'][0], self.config['UI_rect'][1] + 120))

        # Draw High Score
        high_score_text = self.ui_font.render(f'High Score: {self.high_score}', True, (255, 255, 255))
        self.screen.blit(high_score_text, (self.config['UI_rect'][0], self.config['UI_rect'][1] + 150))

        # draw gravity slider
        pygame.draw.rect(self.screen, (180, 180, 180), self.slider_rect)
        pygame.draw.rect(self.screen, (100, 100, 100), self.slider_button_rect)

        # Draw the label
        label_text = self.ui_font.render('Gravity', True, (255, 255, 255))
        self.screen.blit(label_text, (self.config['UI_rect'][0], self.slider_rect.y - 30))



    def reset(self):
        for t in self.tetrinos:
            self.physics.remove_tetrino(t)
        self.tetrinos = []
        self.spawn_new_tetrino()
        if self.current_score > self.high_score:
            self.high_score = self.current_score
        self.elapsed_time = 0
        self.running = True