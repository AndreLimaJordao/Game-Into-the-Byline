import solve_path
import pygame
import utils


class Monster:
    def __init__(self, steps, color, start_pos, win, m, maze_map):
        self.pos = start_pos
        self.color = color
        self.steps = steps
        self.m = m
        self.win = win
        self.maze_map = maze_map

    def set_new_steps(self, steps):
        self.steps = steps

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

