import pygame
import moviepy.editor
import utils
import maze_generator

from pygame.locals import *
from sys import exit
from player import Player
from flash import Flash
from boxes import Boxes
from inventory import Inventory
from monster import Monster
from score import Score

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
is_scared = False

trigger = False
battery_trigger = False

door_position = (-1, -1)
door_revealed = False

item_description = {"g": "Glowstick", "r": "Radar", "s": "Super Battery", "k": "Key", "#": "Nothing"}
item = "nada"
texts = ""
box_collected = False


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
        
        self.is_scared_photo = pygame.image.load('assets/images/scared.png')
        self.is_not_scared_photo = pygame.image.load('assets/images/not_scared.png')
         
        self.score = Score(1000000)

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

        self.inventory = Inventory(self.screen, self.maze, self.flash, self.player, self.billy, self.bob, self.score)

        self.font_item = pygame.font.Font("assets/fonts/Pixelation.ttf", 23)
        self.rect_item = pygame.Rect(897, 460, 260, 85)

    def run(self):
        global flashs_list
        global glowsticks_list
        global trigger
        global got_killed
        global got_killed_billy
        global got_killed_bob
        global is_scared
        global billy_radar
        global bob_radar
        global battery_trigger
        global door_revealed
        global door_position
        global box_collected
        global item
        global texts

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

                    if self.map_id == "background" and self.player.num_steps == 0:
                        mousex, mousey = pygame.mouse.get_pos()
                        print((mousex, mousey))

                        box_collected, item = self.boxes.get_box(event, flashs_list, glowsticks_list, self.player, self.inventory)
                        if box_collected or item == "#":
                            texts = utils.update_qty_items(self.font, self.inventory.get_inventory())
                            self.bob.set_new_steps(7)
                            got_killed = got_killed_bob = self.bob.move(self.player.get_position_maze())
                            self.bob.set_new_steps(3)

                        self.player.control(event, self.maze)

                        player_position = self.player.get_position()

                        self.inventory.use_item(event)

                        battery_trigger = self.inventory.get_battery()

                        billy_radar = self.billy.get_radar_position()
                        bob_radar = self.bob.get_radar_position()

                        used_item = self.inventory.get_trigger(event)
                        if used_item:
                            texts = utils.update_qty_items(self.font, self.inventory.get_inventory())

                        self.flash.active(event, self.maze_map, player_position)

                        flashs_list = self.flash.get_flashs_lists()
                        glowsticks_list = self.flash.get_glowsticks_list()

                        used_flash = self.flash.get_trigger(event)

                        if used_flash:
                            self.score.set_highscore(100)
                            utils.remove_least_monster(monsters_captured)
                            got_killed_billy = self.billy.move(self.player.position_maze)
                            got_killed_bob = self.bob.move(self.player.position_maze)
                            got_killed = got_killed_billy or got_killed_bob
                            if self.billy.position() in flashs_list[-1]:
                                self.score.set_highscore(50)
                                x_B, y_B = self.billy.position()
                                monsters_captured[0] = ([True, (y_B + 1, x_B + 1), num_flashs - 1])
                            if self.bob.position() in flashs_list[-1]:
                                self.score.set_highscore(50)
                                x_b, y_b = self.bob.position()
                                monsters_captured[1] = ([True, (y_b + 1, x_b + 1), num_flashs - 1])
                            if got_killed:
                                self.map_id = "dead_end"

                        is_scared = False
                        for i in range(2):
                            if monsters_captured[i][0]:
                                is_scared = True

                        door_position = self.inventory.get_door_position()

                        door_revealed = False
                        for i in range(len(flashs_list)):
                            if door_position in flashs_list[i]:
                                door_revealed = True

                        if door_revealed and self.player.get_position() == door_position:
                            self.map_id = "win_end"

                    if self.map_id == "home_screen":
                        if event.key == pygame.K_1:
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
                        self.score.reset_highscore()
                        self.screen.fill((0, 0, 0))
                        pygame.display.update()
                        if got_killed_billy:
                            self.billy_scream.play()
                            pygame.time.delay(5000)
                        elif got_killed_bob:
                            self.bob_scream.play()
                            pygame.time.delay(5000)

                    if self.map_id == "win_end":
                        win_end_sound = pygame.mixer.Sound("assets/sounds/win_end_sound.mp3")
                        win_end_sound.play()
                        win_cutscene = moviepy.editor.VideoFileClip("assets/cutscenes/win_end.mp4")
                        win_cutscene.preview()
                        self.map_id = "deathscore"
                        
                        data_read = open("data/data.txt", "r")
                        if self.score.get_highscore() > int(data_read.readline()):
                            data_read.close()
                            data_write = open("data/data.txt", "w")
                            data_write.write(str(self.score.get_highscore()))
                            data_write.close()
                        
                    if self.map_id == "deathscore":
                        self.display = utils.load_display(self.map_id, RESOLUTION)
                        self.screen.blit(self.display, (0, 0))
                        font_deathscore = pygame.font.Font("assets/fonts/Pixelation.ttf", 75)
                        
                        text_deathscore = font_deathscore.render(f"{self.score.get_highscore()}", False, (255, 255, 255))
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

            if self.map_id in ["home_screen", "guide"]:
                self.screen.blit(self.display, (0, 0))
                pygame.display.update()
            elif self.map_id == "background":

                if self.player.num_steps == 0:
                    self.screen.blit(self.display, (0, -0.7))

                    self.inventory.draw_glowstick(self.boxes.get_boxes_pos())

                    if is_scared:
                        self.screen.blit(self.is_scared_photo, (895, 56))
                    else:
                        self.screen.blit(self.is_not_scared_photo, (895, 56))

                    if box_collected or item == "#":
                        utils.draw_item_found(self.screen, self.font_item, item_description[item], self.rect_item)
                    else:
                        utils.draw_no_item(self.screen, self.font_item, self.rect_item)

                    utils.draw_qty_items(self.screen, texts)
                    self.boxes.draw(self.screen, self.maze, flashs_list)

                    if door_revealed:
                        x, y = door_position
                        utils.draw(self.maze, self.screen, "#FFBD59", (14, 14), (y + 1, x + 1))

                    utils.get_monster_draw(self.maze, self.screen, monsters_captured)
                    utils.active_radar(self.screen, self.maze, (billy_radar, bob_radar))
                    utils.show_battery(self.screen, battery_trigger)

                    self.inventory.try_generate_door()

                    #self.player.draw(maze_position)
                    # self.maze.display_maze_cells(self.screen, (255, 255, 255), [[self.player.get_position()]], flashs_list)

                    self.player.draw(maze_position)
                    self.maze.display_maze_cells(self.screen, (255, 255, 255), [[self.player.get_position()]])

                    self.maze.display_maze_cells(self.screen, (255, 255, 255), flashs_list)

                    self.maze.display_maze_cells(self.screen, (222, 252, 8), glowsticks_list)

                    pygame.display.update()

                else:
                    self.player.move(self.maze, flashs_list, glowsticks_list, self.boxes.get_boxes_pos())


if __name__ == "__main__":
    game = Game()
    game.run()
