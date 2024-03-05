import pygame
import sys
from src.game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Tetris with Physics')

    game = Game(screen)
    game.run()

if __name__ == "__main__":
    main()
