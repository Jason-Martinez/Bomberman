from scripts.paths_list import get_path
from constans import MAP1_INDESTRUCTIBLE, MAP2_INDESTRUCTIBLE, MAP3_INDESTRUCTIBLE, MAP4_INDESTRUCTIBLE
import random
import pygame
import os

#Constantes
ROWS = 20
COLS = 25
SCALE = 32
BGS = get_path(os.path.join('Assets', 'tiles'))
IMGS = {
    'box': pygame.image.load(BGS[0]),
    'grass': pygame.image.load(BGS[1]),
    'stone': pygame.image.load(BGS[2])
}
SCALE_IMS = {
    'box': pygame.transform.scale(IMGS['box'], (SCALE, SCALE)),
    'grass': pygame.transform.scale(IMGS['grass'], (SCALE, SCALE)),
    'stone': pygame.transform.scale(IMGS['stone'], (SCALE, SCALE))
}

'''
Genera una matriz de 20x25 la cual va contener los tiles de la imagen de fondo
los elementos de la matriz corresponden: 
0 --> suelo
1 --> Assets indestructibles
2 --> Assets destructibles
'''
class Maps:
    def __init__(self, surface, level=1):
        self.surface = surface
        self.matriz = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.level = level

        #Agregando bordes indestructibles
        for row in range(ROWS):
            for col in range(COLS):
                if row == 0 or row == ROWS - 1 or col == 0 or col == COLS - 1:
                    self.matriz[row][col] = 1

        self._generate_map()
    def _generate_map(self):
        percent = 0
        if self.level == 1:
            percent = 0.70
            indestructibles = MAP1_INDESTRUCTIBLE
        elif self.level == 2:
            percent = 0.60
            indestructibles = MAP2_INDESTRUCTIBLE
        elif self.level == 3:
            percent = 0.50
            indestructibles = MAP3_INDESTRUCTIBLE
        elif self.level == 4:
            percent = 0.40
            indestructibles = MAP4_INDESTRUCTIBLE
        #Agregando destructibles e indestructibles

        for row in range(ROWS):
            for col in range(COLS):
                if (row, col) in indestructibles:
                    self.matriz[row][col] = 1
                elif self.matriz[row][col] == 0: 
                    if random.random() <= percent:
                        self.matriz[row][col] = 2


    def draw(self, tile_size):  
        for row in range(ROWS):
            for col in range(COLS):
                if self.matriz[row][col] == 2:
                    self.surface.blit(SCALE_IMS['box'], (col * tile_size, row * tile_size, tile_size, tile_size))
                if self.matriz[row][col] == 0:
                    self.surface.blit(SCALE_IMS['grass'], (col * tile_size, row * tile_size, tile_size, tile_size))
                elif self.matriz[row][col] == 1:
                    self.surface.blit(SCALE_IMS['stone'], (col * tile_size, row * tile_size, tile_size, tile_size))
                

