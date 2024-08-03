import solve_path
import pygame
import utils
import random

class Monster:
    def __init__(self, steps, color, start_pos, win, m, maze_map):
        self.pos = start_pos
        self.color = color
        self.steps = steps
        self.m = m
        self.win = win
        self.maze_map = maze_map

        self.radar_position = (-1, -1)

    def set_new_steps(self, steps):
        self.steps = steps

    def set_start_position(self, player_position):
        if player_position[0] <= 10 and player_position[1] <= 10:
            self.pos = (random.randint(16, 20), random.randint(16, 20))
        elif player_position[0] > 10 and player_position[1] <= 10:
            self.pos = (random.randint(1, 5), random.randint(16, 20))
        elif player_position[0] <= 10 and player_position[1] > 10:
            self.pos = (random.randint(16, 20), random.randint(1, 5))
        elif player_position[0] > 10 and player_position[1] > 10:
            self.pos = (random.randint(1, 5), random.randint(1, 5))

    def move(self, position):
        path = solve_path.solve_path(self.pos, position, self.maze_map)
        try:
            for i in range(self.steps):
                self.pos = path[self.pos]
            return False
        except:
            return True

    def draw(self):
        mons = pygame.Surface((14, 14))
        mons.fill(self.color)

        pixel_xy = utils.cell_to_pixels(self.m, self.pos)
        cell_rect = pygame.Rect(pixel_xy, (self.m.cell_grid_width, self.m.cell_grid_width))
        self.win.blit(mons, (cell_rect.centerx - 7, cell_rect.centery - 7))

    def position(self):
        x, y = self.pos
        return y - 1, x - 1

    def active_radar(self):
        self.radar_position = self.pos

    def disable_radar(self):
        self.radar_position = (-1, -1)

    def get_radar_position(self):
        return self.radar_position
