import pygame
from scripts.load_animations import characters, all_animations
import constans
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, row, col, grid, screen, tile_size, hp=100):
        super().__init__()
        self.row = row
        self.col = col
        self.grid = grid
        self.screen = screen
        self.tile_size = tile_size

        # --- Caracteristicas del jugador ---
        self.hp = hp
        self.max_hp = self.hp
        self.existKey = False

        # --- Conversion de posiciones de la matriz en pixeles ---
        self.posi_x = self.col * self.tile_size
        self.posi_y = constans.OFFSET_Y + self.row * self.tile_size
        
        # --- Variables para controlar el movimiento celda a celda ---
        self.move_delay = 500 
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
                
                if 0 <= new_row < grid_height and 0 <= new_col < grid_width and self.grid[new_row][new_col] == 0:
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


class Explosion(pygame.sprite.Sprite):
    def __init__(self, row, col, tile_size, explosion_frames):
        super().__init__()
        self.row = row
        self.col = col
        self.tile_size = tile_size
        self.x = self.col * self.tile_size
        self.y = constans.OFFSET_Y + self.row * self.tile_size

        self.explosion_frames = explosion_frames
        self.explosion_frame_delay = 100  # ms por frame
        self.current_explosion_frame_index = 0
        self.last_explosion_frame_time = pygame.time.get_ticks()
        self.visual_explosion_duration_ms = 1000  # Duración total (1 segundo)
        self.start_time = pygame.time.get_ticks()

        self.image = self.explosion_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x + self.tile_size // 2, self.y + self.tile_size // 2)

    def update(self):
        current_time = pygame.time.get_ticks()
        time_since_start = current_time - self.start_time

        if time_since_start <= self.visual_explosion_duration_ms:
            if current_time - self.last_explosion_frame_time > self.explosion_frame_delay:
                self.current_explosion_frame_index = (self.current_explosion_frame_index + 1) % len(self.explosion_frames)
                self.last_explosion_frame_time = current_time
                self.image = self.explosion_frames[self.current_explosion_frame_index]
        else:
            self.kill()

