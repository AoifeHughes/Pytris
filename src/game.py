import pygame
import pymunk
import sys
from src.physics import Physics
from src.tetrino import Tetrino
from src.board import Board

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()
        self.physics = Physics()
        self.board = Board(self.physics)
        self.current_tetrino = Tetrino(100, 100, 'O', 'blue')
        self.current_tetrino.add_to_physics_space(self.physics.space)
        self.tetrinos = [self.current_tetrino]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    # Move left instantly
                    self.current_tetrino.body.position += (-20, 0)
                elif event.key == pygame.K_RIGHT:
                    # Move right instantly
                    self.current_tetrino.body.position += (20, 0)
                elif event.key == pygame.K_UP:
                    # Rotate clockwise
                    self.current_tetrino.rotate(clockwise=True)
                elif event.key == pygame.K_DOWN:
                    # Rotate counter-clockwise
                    self.current_tetrino.rotate(clockwise=False)
                elif event.key == pygame.K_SPACE:
                    # Drop to the bottom instantly (this will need further implementation to stop at the bottom)
                    self.current_tetrino.body.velocity = pymunk.Vec2d(0, -1000)  # Temp high downward velocity


    def update(self):

        self.physics.space.step(1/60.0)  # Physics simulation step

    def draw(self):
        self.screen.fill((0, 0, 0))  # Clear screen with black
        for tetrino in self.tetrinos:
            tetrino.draw(self.screen)  # Draw each tetrino

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()  # Update the full display Surface to the screen
            self.clock.tick(60)  # Limit frame rate to 60 FPS

        pygame.quit()
        sys.exit()
