from scripts.load_animations import characters
import pygame
import constans
class Player(pygame.sprite.Sprite):
    '''Clase para manejar al jugador'''
    def __init__(self, row, col, grid, screen, tile_size, ambientation,hp=100):
        super().__init__()
        self.row = row
        self.col = col
        self.grid = grid
        self.screen = screen
        self.tile_size = tile_size
        self.ambientation = ambientation

        # --- Caracteristicas del jugador ---
        self.hp = hp
        self.max_hp = self.hp
        self.existKey = False
        self.existbomb = False
        self.total_bombs = 10
        self.dammage = 50

        # --- Conversion de posiciones de la matriz en pixeles ---
        self.posi_x = self.col * self.tile_size
        self.posi_y = constans.OFFSET_Y + self.row * self.tile_size
        
        # --- Variables para controlar el movimiento celda a celda ---
        self.move_delay = 100
        self.original_move_delay = self.move_delay 
        self.last_move = pygame.time.get_ticks()   

        # --- Variables para la animación ---
        self.animation_time = 350 
        self.last_frame_time = pygame.time.get_ticks()
        self.frame = 0 # Índice
        self.direction = 'bottom' 
        
        # Cargar imágenes del personaje y sus animaciones respectivas
        self.animations = characters['StrongChar'] 
        self.image = self.animations[self.direction][self.frame]
        
        # El rect ahora se basa en la imagen cargada o en tile_size
        self.rect = self.image.get_rect(topleft=(self.posi_x, self.posi_y))

        # Controlar el tiempo de ambientacion
        self.ambientation_time = pygame.time.get_ticks()
        self.ambientation_rate = 500
        self.move_grid = [0, 'V', 'H']

    def _aply_ambientation(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.ambientation_time > self.ambientation_rate:
            if self.ambientation[self.row][self.col] == 'V':
                self.hp -= 5
            elif self.ambientation[self.row][self.col] == 'H':
                self.move_delay = 1000
            else:
                self.move_delay = self.original_move_delay
            self.ambientation_time = current_time
            
    def update(self):
            current_time = pygame.time.get_ticks()
            keys = pygame.key.get_pressed()
            dx, dy = 0, 0

            # Determinar dirección y movimiento
            if keys[pygame.K_w]:  # Arriba
                dy = -1
                self.direction = 'top'
            elif keys[pygame.K_s]:  # Abajo
                dy = 1
                self.direction = 'bottom'
            elif keys[pygame.K_a]:  # Izquierda
                dx = -1
                self.direction = 'left'
            elif keys[pygame.K_d]:  # Derecha
                dx = 1
                self.direction = 'right'

            # Movimiento si ha pasado el tiempo suficiente
            if current_time - self.last_move > self.move_delay and (dx != 0 or dy != 0):
                new_row = self.row + dy
                new_col = self.col + dx
                
                # Verificar límites y colisiones
                grid_width = len(self.grid[0])
                grid_height = len(self.grid)
                
                if 0 <= new_row < grid_height and 0 <= new_col < grid_width and self.grid[new_row][new_col] in self.move_grid:
                    self.grid[self.row][self.col] = 0
                    self.row = new_row
                    self.col = new_col
                    self.grid[self.row][self.col] = 'J'
                    self.posi_x = self.col * self.tile_size
                    self.posi_y = constans.OFFSET_Y + self.row * self.tile_size
                    self.rect.topleft = (self.posi_x, self.posi_y)
                    self.last_move = current_time  

            # Actualizar animación
            if current_time - self.last_frame_time > self.animation_time:
                if any([keys[pygame.K_w], keys[pygame.K_s], keys[pygame.K_a], keys[pygame.K_d]]):
                    self.frame = (self.frame + 1) % len(self.animations[self.direction])
                else:
                    self.frame = 0  # Frame de idle
                self.last_frame_time = current_time

            # Actualizar imagen
            self.image = self.animations[self.direction][self.frame]
            self._aply_ambientation()