class Bomb(pygame.sprite.Sprite):
    def __init__(self, row, col, grid, screen, tile_size, player_instance_ref, all_sprites, object_group, enemy_group):
        super().__init__()
        self.row = row
        self.col = col
        self.grid = grid
        self.screen = screen
        self.tile_size = tile_size
        self.all_sprites = all_sprites  # Grupo de sprites para agregar explosiones
        self.group = object_group
        self.enemy_group = enemy_group

        self.x, self.y = self.col * self.tile_size, constans.OFFSET_Y + self.row * self.tile_size
        self.rect = pygame.Rect(self.x, self.y, self.tile_size, self.tile_size)

        self.explosion_time_ms = 3000  # Tiempo hasta que la bomba detona (3 segundos)
        self.placed_time = pygame.time.get_ticks()
        
        self.exploded = False
        self.is_visual_explosion_active = False
        
        self.range = 2  # Rango de destrucción

        # Variables para la animación de la bomba
        self.bomb_frames = all_animations['bombs']
        self.bomb_frame_delay_initial = 3000
        self.bomb_frame_delay_final = 150
        self.current_bomb_frame_delay = self.bomb_frame_delay_initial
        
        # Variables de estado de animación
        self.current_frame_index = 0
        self.last_frame_update_time = pygame.time.get_ticks()

        # Referencia al jugador
        self.player_ref = player_instance_ref

        # Establecer la imagen inicial
        self.image = self.bomb_frames[0]

    def update(self):
        current_time = pygame.time.get_ticks()

        if not self.exploded and not self.is_visual_explosion_active:
            time_elapsed = current_time - self.placed_time

            # Calcular velocidad de animación
            if time_elapsed < self.explosion_time_ms:
                progress = time_elapsed / self.explosion_time_ms
                self.current_bomb_frame_delay = self.bomb_frame_delay_initial - \
                                                (self.bomb_frame_delay_initial - self.bomb_frame_delay_final) * progress
                if self.current_bomb_frame_delay < self.bomb_frame_delay_final:
                    self.current_bomb_frame_delay = self.bomb_frame_delay_final
            else:
                self.current_bomb_frame_delay = self.bomb_frame_delay_final

            # Actualizar frame de la bomba
            if current_time - self.last_frame_update_time > self.current_bomb_frame_delay:
                self.current_frame_index = (self.current_frame_index + 1) % len(self.bomb_frames)
                self.last_frame_update_time = current_time
                self.image = self.bomb_frames[self.current_frame_index]

            # Comprobar si es hora de la explosión
            if time_elapsed > self.explosion_time_ms:
                self.explode()
                self.exploded = True
                self.is_visual_explosion_active = True
                

        elif self.exploded and self.is_visual_explosion_active:
            # La bomba se elimina después de iniciar las explosiones
            self.kill()

    def explode(self):
        """
        Destrucción del mapa y creación de explosiones visuales.
        """

        grid_height = len(self.grid)
        grid_width = len(self.grid[0])

        # Crear explosión en la celda central
        explosion = Explosion(self.row, self.col, self.tile_size, all_animations['explotions'])
        self.all_sprites.add(explosion)

        # Afectar celdas en cruz
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        for dx_dir, dy_dir in directions:
            for i in range(1, self.range + 1):
                target_x = self.col + (dx_dir * i)
                target_y = self.row + (dy_dir * i)

                if not (0 <= target_x < grid_width and 0 <= target_y < grid_height):
                    break

                cell_type = self.grid[target_y][target_x]
                
                if cell_type == 1:  # Pared indestructible
                    break
                elif cell_type == 2:  # Pared destructible
                    self._apply_destruction(target_x, target_y, grid_width, grid_height)
                    explosion = Explosion(target_y, target_x, self.tile_size, all_animations['explotions'])
                    self.all_sprites.add(explosion)
                elif cell_type == 0:  # Celda caminable
                    self._apply_destruction(target_x, target_y, grid_width, grid_height)
                    explosion = Explosion(target_y, target_x, self.tile_size, all_animations['explotions'])
                    self.all_sprites.add(explosion)
                elif cell_type == 'J':
                    self.player_ref.hp -= 25
                    explosion = Explosion(target_y, target_x, self.tile_size, all_animations['explotions'])
                    self.all_sprites.add(explosion)
                elif cell_type == 'LS':
                    llave = Key(target_x, target_y, self.tile_size)
                    self.group.add(llave)
                    self.all_sprites.add(llave)
                    self._apply_destruction(target_x, target_y, grid_width, grid_height)
                elif cell_type == 'E':
                    for enemy in self.enemy_group:
                        if enemy.row == target_y and enemy.col == target_x:
                            enemy.kill()
                            self.grid[enemy.row][enemy.col] = 0

                    
    def _apply_destruction(self, x, y, grid_width, grid_height):
        """
        Aplica los efectos de la explosión a una celda específica.
        """
        if not (0 <= x < grid_width and 0 <= y < grid_height):
            return

        if self.grid[y][x] == 2:
            self.grid[y][x] = 0
        if self.grid[y][x] == 'LS':
            self.grid[y][x] = 0

