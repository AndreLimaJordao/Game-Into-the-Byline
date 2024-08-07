import pygame
from pygame import mixer
from pygame.locals import *
import random

mixer.init()
openC = mixer.Sound("assets/sounds/open_chest.wav")

class Item:
    def __init__(self, x, y, win, width, height, color, space, width_maze, num_pixels):
        self.pos_x = x
        self.pos_y = y
        self.window = win
        self.width = width
        self.height = height
        self.color = color
        self.space = space
        self.speed = width_maze / num_pixels
        self.items_coordinates = []
        self.cal = []
        self.key = []
        self.glowstick = []
        self.radar = []
        self.super_battery = []
        self.qty_key = 0
        self.qty_glowstick = 4
        self.qty_radar = 3
        self.qty_super_battery = 2


    def generator(self, num_pixels):
        #key = []
        #glowstick = []
        #radar = []
        #super_battery = []
        #items_coordinates = []
        #cal = []
        j = 0
        for i in range(5):
        '''
            while len(self.itens_2_distribute) > 0:
                index = random.randint(0, len(self.itens))
                item = self.itens_2_distribute.pop(0)
                self.itens.insert(index, item)

            for i in range(len(self.itens)):
                get_coord = True
                while get_coord:
                    coord = (random.randint(40, 600), random.randint(40, 400))
                    if not coord in self.coord_list:
                        self.coord_list.append(coord)
                        get_coord = False'''
            
            
            pos_x = random.randint(0, num_pixels - 1)
            pos_y = random.randint(0, num_pixels - 1)
            self.key.append((pos_x, pos_y))
            self.items_coordinates.append((pos_x, pos_y))
            self.cal.append((pos_x, pos_y))


            j +=1
            pos_x = random.randint(0, num_pixels - 1)
            pos_y = random.randint(0, num_pixels - 1)
            self.glowstick.append((self.pos_x, self.pos_y))
            self.items_coordinates.append((pos_x, pos_y))
            self.cal.append((pos_x, pos_y))

            j +=1
            pos_x = random.randint(0, num_pixels - 1)
            pos_y = random.randint(0, num_pixels - 1)
            self.radar.append((pos_x, pos_y))
            self.items_coordinates.append((pos_x, pos_y))
            self.cal.append((pos_x, pos_y))

            j += 1
            pos_x = random.randint(0, num_pixels - 1)
            pos_y = random.randint(0, num_pixels - 1)
            self.super_battery.append((self.pos_x, self.pos_y))
            self.items_coordinates.append((pos_x, pos_y))
            self.cal.append((pos_x, pos_y))

            j += 1

            #self.items_coordinates = items_coordinates
            #self.cal = cal

    def draw(self, x_maze, y_maze):
        for j in range(20):
            coord = self.items_coordinates[j]
            self.pos_x = coord[0]
            self.pos_y = coord[1]

            pos_x = self.pos_x * self.speed + x_maze + (self.speed - self.width) / 2
            pos_y = self.pos_y * self.speed + y_maze + (self.speed - self.height) / 2
            if self.cal[j] != 'opened':


                pygame.draw.rect(self.window, self.color, (pos_x, pos_y, self.width, self.height) , )
            else:
                pygame.draw.rect(self.window, (0, 0, 0),(pos_x, pos_y, self.width, self.height), )

            #pygame.draw.rect(self.window, self.color, (pos_x, pos_y, self.width, self.height))
            pygame.display.update((self.pos_x * self.speed + x_maze, self.pos_y * self.speed + y_maze, self.speed, self.speed))



    def interact(self, event, xyplayer, x_maze, y_maze):
        if event.type == KEYDOWN:
            if event.key == self.space:
                for k in range(20):
                    if xyplayer == self.items_coordinates[k] and self.cal[k] != 'opened':
                        if self.items_coordinates[k] in self.key:
                            #qty_key += 1
                            openC.play()


                        elif self.items_coordinates[k] in self.glowstick:
                            #qty_glowstick += 1
                            openC.play()


                        elif self.items_coordinates[k] in self.radar:
                            #qty_radar += 1
                            openC.play()


                        elif self.items_coordinates[k] in self.super_battery:
                            #qty_super_battery += 1
                            openC.play()
                        openC.play()
                        self.cal[k] = 'opened'
