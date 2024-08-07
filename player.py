import pygame
from pygame.locals import *
from pygame import mixer
from pygame import Surface

import random
from maze_generator import Maze

mixer.init()
step = mixer.Sound("assets/sounds/steps.mp3")

class Player:
    def __init__(self, win: Surface, left, right, up, down, num_pixels, side_pixel):

        self.pos_x, self.pos_y = (0, 0)
        self.width = 10
        self.height = 10
        self.color = (33, 179, 76)

        self.num_steps = 0
        self.x_movement = 0
        self.y_movement = 0
        self.old_pos_x, self.old_pos_y = (0, 0)
        self.new_pos_x, self.new_pos_y = (0, 0)

        self.window = win
        self.left = left
        self.right = right
        self.up = up
        self.down = down
        self.speed = side_pixel
        self.num_pixels = num_pixels

    def spawn(self):

        self.pos_x = random.randint(0, self.num_pixels - 1)
        if self.pos_x in [0, self.num_pixels - 1]:
            self.pos_y = random.randint(0, self.num_pixels - 1)
        else:
            self.pos_y = random.choice([0, self.num_pixels - 1])

    def draw(self, maze_position):

        x_maze, y_maze = maze_position
        pos_x = self.pos_x * self.speed + x_maze + (self.speed - self.width) / 2
        pos_y = self.pos_y * self.speed + y_maze + (self.speed - self.height) / 2

        pygame.draw.rect(self.window, self.color, (pos_x, pos_y, self.width, self.height))

    def control(self, event, maze: Maze):

        if event.key in [self.left, self.right, self.up, self.down]:

            if self.num_steps == 0:

                directions = {
                    self.left: ["W", [-0.2, 0]],
                    self.right: ["E", [0.2, 0]],
                    self.up: ["N", [0, -0.2]],
                    self.down: ["S", [0, 0.2]]
                }

                possible_directions = maze.maze_map[(self.pos_y + 1, self.pos_x + 1)]
                direction = directions[event.key][0]

                if possible_directions[direction]:
                    step.play()

                    movement = directions[event.key][1]
                    self.x_movement = movement[0]
                    self.y_movement = movement[1]

                    self.old_pos_x = self.pos_x
                    self.old_pos_y = self.pos_y

                    self.new_pos_x = self.pos_x + self.x_movement * 5
                    self.new_pos_y = self.pos_y + self.y_movement * 5

                    # wall_position = wall_new_y + 1, wall_new_x + 1
                    self.num_steps = 5


        """
            if possible_directions[direction]:
                step.play()
                wall_new_x = self.pos_x + x_movement * 10
                wall_new_y = self.pos_y + y_movement * 10
                #wall_position = wall_new_y + 1, wall_new_x + 1
                wall_position = wall_new_x, wall_new_y
                for _ in range(10):

                    #self.window.fill((0, 0, 0), (int(self.pos_x) * 30 + 57.5, int(self.pos_y) * 30 + 57.5, 30, 30))
                    #self.window.fill((0, 0, 0), (wall_new_x * 30 + 57.5, wall_new_y * 30 + 57.5, 30, 30))

                    self.pos_x = round(self.pos_x + x_movement, 1)
                    self.pos_y = round(self.pos_y + y_movement, 1)

                    #maze.display_maze_cells(self.window, (255, 255, 255), [[self.position]])
                    maze.display_maze_cells(self.window, (255, 255, 255), [[wall_position]])

                    self.draw((57.5, 57.5))

                    pygame.display.update((self.pos_x * 30 + 57.5, self.pos_y * 30 + 57.5, 30, 30))

                    #pygame.time.delay(1)
        """



        #print(self.pos_x, self.pos_y)

    def move(self, maze, flash_list, glostick_list, boxes_list):

        if self.num_steps > 0:

            cells_flash = []
            cells_glow = []
            cells_box = []

            for cell_list in flash_list:
                for cell in cell_list:
                    cells_flash.append(cell)

            for cell_list in glostick_list:
                for cell in cell_list:
                    cells_glow.append(cell)

            for y_box, x_box in boxes_list:
                cells_box.append((x_box - 1, y_box - 1))

            if (self.old_pos_x, self.old_pos_y) not in cells_box:
                self.window.fill((0, 0, 0), (self.old_pos_x * 30 + 57.5, self.old_pos_y * 30 + 57.5, 30, 30))
            self.window.fill((0, 0, 0), (self.new_pos_x * 30 + 57.5, self.new_pos_y * 30 + 57.5, 30, 30))

            if (self.old_pos_x, self.old_pos_y) not in [*cells_glow, *cells_flash]:
                pygame.display.update((self.old_pos_x * 30 + 57.5, self.old_pos_y * 30 + 57.5, 30, 30,))

            self.pos_x = round(self.pos_x + self.x_movement, 1)
            self.pos_y = round(self.pos_y + self.y_movement, 1)

            #pygame.display.update((self.old_pos_x * 30 + 57.5, self.old_pos_y * 30 + 57.5, 30, 30,))

            if (self.new_pos_x, self.new_pos_y) not in cells_glow:
                maze.display_maze_cells(self.window, (255, 255, 255), [[self.position]])
            else:
                maze.display_maze_cells(self.window, (222, 252, 8), [[self.position]])

            if (self.old_pos_x, self.old_pos_y) not in cells_glow:
                maze.display_maze_cells(self.window, (255, 255, 255), [[self.old_position]])
            else:
                maze.display_maze_cells(self.window, (222, 252, 8), [[self.old_position]])

            self.draw((57.5, 57.5))

            pygame.display.update((self.pos_x * 30 + 57.5, self.pos_y * 30 + 57.5, 30, 30,))

            #pygame.time.delay(1000)

            print(self.pos_x, self.pos_y)

            self.num_steps -= 1

        #if self.num_steps == 0:
            #self.draw((57.5, 57.5))
            #pygame.display.update((self.pos_x * 30 + 57.5, self.pos_y * 30 + 57.5, 30, 30,))
            #maze.display_maze_cells(self.window, (255, 255, 255), [[self.get_position()]])


    def get_position(self):
        return self.pos_x, self.pos_y

    def get_position_maze(self):
        return self.pos_y + 1, self.pos_x + 1

    @property
    def position(self):
        return self.new_pos_x, self.new_pos_y

    @property
    def position_maze(self):
        return self.new_pos_y + 1, self.new_pos_x + 1

    @property
    def old_position(self):
        return self.old_pos_x, self.old_pos_y
