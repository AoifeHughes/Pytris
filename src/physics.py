import pymunk

class Physics:
    def __init__(self, game):
        self.space = pymunk.Space()
        self.space.gravity = (0, game.config['gravity']* game.config['gravity_factor'])  # Gravity directed downwards
        self.create_play_area_boundaries(game.config['play_area_rect'])


    def create_play_area_boundaries(self, rect):
        x, y, width, height = rect
        boundaries = [
            pymunk.Segment(self.space.static_body, (x, y), (x + width, y), 1),  # Top
            pymunk.Segment(self.space.static_body, (x, y), (x, y + height), 1),  # Left
            pymunk.Segment(self.space.static_body, (x + width, y), (x + width, y + height), 1),  # Right
            pymunk.Segment(self.space.static_body, (x, y + height), (x + width, y + height), 1)  # Bottom
        ]
        for boundary in boundaries:
            boundary.elasticity = 0.4
            boundary.friction = 0.5
        self.space.add(*boundaries)

    def update_gravity(self, value):
        self.space.gravity = (0, value)

    def add_tetrino(self, tetrino):
        # Assign collision type to tetrino
        for shape in tetrino.shapes:
            shape.collision_type = 1
        tetrino.add_to_physics_space(self.space)

    def remove_tetrino(self, tetrino):
        for shape in tetrino.shapes:
            self.space.remove(shape)
        self.space.remove(tetrino.body)

    def step(self, dt):
        self.space.step(dt)