class Key(pygame.sprite.Sprite):
    def __init__(self, col, row, tile_size):
        super().__init__()
        self.x = col * tile_size
        self.y = constans.OFFSET_Y + row * tile_size
        self.image = pygame.image.load(constans.KEY_PATH).convert_alpha()
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.rect =self.image.get_rect()
        self.rect.center = (self.x + tile_size // 2, self.y + tile_size // 2)
    
    def update(self):
        self.image
        
class Portal(pygame.sprite.Sprite):
    def __init__(self, col, row, tile_size):
        super().__init__()
        self.x = col * tile_size
        self.y = constans.OFFSET_Y + row * tile_size

        self.imgs = all_animations['portal']
        self.frame_index = 0
        self.last_frame = pygame.time.get_ticks()
        self.frame_delay = 50

        self.image = self.imgs[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x + tile_size // 2, self.y + tile_size // 2)
    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_frame > self.frame_delay:
            self.frame_index = (self.frame_index + 1) % len(self.imgs)
            self.image = self.imgs[self.frame_index]
            self.last_frame = current_time 

class Enemy(pygame.sprite.Sprite):
    '''
    Esta clase va contener todo los parametros necesarios para la creacion de enemigos
    '''
    def __init__(self, row, col, animations, tile_size):
        super().__init__()
        self.row = row
        self.col = col
        self.tile_size = tile_size

        self.x = col * tile_size
        self.y = constans.OFFSET_Y + row * tile_size

        self.movement_time = 1000
        self.last_move = pygame.time.get_ticks()
        
        self.frame_rate = 100
        self.last_frame = pygame.time.get_ticks()
        self.frame_index = 0
        self.direction = 'bottom'

        self.animations = animations
        self.image = self.animations[self.direction][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x + tile_size // 2, self.y + tile_size // 2)

class EnemyType1(Enemy):
    '''
    Enemigo de bajo nivel, hereda de la clase Enemy su constructor.
    Su comportamiento es moverse de manera aleatoria, ademas de ser un enemigo pasivo
    que no hace daño
    '''
    def __init__(self, row, col, grid):
        super().__init__(row, col, characters['EasyEnemy'], constans.CELL_SIZE)
        self.flip = False
        self.grid = grid
        self.grid[row][col]='E'

    def update(self):
        current_time = pygame.time.get_ticks()
        directions = [(0,-1), (0,1), (-1,0), (1,0)]
        direction = random.choice(directions)
        dx = direction[0]
        dy = direction[1]
        if dy == -1:
            self.direction = 'top'
        elif dy == 1:
            self.direction = 'bottom'
        elif dx == -1:
            self.direction = 'left'
        elif dx == 1:
            self.direction = 'right'
        
        if current_time - self.last_move > self.movement_time:
            new_row = self.row + dy
            new_col = self.col + dx
            if self.grid[new_row][new_col] == 0:
                print('Hubo movimiento')
                self.grid[self.row][self.col]=0
                self.row = new_row
                self.col = new_col
                self.grid[self.row][self.col]='E'
                self.x = self.col * self.tile_size
                self.y = constans.OFFSET_Y + self.row * self.tile_size
                self.frame_index = (self.frame_index + 1) % len(self.animations[self.direction])
                self.image = self.animations[self.direction][self.frame_index]
                self.rect.center = (self.x+self.tile_size//2, self.y+self.tile_size//2)
            
            self.last_move = current_time

class EnemyType2(Enemy):
    '''
    Enemigo de nivel intermedio, hereda de la clase Enemy su constructor.
    El comportamiento de este enemigo se basa en seguir al jugador en un rango especifico,
    si el jugador se encuentra dentro de ese rango lo persigue, caso contrario sigue su movimiento de manera
    aleatoria
    '''
    def __init__(self, row, col, grid, player):
        super().__init__(row, col, characters['MidEnemy'], constans.CELL_SIZE)
        self.grid = grid
        self.player = player

        self.grid[row][col]='E'
        self.movement_time = 1000

        self.frame_rate = 200

        self.moved = False

        self.last_direction = self.direction

        self.range = 2

    def is_player_in_range(self):
        '''
        Verifica si se encuentra el jugador en el area de "vision" del enemigo
        '''
        for i in range(-self.range, self.range + 1):
            for j in range(-self.range, self.range + 1):
                row = self.row + i
                col = self.col + j

                if 0 <= row < len(self.grid) and 0 <= col < len(self.grid[0]):
                    if self.grid[row][col] == 'J':
                        return True
        return False
    
    def random_move(self):
        '''Movimiento aleatorio verificando espacio libres'''
        current_time = pygame.time.get_ticks()
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        dx, dy = random.choice(directions)

        # Asignar dirección para la animación
        if dy == -1:
            self.direction = 'top'
        elif dy == 1:
            self.direction = 'bottom'
        elif dx == -1:
            self.direction = 'left'
        elif dx == 1:
            self.direction = 'right'

        if current_time - self.last_move > self.movement_time:
            new_row = self.row + dy
            new_col = self.col + dx

            # Validar límites del mapa
            if (0 <= new_row < len(self.grid) and
                0 <= new_col < len(self.grid[0]) and
                self.grid[new_row][new_col] == 0):

                self.grid[self.row][self.col] = 0
                self.row = new_row
                self.col = new_col
                self.grid[self.row][self.col] = 'E'

                self.x = self.col * self.tile_size
                self.y = constans.OFFSET_Y + self.row * self.tile_size

                self.rect.center = (self.x + self.tile_size // 2, self.y + self.tile_size // 2)
                self.moved = True
                self.last_direction = self.direction
            self.last_move = current_time

    def follow_player(self):
        '''
        Seguir al jugador evitando los obstaculos a toda costa
        '''
        current_time = pygame.time.get_ticks()
        directions = []

        distance_row = self.player.row - self.row
        distance_col = self.player.col - self.col
        if abs(distance_row) >= abs(distance_col):
            if distance_row < 0:
                directions.append((-1, 0))  # arriba
            if distance_row > 0:
                directions.append((1, 0))   # abajo
            if distance_col < 0:
                directions.append((0, -1))  # izquierda
            if distance_col > 0:
                directions.append((0, 1))   # derecha
        else:
            if distance_col < 0:
                directions.append((0, -1))
            if distance_col > 0:
                directions.append((0, 1))
            if distance_row < 0:
                directions.append((-1, 0))
            if distance_row > 0:
                directions.append((1, 0))
        
        if current_time - self.last_move > self.movement_time:
            for dy, dx in directions:
                new_row = self.row + dy
                new_col = self.col + dx

                if (
                    0 <= new_row < len(self.grid) and
                    0 <= new_col < len(self.grid[0]) and
                    self.grid[new_row][new_col] in [0, 'J']
                ):
                    # Definir dirección solo si se mueve realmente
                    if dy == -1:
                        self.direction = 'top'
                    elif dy == 1:
                        self.direction = 'bottom'
                    elif dx == -1:
                        self.direction = 'left'
                    elif dx == 1:
                        self.direction = 'right'

                    self.grid[self.row][self.col] = 0
                    self.row = new_row
                    self.col = new_col
                    self.grid[self.row][self.col] = 'E'

                    self.x = self.col * self.tile_size
                    self.y = constans.OFFSET_Y + self.row * self.tile_size
                    self.rect.center = (self.x + self.tile_size // 2, self.y + self.tile_size // 2)

                    self.moved = True
                    self.last_direction = self.direction
                    break  # No intentar más direcciones

            self.last_move = current_time
            
    def update(self):
        current_time = pygame.time.get_ticks()

        if self.is_player_in_range():
            self.follow_player()
        if not self.is_player_in_range():
            self.random_move()

        if current_time - self.last_frame > self.frame_rate:
            if self.moved:
                self.frame_index = (self.frame_index + 1) % len(self.animations[self.direction])
                self.image = self.animations[self.direction][self.frame_index]
                self.moved = False
            else:
                self.frame_index = (self.frame_index + 1) % len(self.animations[self.last_direction])
                self.image = self.animations[self.last_direction][self.frame_index]
            self.last_frame = current_time 

class EnemyType3(EnemyType2):
    def __init__(self, row, col, grid, player):
        super().__init__(row, col, grid, player)                  