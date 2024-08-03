import pygame
from pygame.locals import *
from pygame import mixer
import random

mixer.init()
step = mixer.Sound("assets/sounds/steps.mp3")

class Player:
    def __init__(self, win, left, right, up, down, num_pixels, side_pixel):

        self.pos_x, self.pos_y = (0, 0)
        self.width = 10
        self.height = 10
        self.color = (33, 179, 76)
        self.inventory = {"k": 0, "g": 1, "s": 1, "r": 1}

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

    def add_inventory(self, item):
        if item in self.inventory:
            self.inventory[item] += 1
            print(self.inventory)

    def draw(self, maze_position):

        x_maze, y_maze = maze_position
        pos_x = self.pos_x * self.speed + x_maze + (self.speed - self.width) / 2
        pos_y = self.pos_y * self.speed + y_maze + (self.speed - self.height) / 2

        pygame.draw.rect(self.window, self.color, (pos_x, pos_y, self.width, self.height))

    def control(self, event, maze_map):

        possible_directions = maze_map[(self.pos_y + 1, self.pos_x + 1)]

        if event.key in [self.left, self.right, self.up, self.down]:

            directions = {
                self.left: ["W", [-1, 0]],
                self.right: ["E", [1, 0]],
                self.up: ["N", [0, -1]],
                self.down: ["S", [0, 1]]
            }

            direction = directions[event.key][0]
            movement = directions[event.key][1]
            x_movement = movement[0]
            y_movement = movement[1]

            if possible_directions[direction]:
                self.pos_x += x_movement
                self.pos_y += y_movement
                step.play()

    def get_position(self):
        return self.pos_x, self.pos_y

    def get_position_maze(self):
        return self.pos_y + 1, self.pos_x + 1

    @property
    def position(self):
        return self.pos_x, self.pos_y

    @property
    def position_maze(self):
        return self.pos_y + 1, self.pos_x + 1
