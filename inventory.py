import pygame
import utils
from pygame import mixer
from pygame.locals import *
from pygame.surface import Surface as Sfc
import random

from player import Player
from flash import Flash
from monster import Monster as Mnst
from maze_generator import Maze
from score import Score

radar_sound = mixer.Sound("assets/sounds/radar.mp3")
glowstick_sound = mixer.Sound("assets/sounds/glowsticks.wav")
active_battery_sound = mixer.Sound("assets/sounds/active_battery.mp3")
disable_battery_sound = mixer.Sound("assets/sounds/disable_battery.mp3")


class Inventory(pygame.sprite.Sprite):
    def __init__(self, window: Sfc, maze: Maze, flash: Flash, player: Player, billy: Mnst, bob: Mnst, score: Score):
        pygame.sprite.Sprite.__init__(self)

        # key, glowstick, super battery, radar
        self.inventory = {"k": 0, "g": 4, "r": 2, "s": 1}

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
        self.score = score

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

            surface_door = pygame.Surface((14, 14), pygame.SRCALPHA)

            surface_door.fill((12, 134, 122, self.timer_door))
            self.window.blit(surface_door, (pixel_x_maze, pixel_y_maze))
            self.timer_door -= 5

    def get_door_position(self):
        return self.door_position

    def get_door_position_maze(self):
        x_door, y_door = self.door_position
        return y_door + 1, x_door + 1

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
            glowstick_sound.play()
            self.score.set_highscore(200)

        elif event.key == self.key_radar and self.inventory["r"] > 0:
            self.inventory["r"] -= 1
            print("Usar Radar")
            self.billy.active_radar()
            self.bob.active_radar()
            radar_sound.play()
            self.score.set_highscore(200)

        elif event.key == self.key_battery and self.inventory["s"] > 0:
            self.battery_trigger = not self.battery_trigger
            if self.battery_trigger:
                self.flash.set_type_battery()
                active_battery_sound.play()
            else:
                self.flash.reset_type_battery()
                disable_battery_sound.play()

        elif flash_trigger:
            self.billy.disable_radar()
            self.bob.disable_radar()
            if self.battery_trigger:
                print("Usar Bateria")
                self.inventory["s"] -= 1
                self.battery_trigger = not self.battery_trigger
                self.score.set_highscore(200)

    def draw_glowstick(self, boxes_list):
        glowstick_sequences = []

        for glowstick_list in self.flash.glowsticks_list:
            for glowstick_sequence in glowstick_list:
                x_glow, y_glow = glowstick_sequence
                glowstick_sequences.append((y_glow + 1, x_glow + 1))

        for glowstick_position in glowstick_sequences:
            x_glow, y_glow = utils.cell_to_pixels(self.maze, glowstick_position)

            if glowstick_position == self.billy.pos:
                pygame.draw.rect(self.window, (244, 0, 0), (x_glow + 8, y_glow + 8, 14, 14))
            elif glowstick_position == self.bob.pos:
                pygame.draw.rect(self.window, (244, 78, 63), (x_glow + 8, y_glow + 8, 14, 14))
            elif glowstick_position in boxes_list:
                pygame.draw.rect(self.window, (5, 79, 119), (x_glow + 8, y_glow + 8, 14, 14))
            elif glowstick_position == self.get_door_position_maze():
                pygame.draw.rect(self.window, (255, 255, 255), (x_glow + 8, y_glow + 8, 14, 14))

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
