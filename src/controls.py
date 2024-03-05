import pygame
import numpy as np

class Controls:
    def __init__(self, game):
        self.game = game

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                self.process_keydown(event.key)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.game.pause_button_rect.collidepoint(event.pos):
                    self.game.paused = not self.game.paused
                elif self.game.reset_button_rect.collidepoint(event.pos):
                    self.game.reset()

                if self.game.slider_button_rect.collidepoint(event.pos):
                    self.game.dragging_slider = True

            elif event.type == pygame.MOUSEBUTTONUP:
                self.game.dragging_slider = False

            elif event.type == pygame.MOUSEMOTION and self.game.dragging_slider:
                self.game.slider_button_rect.x = max(self.game.slider_rect.x, min(event.pos[0], self.game.slider_rect.right - self.game.slider_button_rect.width))
                self.update_gravity()


        if self.check_collision_with_floor_or_tetrinos():
            self.game.spawn_new_tetrino()

    def process_keydown(self, key):
        if key == pygame.K_LEFT:
            # Check if moving left is within bounds
            if self.is_within_left_bound():
                self.game.current_tetrino.body.position += (-self.game.config['movement_rate'], 0)
        elif key == pygame.K_RIGHT:
            # Check if moving right is within bounds
            if self.is_within_right_bound():
                self.game.current_tetrino.body.position += (self.game.config['movement_rate'], 0)
        elif key == pygame.K_UP:
            self.game.current_tetrino.rotate(clockwise=True)
        elif key == pygame.K_DOWN:
            self.game.current_tetrino.rotate(clockwise=False)

    def is_within_left_bound(self):
        # Calculate the leftmost position of any block in the Tetrino
        leftmost_block_edge = min(self.game.current_tetrino.body.position.x + (block[0] * self.game.config['block_size']) - 10 for block in self.game.current_tetrino.blocks)
        # Get the left boundary of the play area
        left_bound = self.game.board.play_area_rect[0]
        return leftmost_block_edge > left_bound

    def is_within_right_bound(self):
        # Calculate the rightmost position of any block in the Tetrino
        rightmost_block_edge = max(self.game.current_tetrino.body.position.x + (block[0] * self.game.config['block_size']) + 10 for block in self.game.current_tetrino.blocks)
        # Get the right boundary of the play area
        right_bound = self.game.play_area_rect[0] + self.game.play_area_rect[2]
        return rightmost_block_edge < right_bound
    
    def check_collision_with_roof(self):
        for tetrino in self.game.tetrinos:
            cur_pos = self.get_rotated_block_positions(tetrino) 
            for x, y in cur_pos:
                if y <= 0:  
                    return True   
        return False  # No collision with the roof        


    def check_collision_with_floor_or_tetrinos(self):
            # Get the rotated positions of the current Tetrino's blocks
            current_blocks_world_positions = self.get_rotated_block_positions(self.game.current_tetrino)

            # Check collision with floor
            play_area_bottom = self.game.play_area_rect[1] + self.game.play_area_rect[3]
            for x, y in current_blocks_world_positions:
                if y + self.game.config['block_size'] >= play_area_bottom:  # Assuming block size is 20
                    return True  # Collision with floor

            # Check collision with other Tetrinos
            if len(self.game.tetrinos) > 1:
                for settled_tetrino in self.game.tetrinos[:-1]:  # Exclude the current falling Tetrino
                    settled_blocks_world_positions = self.get_rotated_block_positions(settled_tetrino)
                    for current_block_pos in current_blocks_world_positions:
                        for settled_block_pos in settled_blocks_world_positions:
                            if settled_block_pos[1] < 100:
                                self.game.reset()
                                return False
                            if (abs(current_block_pos[0] - settled_block_pos[0]) < self.game.config['block_size'] and
                                    abs(current_block_pos[1] - settled_block_pos[1]) < self.game.config['block_size']):
                                if current_block_pos[1] < 100:
                                    self.game.reset()
                                    return False
                                return True  # Collision with another Tetrino

            return False  # No collisions

    def get_rotated_block_positions(self, tetrino):
        """Calculate the world positions of tetrino's blocks considering rotation."""
        positions = []
        angle = tetrino.body.angle  # Rotation angle in radians
        cx, cy = tetrino.body.position  # Center position of the Tetrino
        for block in tetrino.blocks:
            # Calculate block's position relative to Tetrino's center, considering rotation
            local_x, local_y = block[0] * self.game.config['block_size'], block[1] * self.game.config['block_size']  # Assuming block size is 20
            rotated_x = cx + local_x * np.cos(angle) - local_y * np.sin(angle)
            rotated_y = cy + local_x * np.sin(angle) + local_y * np.cos(angle)
            positions.append((rotated_x, rotated_y))
        return positions
    

    def update_gravity(self):
        # Update the gravity based on the slider position
        relative_position = (self.game.slider_button_rect.x - self.game.slider_rect.x) / (self.game.slider_rect.width - self.game.slider_button_rect.width)
        gravity_range = self.game.config['slider_range']
        self.slider_value = gravity_range[0] + (gravity_range[1] - gravity_range[0]) * relative_position
        self.game.physics.update_gravity(self.slider_value * self.game.config['gravity'])