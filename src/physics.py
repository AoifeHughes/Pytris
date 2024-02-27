import pymunk

class Physics:
    def __init__(self):
        self.space = pymunk.Space()
        self.space.gravity = (0, 98.1)  # Gravity directed downwards

        # Create a floor at the bottom of the screen
        # Assuming `window_height` is the height of your game window
        window_height = 600
        floor_height = window_height - 50  # Adjust `50` to place the floor as desired
        floor_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        floor_shape = pymunk.Segment(floor_body, (0, floor_height), (800, floor_height), 5)
        floor_shape.elasticity = 0.4
        floor_shape.friction = 0.5
        self.space.add(floor_body, floor_shape)

    def add_tetrino(self, tetrino):
        tetrino.add_to_physics_space(self.space)

    def remove_tetrino(self, tetrino):
        for shape in tetrino.shapes:
            self.space.remove(shape)
        self.space.remove(tetrino.body)

    def step(self, dt):
        self.space.step(dt)
