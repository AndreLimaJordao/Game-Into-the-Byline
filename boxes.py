import pygame
import random
import utils

from pygame.locals import *
from player import Player
from inventory import Inventory


QTY_BOXES = 20
glowstick_tick = 10
radar_tick = 30
super_battery_tick = 40
pygame.mixer.init()
open_chest = pygame.mixer.Sound("assets/sounds/open_chest.wav")


class Boxes(pygame.sprite.Sprite):
    def __init__(self, qty_boxes=QTY_BOXES):
        super().__init__()
        self.boxes_pos = []
        self.itens = ["k", "k", "k", "k", "k"]
        self.qty_boxes = qty_boxes

    def generate_boxes(self, maze_map) -> None:
        all_positions = [cell for cell in maze_map.keys()]
        positions = []
        for _ in range(self.qty_boxes):
            cell = random.choice(all_positions)
            positions.append(cell)
            all_positions.remove(cell)
        for i in range(6, QTY_BOXES):
            tick = random.randint(1, 100)
            index = random.randint(0, len(self.itens))
            if tick <= glowstick_tick:
                self.itens.insert(index, "g")
            elif tick <= radar_tick:
                self.itens.insert(index, "r")
            elif tick <= super_battery_tick:
                self.itens.insert(index, "s")
            else:
                self.itens.insert(index, "#")
        self.boxes_pos = positions

    def reset_boxes(self):
        self.boxes_pos = []

    def get_box(self, event, flashs_list, player: Player, inventory: Inventory):
        if event.key == K_SPACE:
            if player.position_maze in self.boxes_pos:

                flash_cells = []
                for flash_list in flashs_list:
                    for column, line in flash_list:
                        flash_cells.append((line + 1, column + 1))

                if player.position_maze in flash_cells:
                    item = self.itens.pop(0)

                    print("ITEM PEGO!")
                    print(f"Item: {item}")

                    open_chest.play()
                    self.boxes_pos.remove(player.position_maze)

                    if item != "#" and player.inventory[item] <= 6:
                        inventory.add_item(item)
                        return True

    def draw(self, screen, maze, flashs_list, glowsticks_list):
        flash_cells = []

        for flash_list in flashs_list:
            for column, line in flash_list:
                flash_cells.append((line + 1, column + 1))

        # for glowstick_list in glowsticks_list:
        #     for column, line in glowstick_list
        #         f

        for box_pos in self.boxes_pos:
            if box_pos in flash_cells:
                box = pygame.Surface((14, 14))
                box.fill((5, 79, 119))

                pixel_xy = utils.cell_to_pixels(maze, box_pos)
                cell_rect = pygame.Rect(pixel_xy, (maze.cell_grid_width, maze.cell_grid_width))
                screen.blit(box, (cell_rect.centerx - 7, cell_rect.centery - 7))

