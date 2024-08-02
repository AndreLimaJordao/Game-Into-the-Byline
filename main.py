import pygame
import utils
import maze_generator

from pygame.locals import *
from sys import exit
from player import Player
from flash import Flash
from boxes import Boxes
from inventory import Inventory
from monster import Monster


RESOLUTION = (1280, 720)
FPS = 60

maze_position = (57.5, 57.5)
side_maze = 600
num_pixels = 20
side_pixel = side_maze / num_pixels

flashs_list = [[]]
monsters_captured = [[False], [False]]
glowsticks_list = [[]]
num_flashs = 7
got_killed = False

trigger = False


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(RESOLUTION)
        pygame.display.set_caption("Into the Byline")

        self.clock = pygame.time.Clock()

        self.icon = pygame.image.load('assets/icon/icon.png')
        pygame.display.set_icon(self.icon)

        self.map_id = "home_screen"
        self.display = utils.load_display(self.map_id, RESOLUTION)

        self.music = "None :)"
        self.font = pygame.font.Font("assets/fonts/Pixelation.ttf", 25)

        left_player, right_player, up_player, down_player = K_a, K_d, K_w, K_s
        self.player = Player(self.screen, left_player, right_player, up_player, down_player, num_pixels, side_pixel)

        left_flash, right_flash, up_flash, down_flash = K_LEFT, K_RIGHT, K_UP, K_DOWN
        self.flash = Flash(self.screen, left_flash, right_flash, up_flash, down_flash, num_flashs)

        self.maze_map = maze_generator.get_mazemap()
        self.maze = maze_generator.Maze(57.5, 57.5, 600, 600, self.maze_map)

        self.boxes = Boxes()
        self.boxes.generate_boxes(self.maze_map)

        self.inventory = Inventory(self.boxes, self.player, self.flash, self.maze_map)

        self.billy = Monster(5, "#F40000", (1, 1), self.screen, self.maze, self.maze_map)
        self.bob = Monster(3, "#F44E3F", (1, 2), self.screen, self.maze, self.maze_map)

    def run(self):
        global flashs_list
        global glowsticks_list
        global trigger
        global got_killed

        while True:
            self.clock.tick(60)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()

                    if self.map_id == "background":
                        box_collected = self.boxes.get_box(event, flashs_list, self.player, self.inventory)
                        if box_collected:
                            texts = utils.update_qty_items(self.font, self.inventory.get_inventory())

                        self.player.control(event, self.maze_map)

                        self.inventory.use_item(event)

                        item_used = self.inventory.get_trigger(event)
                        if item_used:
                            texts = utils.update_qty_items(self.font, self.inventory.get_inventory())

                        #  flashs_list = self.flash.active(event, self.maze_map, self.player.position, flashs_list)
                        #  glowsticks_list = self.flash.get_glowsticks_list()

                        self.flash.active(event, self.maze_map, self.player.position)

                        #flashs_list, trigger = self.flash.get_flashs_lists()
                        flashs_list = self.flash.get_flashs_lists()
                        glowsticks_list = self.flash.get_glowsticks_list()

                        flash_used = self.flash.get_trigger(event)

                        if flash_used:
                            # flash_used = not flash_used
                            utils.remove_least_monster(monsters_captured)
                            got_killed = self.billy.move(self.player.position_maze) or self.bob.move(self.player.position_maze)
                            if self.billy.position() in flashs_list[-1]:
                                x_B, y_B = self.billy.position()
                                monsters_captured[0] = ([True, (y_B + 1, x_B + 1), num_flashs])
                            if self.bob.position() in flashs_list[-1]:
                                x_b, y_b = self.bob.position()
                                monsters_captured[1] = ([True, (y_b + 1, x_b + 1), num_flashs])


                        #print(self.billy.position())
                        #print(monsters_captured[0])
                        #print(self.player.position_maze)

                        #print(f"got_killed: {got_killed}")
                        #print(flashs_list)

                    if self.map_id == "home_screen":
                        if event.key == pygame.K_1:
                            self.map_id = "background"
                            self.display = utils.load_display(self.map_id, RESOLUTION)
                            self.music = utils.set_music(self.map_id)
                            self.screen.fill((0, 0, 0))
                            pygame.display.update()
                            self.music.play()
                            pygame.time.delay(1000)
                            texts = utils.update_qty_items(self.font, self.inventory.get_inventory())
                            self.player.spawn()
                        if event.key == pygame.K_2:
                            self.map_id = "config"
                            self.display = utils.load_display(self.map_id, RESOLUTION)
                            self.music = utils.set_music(self.map_id)
                        if event.key == pygame.K_3:
                            pygame.quit()
                            exit()

                    cells = []

                    for flash_list in flashs_list:
                        for column, line in flash_list:
                            cells.append((line + 1, column + 1))

                    if len(glowsticks_list) > 0:
                        for glowstick_position in glowsticks_list:
                            for column, line in glowstick_position:
                                cells.append((line + 1, column + 1))

                    cells.append(self.player.position_maze)

            if self.map_id in ["home_screen", "config"]:
                self.screen.blit(self.display, (0, 0))
                pygame.display.update()
            else:
                self.screen.blit(self.display, (0, 0))
                utils.draw_qty_items(self.screen, texts)
                self.boxes.draw(self.screen, self.maze, flashs_list, glowsticks_list)
                utils.get_monster_draw(self.maze, self.screen, monsters_captured)
                self.player.draw(maze_position)
                self.maze.display_maze_cells(self.screen, cells)

                pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
