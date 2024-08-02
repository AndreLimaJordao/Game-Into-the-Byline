import pygame
import utils
from pygame import mixer
from pygame.locals import *
import random

from flash import Flash


class Inventory(pygame.sprite.Sprite):
    def __init__(self, boxes, player, flash, maze_map):
        super().__init__()

        # key, glowstick, super battery, radar
        self.inventory = {"k": 0, "g": 3, "s": 3, "r": 3}

        self.key_glowstick = K_1
        self.key_radar = K_2
        self.key_battery = K_3
        self.battery_trigger = False

        self.boxes = boxes
        self.player = player
        self.flash = flash

        self.maze_map = maze_map

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

        elif event.key == self.key_battery and self.inventory["s"] > 0:
            self.battery_trigger = not self.battery_trigger
            if self.battery_trigger:
                self.flash.set_type_battery()
            else:
                self.flash.reset_type_battery()

        elif flash_trigger and self.battery_trigger:
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


