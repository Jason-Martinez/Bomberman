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
        self.ambientacion = [[0 for _ in range(constans.COLS)] for _ in range(constans.ROWS)]
        self.level = level
        self.img_indestructible = None
        self.img_walK = None

        #Agregando bordes indestructibles
        for row in range(constans.ROWS):
            for col in range(constans.COLS):
                if row == 0 or row == constans.ROWS - 1 or col == 0 or col == constans.COLS - 1:
                    self.matriz[row][col] = 1

        self._generate_map()
    def _generate_map(self):
        percent = 0
        if self.level == 1:
            percent = 0.05
            indestructibles = constans.MAP1_INDESTRUCTIBLE
            veneno = constans.MAP1_AMBIENTE['V']
            hielo = constans.MAP1_AMBIENTE['H']
            portal_pos = constans.PORTAL_POS[0]
            self.img_walK = constans.SCALE_IMS['grass']
            self.img_indestructible = constans.SCALE_IMS['stone']
        elif self.level == 2:
            percent = 0.10
            indestructibles = constans.MAP2_INDESTRUCTIBLE
            veneno = constans.MAP2_AMBIENTE['V']
            hielo = constans.MAP2_AMBIENTE['H']
            portal_pos = constans.PORTAL_POS[1]
            self.img_walK = constans.SCALE_IMS['sand']
            self.img_indestructible = constans.SCALE_IMS['stone']
        elif self.level == 3:
            percent = 0.15
            indestructibles = constans.MAP3_INDESTRUCTIBLE
            veneno = constans.MAP3_AMBIENTE['V']
            hielo = constans.MAP3_AMBIENTE['H']
            portal_pos = constans.PORTAL_POS[2]
            self.img_walK = constans.SCALE_IMS['grass']
            self.img_indestructible = constans.SCALE_IMS['stone']
        elif self.level == 4:
            percent = 0.20
            indestructibles = constans.MAP4_INDESTRUCTIBLE
            veneno = constans.MAP4_AMBIENTE['V']
            hielo = constans.MAP4_AMBIENTE['H']
            portal_pos = constans.PORTAL_POS[3]
            self.img_walK = constans.SCALE_IMS['land']
            self.img_indestructible = constans.SCALE_IMS['volcano_stone']
        
        spawnPlayer = [(1,1), (1,2), (2,1), (2,2), (3,10), (3,3)]
        #Agregando destructibles e indestructibles
        self.genarate_objects(percent, indestructibles, spawnPlayer, veneno, hielo, portal_pos)
        if 1<= self.level < 4:
            self.generateKey()
        self.generate_ambientation(veneno, hielo)

    def genarate_objects(self, percent, indestructibles, spawnPlayer, veneno, hielo, portal_pos):
        for row in range(constans.ROWS):
            for col in range(constans.COLS):
                if (row, col) in indestructibles:
                    self.matriz[row][col] = 1
                elif self.matriz[row][col] == 0: 
                    if (random.random() <= percent and 
                        (row, col) not in spawnPlayer and
                        (row, col) not in veneno and
                        (row, col) not in hielo and
                        (row, col) != portal_pos):
                        self.matriz[row][col] = 2
    
    def generateKey(self):
        '''Permite que la llave aparezca de manera aleatoria en los destructibles'''
        while True:
            row = random.randint(0, constans.ROWS - 1)
            col = random.randint(0, constans.COLS - 1)
            if self.matriz[row][col] == 2:
                self.matriz[row][col] = 'LS' #Llave secreta
                break
    
    def generate_ambientation(self, veneno, hielo):
        '''Copia la matriz original y coloca valores para identificar el tipo de ambientacion'''
        rows = len(self.ambientacion)
        cols = len(self.ambientacion[0])
        for row in range(rows):
            for col in range(cols):
                if (row, col) in veneno:
                    self.ambientacion[row][col] = 'V'
                elif (row, col) in hielo:
                    self.ambientacion[row][col] = 'H'
    
    def draw(self, tile_size):
        walkable = ('J', 0, 'E') 
        destrutibles = (2, 'LS') 
        for row in range(constans.ROWS):
            for col in range(constans.COLS):
                pos_y = constans.OFFSET_Y + row * tile_size
                if self.matriz[row][col] in destrutibles:
                    self.surface.blit(constans.SCALE_IMS['box'], (col * tile_size, pos_y, tile_size, tile_size))
                
                if self.matriz[row][col] in walkable:
                    self.surface.blit(self.img_walK, (col * tile_size, pos_y, tile_size, tile_size))
                    if self.ambientacion[row][col] == 'V':
                        self.surface.blit(constans.SCALE_IMS['poison'], (col * tile_size, pos_y, tile_size, tile_size))
                    elif self.ambientacion[row][col] == 'H':
                        self.surface.blit(constans.SCALE_IMS['ice'], (col * tile_size, pos_y, tile_size, tile_size))
                
                elif self.matriz[row][col] == 1:
                    self.surface.blit(self.img_indestructible, (col * tile_size, pos_y, tile_size, tile_size))