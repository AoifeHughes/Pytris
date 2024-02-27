import pymunk
from pygame.color import THECOLORS
import pygame
import numpy as np

class Tetrino:
    def __init__(self, x, y, shape_type, color):
        self.x = x
        self.y = y
        self.shape_type = shape_type
        self.color = THECOLORS[color]
        self.blocks = self.create_blocks()
        self.shapes = []
        self.body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
        self.body.position = x, y
        self.add_mass_and_moment()

    def create_blocks(self):
        blocks = []
        # Define Tetris shapes with their relative block positions
        if self.shape_type == 'I':
            blocks = [(-1.5, 0), (-0.5, 0), (0.5, 0), (1.5, 0)]
        elif self.shape_type == 'O':
            blocks = [(0, 0), (1, 0), (0, 1), (1, 1)]
        elif self.shape_type == 'T':
            blocks = [(-1, 0), (0, 0), (1, 0), (0, 1)]
        elif self.shape_type == 'J':
            blocks = [(-1, 0), (0, 0), (1, 0), (-1, 1)]
        elif self.shape_type == 'L':
            blocks = [(-1, 0), (0, 0), (1, 0), (1, 1)]
        elif self.shape_type == 'S':
            blocks = [(-1, 0), (0, 0), (0, 1), (1, 1)]
        elif self.shape_type == 'Z':
            blocks = [(1, 0), (0, 0), (0, 1), (-1, 1)]
        return blocks

    def add_mass_and_moment(self):
        # Calculate the moment for a box which approximates the tetrino
        mass = 1.0  # Arbitrary mass
        moment = pymunk.moment_for_box(mass, (20, 20))  # Approximate the tetrino as a box
        self.body.mass = mass
        self.body.moment = moment

    def add_to_physics_space(self, space):
        space.add(self.body)
        for block in self.blocks:
            offset_x, offset_y = block
            width, height = 20, 20  # Block size
            vertices = [(-width / 2, -height / 2), (-width / 2, height / 2), (width / 2, height / 2), (width / 2, -height / 2)]
            vertices = [(x + offset_x * width, y + offset_y * height) for x, y in vertices]
            shape = pymunk.Poly(self.body, vertices)
            shape.density = 1.0  # Density to determine mass of the shape
            shape.elasticity = 0.5  # Bounciness
            shape.friction = 0.5  # Friction with other objects
            self.shapes.append(shape)
            space.add(shape)

    def draw(self, screen):
        outline_color = THECOLORS['white']  # Color for the outline
        for shape in self.shapes:
            vertices = shape.get_vertices()
            points = [(v.rotated(self.body.angle) + self.body.position) for v in vertices]

            # Draw the polygon with the tetrino color
            pygame.draw.polygon(screen, self.color, points)

            # Draw the outline around the polygon
            pygame.draw.polygon(screen, outline_color, points, 1)  # The last argument is the thickness of the line


    def rotate(self, clockwise=True):
        angle = np.radians(15) if clockwise else -np.radians(15)
        self.body.angle += angle
