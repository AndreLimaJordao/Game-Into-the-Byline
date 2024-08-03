import pygame
import utils
from pygame import mixer
from pygame.locals import *
import random

from player import Player
from flash import Flash
from monster import Monster
from maze_generator import Maze


class Inventory(pygame.sprite.Sprite):
    def __init__(self, window, maze: Maze, flash: Flash, player: Player, billy: Monster, bob: Monster):
        pygame.sprite.Sprite.__init__(self)

        # key, glowstick, super battery, radar
        self.inventory = {"k": 0, "g": 1, "r": 2, "s": 1}

        self.key_glowstick = K_1
        self.key_radar = K_2
        self.key_battery = K_3
        self.battery_trigger = False
        self.door_position = (-1, -1)
        self.timer_door = 255

        self.window = window
        self.maze = maze
        self.player = player
        self.flash = flash
        self.billy = billy
        self.bob = bob

    def try_generate_door(self):
        x_door, y_door = self.door_position
        if self.inventory["k"] == 3 and self.door_position == (-1, -1):
            x_player, y_player = self.player.position

            while abs(x_player - x_door) < 10 or abs(y_player - y_door) < 10:
                x_door = random.randint(0, self.maze.num_pixels - 1)
                y_door = random.randint(0, self.maze.num_pixels - 1)

            self.door_position = x_door, y_door

        if self.door_position != (-1, -1) and self.timer_door >= 0:
            pixel_x_maze = self.maze.initial_point_x + (x_door * self.maze.cell_grid_width) + 10
            pixel_y_maze = self.maze.initial_point_y + (y_door * self.maze.cell_grid_width) + 10

            surface_door = pygame.Surface((10, 10), pygame.SRCALPHA)

            surface_door.fill((12, 134, 122, self.timer_door))
            self.window.blit(surface_door, (pixel_x_maze, pixel_y_maze))
            self.timer_door -= 5

    def get_door_position(self):
        return self.door_position

    def add_item(self, item):
        if item in self.inventory:
            self.inventory[item] += 1
            print(self.inventory)

    def use_item(self, event):
        flash_trigger = self.flash.get_trigger(event)

        if event.key == self.key_glowstick and self.inventory["g"] > 0:
            self.inventory["g"] -= 1
            print("Usar Glowstick")
            self.flash.glowstick(self.player.position)

        elif event.key == self.key_radar and self.inventory["r"] > 0:
            self.inventory["r"] -= 1
            print("Usar Radar")
            #x_billy, y_billy = self.billy.position()
            #x_bob, y_bob = self.bob.position()
            #pygame.draw.rect(self.window, (255, 0, 0), (x_billy, y_billy, 14, 14))
            #pygame.draw.rect(self.window, (255, 0, 0), (x_bob, y_bob, 14, 14))
            self.billy.active_radar()
            self.bob.active_radar()

        elif event.key == self.key_battery and self.inventory["s"] > 0:
            self.battery_trigger = not self.battery_trigger
            if self.battery_trigger:
                self.flash.set_type_battery()
            else:
                self.flash.reset_type_battery()

        elif flash_trigger:
            self.billy.disable_radar()
            self.bob.disable_radar()
            if self.battery_trigger:
                print("Usar Bateria")
                self.inventory["s"] -= 1
                self.battery_trigger = not self.battery_trigger

    def get_trigger(self, event: pygame.event) -> bool:
        flash_trigger = self.flash.get_trigger(event)
        if event.key in [self.key_glowstick, self.key_radar] or flash_trigger and not self.battery_trigger:
            return True
        else:
            return False

    def get_inventory(self):
        return self.inventory

    def get_battery(self):
        if self.battery_trigger:
            return True
        else:
            return False


