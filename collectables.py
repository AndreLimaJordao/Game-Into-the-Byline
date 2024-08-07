import pygame
import random
import utils

from pygame.locals import *


QTY_BOXES = 20
glowstick_tick = 10
radar_tick = 30
super_battery_tick = 40
pygame.mixer.init()
open_chest = pygame.mixer.Sound("assets/sounds/open_chest.wav")

class Collectables(pygame.sprite.Sprite):
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

    def get_box(self, event, flashs_list, player):
        if event.key == K_SPACE:
            if player.player_position in self.boxes_pos:

                flash_cells = []
                for flash_list in flashs_list:
                    for column, line in flash_list:                        flash_cells.append((line + 1, column + 1))

                if player.player_position in flash_cells:
                    item = self.itens.pop(0)
                    print("ITEM PEGO!")
                    print(f"Item: {item}")
                    open_chest.play()
                    self.boxes_pos.remove(player.player_position)
                    if(item != "#" and player.inventory[item] <= 6):
                        player.add_inventory(item)

    def draw(self, screen, maze, flashs_list):
        flash_cells = []

        for flash_list in flashs_list:
            for column, line in flash_list:
                flash_cells.append((line + 1, column + 1))

        for box_pos in self.boxes_pos:
            if box_pos in flash_cells:
                box = pygame.Surface((14, 14))
                box.fill((153, 76, 0))

                pixel_xy = utils.cell_to_pixels(maze, box_pos)
                cell_rect = pygame.Rect(pixel_xy, (maze.cell_grid_width, maze.cell_grid_width))
                screen.blit(box, (cell_rect.centerx - 7, cell_rect.centery - 7))

