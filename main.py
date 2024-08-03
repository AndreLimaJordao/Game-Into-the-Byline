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

pygame.mixer.init()

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

billy_radar = (-1, -1)
bob_radar = (-1, -1)
got_killed = False
got_killed_billy = False
got_killed_bob = False

trigger = False
battery_trigger = False
door_revealed = False

DEATHSCORE = 1000000

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

        self.maze_map = maze_generator.get_mazemap()
        self.maze = maze_generator.Maze(57.5, 57.5, 600, 600, self.maze_map)

        left_player, right_player, up_player, down_player = K_a, K_d, K_w, K_s
        self.player = Player(self.screen, left_player, right_player, up_player, down_player, num_pixels, side_pixel)

        self.billy = Monster(5, "#F40000", (1, 1), self.screen, self.maze, self.maze_map)
        self.bob = Monster(3, "#F44E3F", (1, 2), self.screen, self.maze, self.maze_map)
        self.billy_scream = pygame.mixer.Sound("assets/sounds/scream_billy.mp3")
        self.bob_scream = pygame.mixer.Sound("assets/sounds/scream_bob.mp3")

        left_flash, right_flash, up_flash, down_flash = K_LEFT, K_RIGHT, K_UP, K_DOWN
        self.flash = Flash(self.screen, left_flash, right_flash, up_flash, down_flash, num_flashs)

        self.boxes = Boxes()
        self.boxes.generate_boxes(self.maze_map)

        self.inventory = Inventory(self.screen, self.maze, self.flash, self.player, self.billy, self.bob)

    def run(self):
        global flashs_list
        global glowsticks_list
        global trigger
        global got_killed
        global got_killed_billy
        global got_killed_bob
        global billy_radar
        global bob_radar
        global battery_trigger
        global door_revealed
        global DEATHSCORE

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
                            self.bob.set_new_steps(7)
                            got_killed = got_killed_bob = self.bob.move(self.player.get_position_maze())
                            self.bob.set_new_steps(3)

                        self.player.control(event, self.maze_map)

                        player_position = self.player.get_position()

                        self.inventory.use_item(event)

                        battery_trigger = self.inventory.get_battery()

                        billy_radar = self.billy.get_radar_position()
                        bob_radar = self.bob.get_radar_position()

                        item_used = self.inventory.get_trigger(event)
                        if item_used:
                            texts = utils.update_qty_items(self.font, self.inventory.get_inventory())

                        #  flashs_list = self.flash.active(event, self.maze_map, self.player.position, flashs_list)
                        #  glowsticks_list = self.flash.get_glowsticks_list()

                        self.flash.active(event, self.maze_map, player_position)

                        #flashs_list, trigger = self.flash.get_flashs_lists()
                        flashs_list = self.flash.get_flashs_lists()
                        glowsticks_list = self.flash.get_glowsticks_list()

                        flash_used = self.flash.get_trigger(event)

                        if flash_used:
                            # flash_used = not flash_used
                            DEATHSCORE -= 100
                            utils.remove_least_monster(monsters_captured)
                            got_killed_billy, got_killed_bob = self.billy.move(self.player.position_maze), self.bob.move(self.player.position_maze)
                            got_killed = got_killed_billy or got_killed_bob
                            if self.billy.position() in flashs_list[-1]:
                                DEATHSCORE -= 50
                                x_B, y_B = self.billy.position()
                                monsters_captured[0] = ([True, (y_B + 1, x_B + 1), num_flashs])
                            if self.bob.position() in flashs_list[-1]:
                                DEATHSCORE -= 50
                                x_b, y_b = self.bob.position()
                                monsters_captured[1] = ([True, (y_b + 1, x_b + 1), num_flashs])
                            if got_killed:
                                self.map_id = "dead_end"

                        door_position = self.inventory.get_door_position()

                        door_revealed = False
                        for i in range(len(flashs_list)):
                            if door_position in flashs_list[i]:
                                door_revealed = True

                        if door_revealed and self.player.get_position() == door_position:
                            self.map_id = "win_end"

                    if self.map_id == "home_screen":
                        if event.key == pygame.K_1:
                            DEATHSCORE = 1000000
                            self.map_id = "background"
                            self.display = utils.load_display(self.map_id, RESOLUTION)
                            self.music = utils.set_music(self.map_id)
                            self.screen.fill((0, 0, 0))
                            pygame.display.update()
                            self.music.play()
                            pygame.time.delay(5000)
                            texts = utils.update_qty_items(self.font, self.inventory.get_inventory())
                            self.player.spawn()
                            self.billy.set_start_position(self.player.get_position_maze())
                            self.bob.set_start_position(self.player.get_position_maze())

                        if event.key == pygame.K_2:
                            self.map_id = "guide"
                        
                        if event.key == pygame.K_3:
                            pygame.quit()
                            exit()
                    
                    if self.map_id == "guide":
                        self.display = utils.load_display(self.map_id, RESOLUTION)
                        if event.key == pygame.K_r:
                            self.map_id = "home_screen"
                            self.display = utils.load_display(self.map_id, RESOLUTION)
                        
                    if self.map_id == "dead_end":
                        self.map_id = "deathscore"
                        DEATHSCORE = 0
                        self.screen.fill((0, 0, 0))
                        pygame.display.update()
                        if got_killed_billy:
                            self.billy_scream.play()
                            pygame.time.delay(5000)
                        elif got_killed_bob:
                            self.bob_scream.play()
                            pygame.time.delay(5000)
                            

                    if self.map_id == "win_end":
                        self.map_id = "deathscore"
                        
                        data_read = open("data/data.txt", "r")
                        if DEATHSCORE > int(data_read.readline()):
                            data_read.close()
                            data_write = open("data/data.txt", "w")
                            data_write.write(str(DEATHSCORE))
                            data_write.close()
                        
                    if self.map_id == "deathscore":
                        self.display = utils.load_display(self.map_id, RESOLUTION)
                        self.screen.blit(self.display, (0, 0))
                        font_deathscore = pygame.font.Font("assets/fonts/Pixelation.ttf", 75)
                        
                        text_deathscore = font_deathscore.render(f"{DEATHSCORE}", False, (255, 255, 255))
                        text_rect_deathscore = text_deathscore.get_rect(center = (RESOLUTION[0]/2, RESOLUTION[1]/3.7))
                        self.screen.blit(text_deathscore, text_rect_deathscore)
                        
                        data_read = open("data/data.txt", "r")
                        HIGHSCORE = data_read.readline()
                        data_read.close()

                        text_high_deathscore = font_deathscore.render(f"{HIGHSCORE}", False, (255, 255, 255))
                        text_high_rect_deathscore = text_high_deathscore.get_rect(center = (RESOLUTION[0]/2, RESOLUTION[1]/1.5))
                        self.screen.blit(text_high_deathscore, text_high_rect_deathscore)

                        pygame.display.update()

                        if event.key == pygame.K_r:
                            pygame.quit()

                    cells = []

                    for flash_list in flashs_list:
                        for column, line in flash_list:
                            cells.append((line + 1, column + 1))

                    if len(glowsticks_list) > 0:
                        for glowstick_position in glowsticks_list:
                            for column, line in glowstick_position:
                                cells.append((line + 1, column + 1))

                    cells.append(self.player.position_maze)

            if self.map_id in ["home_screen", "guide"]:
                self.screen.blit(self.display, (0, 0))
                pygame.display.update()
            elif self.map_id == "background":
                self.screen.blit(self.display, (0, 0))
                utils.draw_qty_items(self.screen, texts)
                self.boxes.draw(self.screen, self.maze, flashs_list, glowsticks_list)
                if door_revealed:
                    x, y = door_position
                    utils.draw(self.maze, self.screen, "#FFBD59", (14, 14), (y + 1, x + 1))
                utils.get_monster_draw(self.maze, self.screen, monsters_captured)
                utils.active_radar(self.screen, self.maze, (billy_radar, bob_radar))
                utils.show_battery(self.screen, battery_trigger)
                self.player.draw(maze_position)
                self.inventory.try_generate_door()
                self.maze.display_maze_cells(self.screen, cells)

                pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
