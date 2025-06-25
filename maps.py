import constans
import random


#Constantes



class Maps:
    '''
    Genera una matriz de 20x25 la cual va contener los tiles de la imagen de fondo
    los elementos de la matriz corresponden: 
    0 --> suelo,
    1 --> Assets indestructibles,
    2 --> Assets destructibles,
    '''
    def __init__(self, surface, level=1):
        self.surface = surface
        self.matriz = [[0 for _ in range(constans.COLS)] for _ in range(constans.ROWS)]
        self.level = level

        #Agregando bordes indestructibles
        for row in range(constans.ROWS):
            for col in range(constans.COLS):
                if row == 0 or row == constans.ROWS - 1 or col == 0 or col == constans.COLS - 1:
                    self.matriz[row][col] = 1

        self._generate_map()
    def _generate_map(self):
        percent = 0
        if self.level == 1:
            percent = 0.40
            indestructibles = constans.MAP1_INDESTRUCTIBLE
        elif self.level == 2:
            percent = 0.35
            indestructibles = constans.MAP2_INDESTRUCTIBLE
        elif self.level == 3:
            percent = 0.30
            indestructibles = constans.MAP3_INDESTRUCTIBLE
        elif self.level == 4:
            percent = 0.35
            indestructibles = constans.MAP4_INDESTRUCTIBLE
        
        spawnPlayer = [(1,1), (1,2), (2,1), (2,2)]
        #Agregando destructibles e indestructibles
        for row in range(constans.ROWS):
            for col in range(constans.COLS):
                if (row, col) in indestructibles:
                    self.matriz[row][col] = 1
                elif self.matriz[row][col] == 0: 
                    if random.random() <= percent and (row, col) not in spawnPlayer:
                        self.matriz[row][col] = 2


    def draw(self, tile_size):  
        for row in range(constans.ROWS):
            for col in range(constans.COLS):
                pos_y = constans.OFFSET_Y + row * tile_size
                if self.matriz[row][col] == 2:
                    self.surface.blit(constans.SCALE_IMS['box'], (col * tile_size, pos_y, tile_size, tile_size))
                if self.matriz[row][col] == 0 or self.matriz[row][col] == 'J':
                    self.surface.blit(constans.SCALE_IMS['grass'], (col * tile_size, pos_y, tile_size, tile_size))
                elif self.matriz[row][col] == 1:
                    self.surface.blit(constans.SCALE_IMS['stone'], (col * tile_size, pos_y, tile_size, tile_size))