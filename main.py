import pygame
import sys
from src.game import Game
import json
import numpy as np 

def main():
    config = json.load(open('config.json'))
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Tetris with Physics')
    game = Game(screen, config)
    game.run()

if __name__ == "__main__":
    main()
