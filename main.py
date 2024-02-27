import pygame
import sys
from src.game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Tetris with Physics')

    game = Game(screen)

    # Main game loop
    while game.running:
        game.handle_events()  # Handle events in the Game class
        game.update()  # Update game logic
        game.draw()  # Draw the game state to the screen
        pygame.display.flip()  # Update the full display Surface to the screen
        game.clock.tick(60)  # Limit the frame rate to 60 FPS

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
