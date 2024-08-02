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
        self.inventory = {"k": 0, "g": 251, "s": 1, "r": 1}

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
        self.battery_trigger = self.flash.get_used_battery()
        if event.key == self.key_glowstick and self.inventory["g"] > 0:
            self.inventory["g"] -= 1
            print("Usar Glowstick")
            self.flash.glowstick(self.player.position)
            return True

        elif event.key == self.key_radar and self.inventory["r"] > 0:
            self.inventory["r"] -= 1
            print("Usar Radar")
            return True

        elif event.key == self.key_battery and self.battery_trigger:
            self.inventory["s"] += 1
            print("Desusar Bateria")
            self.flash.battery_trigger = False
            self.flash.super_battery_trigger = False

        elif event.key == self.key_battery and not self.battery_trigger and self.inventory["s"] > 0:
            print("Usar Bateria")
            self.flash.set_type_battery()
            self.inventory["s"] -= 1

    def get_inventory(self):
        return self.inventory







