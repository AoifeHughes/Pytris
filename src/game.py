import pygame
import pymunk
import sys
import random
from src.physics import Physics
from src.tetrino import Tetrino
from src.controls import Controls
from src.board import Board

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()
        self.play_area_rect = (250, 0, 300, 600)  # Adjust based on your screen size
        self.physics = Physics(self.play_area_rect)
        self.board = Board(self.physics, self.play_area_rect, screen)
        self.spawn_location = (300, 50)
        self.controls = Controls(self)
        self.tetrinos = []
        self.spawn_new_tetrino()

    def spawn_new_tetrino(self):
        self.current_tetrino = Tetrino(*self.spawn_location)
        self.tetrinos.append(self.current_tetrino)
        self.physics.add_tetrino(self.current_tetrino)

    def update(self):
        self.physics.space.step(1/60.0)        


    def draw(self):
        self.screen.fill((0, 0, 0))
        self.board.draw()  # Draw the play area and its border
        for tetrino in self.tetrinos:
            tetrino.draw(self.screen)

    def run(self):
        while self.running:
            self.controls.handle_events()  # Modified line
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()


    def reset(self):
        for t in self.tetrinos:
            self.physics.remove_tetrino(t)
        self.tetrinos = []
        self.spawn_new_tetrino()
        self.running = True