import pygame
import random
from pygame.locals import *
from pygame import mixer

flash_sound = mixer.Sound("assets/sounds/flash_sound.mp3")


class Flash(pygame.sprite.Sprite):
    def __init__(self, win: pygame.Surface, left: int, right: int, up: int, down: int, num_flashs: int):
        pygame.sprite.Sprite.__init__(self)

        #self.image = pygame.Surface([left, right, up, down])

        self.window = win

        self.left = left
        self.right = right
        self.up = up
        self.down = down

        self.num_flashs = num_flashs

        self.flashs_list = []
        self.glowsticks_list = []

        self.battery_trigger = False
        self.super_battery_trigger = False

    def active(self, event: pygame.event, maze_map: dict, player_position: tuple):

        if event.key in [self.left, self.right, self.up, self.down]:
            flash_sound.play()

            x, y = player_position

            directions = {
                self.left: ["W", [-1, 0]],
                self.right: ["E", [1, 0]],
                self.up: ["N", [0, -1]],
                self.down: ["S", [0, 1]]
            }
            possible_directions = maze_map[(y + 1, x + 1)]

            flash_list = [(x, y)]
            direction = directions[event.key][0]
            movement = directions[event.key][1]
            print(direction)

            wall_break = 0

            while possible_directions[direction] or self.battery_trigger or self.super_battery_trigger:  # enquanto a direção estiver aberta
                x += movement[0]
                y += movement[1]

                if not possible_directions[direction]:
                    if self.battery_trigger:
                        wall_break += 1
                        if x not in range(20) or y not in range(20) or wall_break == 2:
                            break
                    elif self.super_battery_trigger:
                        if x in [-1, 20] or y in [-1, 20]:
                            break

                flash_list.append((x, y))
                possible_directions = maze_map[(y + 1, x + 1)]

            self.flashs_list.append(flash_list)
            self.light(flash_list, 57.5, 57.5)

        print("Battery:", self.battery_trigger)
        print("Super Battery:", self.super_battery_trigger)

        if len(self.flashs_list) > 1 and str(self.flashs_list[-1]) in str(self.flashs_list[:-1])[1:-1]:
            self.flashs_list.pop(-1)
        elif len(self.flashs_list) > self.num_flashs:
            self.flashs_list.pop(0)

        #return flashs_list

    def get_trigger(self, event: pygame.event):
        if event.key in [self.left, self.right, self.up, self.down]:
            return True
        else:
            return False

    def light(self, flash_list: list, x_maze: float, y_maze: float):
        if self.battery_trigger:
            color = Color((255, 221, 175, 200))
            self.battery_trigger = False
        elif self.super_battery_trigger:
            color = Color((255, 194, 175, 200))
            self.super_battery_trigger = False
        else:
            color = Color((252, 255, 175, 200))
        for x_flash, y_flash in flash_list:
            pos_x_maze = x_flash * 30 + x_maze
            pos_y_maze = y_flash * 30 + y_maze
            surface = pygame.Surface((30, 30), pygame.SRCALPHA)
            surface.fill(color)
            self.window.blit(surface, (pos_x_maze, pos_y_maze))
            pygame.display.update((x_flash * 30 + 57.5, y_flash * 30 + 57.5, 30, 30))
            #pygame.time.delay(5)

    def set_type_battery(self):
        value = random.choice([1, 2, 3, 4, 5])
        if value == 5:
            self.super_battery_trigger = True
        else:
            self.battery_trigger = True

    def reset_type_battery(self):
        self.battery_trigger = False
        self.super_battery_trigger = False

    def get_used_battery(self):
        if self.battery_trigger or self.super_battery_trigger:
            return True
        else:
            return False

    def glowstick(self, player_position: tuple):

        glowstick_position = []

        x_player, y_player = player_position

        deslocation = [(x, y) for x in range(-1, 2) for y in range(-1, 2)]

        for x, y in deslocation:
            if x_player + x in range(0, 20) and y_player + y in range(0, 20):
                glowstick_position.append((x_player + x, y_player + y))

        self.glowsticks_list.append(glowstick_position)

        #return glowsticks_list

    def get_flashs_lists(self):
        return self.flashs_list

    def get_glowsticks_list(self):
        return self.glowsticks_list
