import pygame
import pymunk
import sys
import random
from src.physics import Physics
from src.tetrino import Tetrino
from src.board import Board

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()
        play_area_rect = (250, 0, 300, 600)  # Adjust based on your screen size
        self.physics = Physics(play_area_rect)
        self.board = Board(self.physics, play_area_rect, screen)
        self.spawn_location = (300, 50)
        self.tetrinos = []
        self.spawn_new_tetrino()

    def spawn_new_tetrino(self):
        self.current_tetrino = Tetrino(*self.spawn_location)
        self.tetrinos.append(self.current_tetrino)
        self.physics.add_tetrino(self.current_tetrino)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.current_tetrino.body.position += (-20, 0)
                elif event.key == pygame.K_RIGHT:
                    self.current_tetrino.body.position += (20, 0)
                elif event.key == pygame.K_UP:
                    self.current_tetrino.rotate(clockwise=True)
                elif event.key == pygame.K_DOWN:
                    self.current_tetrino.rotate(clockwise=False)
                elif event.key == pygame.K_SPACE:
                    self.spawn_new_tetrino()

    def update(self):
        self.physics.space.step(1/60.0)

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.board.draw()  # Draw the play area and its border
        for tetrino in self.tetrinos:
            tetrino.draw(self.screen)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()
