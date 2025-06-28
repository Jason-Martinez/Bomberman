import pygame
import constans
import random
from collections import deque
from scripts.load_animations import characters

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
        
    def update_position(self):
        """Actualizar posición visual basada en row/col"""
        self.x = self.col * self.tile_size
        self.y = constans.OFFSET_Y + self.row * self.tile_size
        self.rect.center = (self.x + self.tile_size // 2, self.y + self.tile_size // 2)

class EnemyType1(Enemy):
    '''
    Enemigo de bajo nivel, hereda de la clase Enemy su constructor.\n
    Su comportamiento se basa:\n 
    - Se mueve de manera aleatoria.\n 
    - Es un enemigo pasivo que no hace daño.
    '''
    def __init__(self, row, col, grid):
        super().__init__(row, col, characters['EasyEnemy'], constans.CELL_SIZE)
        self.flip = False
        self.grid = grid
        self.grid[row][col]='E'

        self.hp = 50
        self.hp_max = self.hp
        self.type = 'easy'
        self.points = 100

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
                self.grid[self.row][self.col]=0
                self.row = new_row
                self.col = new_col
                self.grid[self.row][self.col]='E'
                self.update_position()
                self.frame_index = (self.frame_index + 1) % len(self.animations[self.direction])
                self.image = self.animations[self.direction][self.frame_index]
                self.rect.center = (self.x+self.tile_size//2, self.y+self.tile_size//2)
            
            self.last_move = current_time

class EnemyType2(Enemy):
    '''
    Enemigo de nivel intermedio, hereda de la clase Enemy su constructor.\n
    El comportamiento de este enemigo se basa:\n 
    - Seguir al jugador en un rango especifico.\n
    - Si el jugador se encuentra dentro del rango lo persigue, caso contrario sigue su movimiento de manera
    aleatoria.\n
    - Si no esta el jugador el enemigo se mueve de manera aleatoria.\n
    - Si toca al jugador le hace daño (como si lo "aplastara")
    '''
    def __init__(self, row, col, grid, player, animations = None):
        if animations is None:
            animations = characters['MidEnemy']
        super().__init__(row, col, animations, constans.CELL_SIZE)
        self.grid = grid
        self.player = player
        
        self.hp = 100
        self.hp_max = self.hp
        self.type = 'mid'
        self.points = 250

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
        random.shuffle(directions)

        # Asignar dirección para la animación
        

        if current_time - self.last_move > self.movement_time:
            for dx, dy in directions:
                new_row = self.row + dy
                new_col = self.col + dx

                # Validar límites del mapa
                if (0 <= new_row < len(self.grid) and
                    0 <= new_col < len(self.grid[0]) and
                    self.grid[new_row][new_col] == 0):
                    
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

                    self.update_position()
                    self.moved = True
                    self.last_direction = self.direction
                    break
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
    '''
    Enemigo de nivel dificil, hereda el constructor de la clase EnemyType2.\n
    El comportamiento de este enemigo se basa:\n
    - Movimientos aleatorios si el jugador no se encuentra en el rango.\n 
    - Si el jugador se encuentra en el rango va verificar si
    se encuentra en la misma fila o columna, sino el enemigo sigue al jugador.\n 
    - El enemigo verifica que no haya algun obstaculo para disparar. 
    '''
    def __init__(self, row, col, grid, player, bullet_group, all_sprites):
        super().__init__(row, col, grid, player, characters['HardEnemy'])
        self.all_sprites = all_sprites
        self.bullet_group = bullet_group

        self.hp = 150
        self.hp_max = self.hp
        self.type = 'hard'
        self.points = 400

        self.last_shoot = pygame.time.get_ticks()
        self.shoot_rate = 2000

        self.range = 3

        self.movement_time = 1000
        self.animating = False
        self.state = 'moving'
    
    def can_shot(self):
        '''Verifica que no hay obstaculos para que el enemigo pueda shoot'''
        if self.player.row == self.row:
            # Verificar obstáculos en la fila
            start = min(self.col, self.player.col) + 1
            end = max(self.col, self.player.col)
            for col in range(start, end):
                if self.grid[self.row][col] != 0:
                    return False
            return True

        if self.player.col == self.col:
            # Verificar obstáculos en la columna
            start = min(self.row, self.player.row) + 1
            end = max(self.row, self.player.row)
            for row in range(start, end):
                if self.grid[row][self.col] != 0:
                    return False
            return True

        return False

    def get_dir(self):
        '''Obtiene la direccion para la animacion o para la bal'''

        if self.row == self.player.row:
            return 'right' if self.player.col > self.col else 'left'
        if self.col == self.player.col:
            return 'bottom' if self.player.row > self.row else 'top'

    def shoot(self):
        '''Genera el disparo del enemigo'''
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shoot >= self.shoot_rate and self.can_shot():
            direction = self.get_dir()
            self.direction = direction
            bullet = Bullet(self.row, self.col, direction, self.grid, self.tile_size, characters['HardEnemyBullet'])
            self.bullet_group.add(bullet)
            self.all_sprites.add(bullet)
            self.last_shoot = current_time
            self.state = 'shooting'
            self.animating = True
            self.frame_index = 0

    def aline_with_player(self):
        '''Verificar si se necesita mover para alinear una de las coordenadas'''
        current_time = pygame.time.get_ticks()
        moved = False
        if self.row != self.player.row:
            if current_time - self.last_move > self.movement_time:
    
                dy = 1 if self.player.row > self.row else -1
                self.direction = 'bottom' if dy == 1 else 'top'
                new_row = self.row + dy

                #Limites
                if 0 <= new_row < len(self.grid) and self.grid[new_row][self.col] == 0:
                    self.grid[self.row][self.col] = 0
                    self.row = new_row
                    self.grid[self.row][self.col] = 'E'
                    self.y = constans.OFFSET_Y + self.row * self.tile_size
                    self.rect.center = (self.x + self.tile_size // 2, self.y + self.tile_size // 2)
                    moved = True
                self.last_move = current_time

        elif self.col != self.player.col:
            if current_time - self.last_move > self.movement_time:

                dx = 1 if self.player.col > self.col else -1
                self.direction = 'right' if dx == 1 else 'left'
                new_col = self.col + dx

                #Limites
                if 0 <= new_col < len(self.grid[0]) and self.grid[self.row][new_col] == 0:
                    self.grid[self.row][self.col] = 0
                    self.col = new_col
                    self.grid[self.row][self.col] = 'E'
                    self.x = self.col * self.tile_size
                    self.rect.center = (self.x + self.tile_size // 2, self.y + self.tile_size // 2)
                    moved = True
                self.last_move = current_time

        return moved  # Devuelve True si se movió, False si no

    def update_animation(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_frame >= self.frame_rate:
            # Determinar animación por estado
            if self.state == "shooting":
                self.animations = characters['HardEnemyShoot']
                frames = self.animations[self.direction]
            else:
                self.animations = characters['HardEnemy']
                frames = self.animations[self.direction]

            self.frame_index += 1

            if self.frame_index >= len(frames):
                self.frame_index = 0
                if self.state == "shooting":
                    self.state = "moving"  # Volver a estado normal

            self.image = frames[self.frame_index]
            self.last_frame = current_time

    def update(self):
        if self.is_player_in_range():
            if self.can_shot():
                self.shoot()
            else:
                if not self.aline_with_player():
                    self.follow_player()
        else:
            self.random_move()
        self.update_animation()

class Boss(EnemyType3):
    '''
    Jefe final. Hereda de EnemyType3.\n
    Comportamiento especial:\n
    - Vida elevada.\n
    - Crea enemigos cuando anda critico de vida.\n
    - Puede disparar en cruz como ataque especial.\n
    '''
    def __init__(self, row, col, grid, player, bullet_group, all_sprites, enemy_group):
        super().__init__(row, col, grid, player, bullet_group, all_sprites)
        self.hp = 500
        self.hp_max = self.hp
        self.type = 'boss'
        self.points = 1000

        self.fase = 1

        self.range = 15

        self.last_phase_check = pygame.time.get_ticks()
        self.special_cooldown = 4000
        self.last_special = 0

        self.frame_index = 0
        self.state = "moving"
        self.animating = False
        self.direction = 'no_direction'
        self.animations = characters['Boss']
        self.image = self.animations[self.direction][self.frame_index]

        self.min_distance = 5

        self.enemies_rate = 5000
        self.enemy_group = enemy_group
        self.last_enemy = pygame.time.get_ticks()

    def generate_enemies(self, num=2):
        current_time = pygame.time.get_ticks()
        percent = random.random()
        if current_time - self.last_enemy >= self.enemies_rate:
            positions = self.get_available_positions(num)
            for row, col in positions:
                if percent <= 0.5:
                    new_enemy = EnemyType3(row, col, self.grid, self.player, self.bullet_group, self.all_sprites)
                else:
                    new_enemy = EnemyType2(row, col, self.grid, self.player)
                self.enemy_group.add(new_enemy)
                self.all_sprites.add(new_enemy)
                self.grid[row][col] = 'E'
            self.last_enemy = current_time

    def get_available_positions(self, num):
        directions = [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (1,1), (-1,1), (1,-1)]
        random.shuffle(directions)
        valid_positions = []

        for dx, dy in directions:
            new_row = self.row + dy
            new_col = self.col + dx
            if 0 <= new_row < len(self.grid) and 0 <= new_col < len(self.grid[0]):
                if self.grid[new_row][new_col] == 0:
                    valid_positions.append((new_row, new_col))
                    if len(valid_positions) == num:
                        break
        return valid_positions

    def cross_shot(self):
        '''Dispara en 4 direcciones si puede.'''
        current_time = pygame.time.get_ticks()
        if current_time - self.last_special >= self.special_cooldown:
            for dir in ['top', 'bottom', 'left', 'right']:
                bullet = Bullet(self.row, self.col, dir, self.grid, self.tile_size, characters['BossBullet'])
                self.bullet_group.add(bullet)
                self.all_sprites.add(bullet)
            self.frame_index = 0
            self.last_special = current_time

    def get_path_to_player(self):
        start = (self.row, self.col)
        goal = (self.player.row, self.player.col)
        visited = set()
        queue = deque()
        queue.append((start, []))  # (posición actual, camino acumulado)

        while queue:
            (current_row, current_col), path = queue.popleft()
            if (current_row, current_col) == goal:
                return path  # lista de pasos [(r1, c1), (r2, c2), ...]

            if (current_row, current_col) in visited:
                continue
            visited.add((current_row, current_col))

            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Arriba, abajo, izq, der
                new_row = current_row + dr
                new_col = current_col + dc

                if (
                    0 <= new_row < len(self.grid)
                    and 0 <= new_col < len(self.grid[0])
                    and self.grid[new_row][new_col] in [0, 'J']  # celda libre o jugador
                ):
                    new_path = path + [(new_row, new_col)]
                    queue.append(((new_row, new_col), new_path))

        return []  # No hay camino

    def follow_player_bfs(self):
        current_time = pygame.time.get_ticks()

         # Distancia actual al jugador
        distance = abs(self.row - self.player.row) + abs(self.col - self.player.col)

        if distance <= self.min_distance:
            return  # No moverse si está demasiado cerca

        if current_time - self.last_move >= self.movement_time:
            path = self.get_path_to_player()
            if path:
                next_row, next_col = path[0]  # siguiente paso

                dx = next_col - self.col
                dy = next_row - self.row

                if dy == -1:
                    self.direction = 'top'
                elif dy == 1:
                    self.direction = 'bottom'
                elif dx == -1:
                    self.direction = 'left'
                elif dx == 1:
                    self.direction = 'right'

                # Mover
                if self.grid[next_row][next_col] in [0, 'J']:
                    self.grid[self.row][self.col] = 0
                    self.row = next_row
                    self.col = next_col
                    self.grid[self.row][self.col] = 'E'

                    self.x = self.col * self.tile_size
                    self.y = constans.OFFSET_Y + self.row * self.tile_size
                    self.rect.center = (self.x + self.tile_size // 2, self.y + self.tile_size // 2)
                    self.moved = True

            self.last_move = current_time

    def update(self):

        if self.is_player_in_range():
            self.follow_player_bfs()
            if self.can_shot():
                self.cross_shot()
        else:
            self.random_move()
        if self.hp <= 400 and len(self.enemy_group) == 1:
            self.generate_enemies(5)
        self.update_animation()

    def update_animation(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_frame >= self.frame_rate:
            # Determinar animación por estado
            if self.state == "moving":
                self.direction = 'no_direction'
                self.animations = characters['Boss']
                frames = self.animations[self.direction]

            self.frame_index = (self.frame_index + 1) % len(frames)
            self.image = frames[self.frame_index]
            self.last_frame = current_time

class Bullet(pygame.sprite.Sprite):
    '''Genera una bala cuya direccion depende del enemigo'''
    def __init__(self, row, col, direction, grid, tile_size, animations):
        super().__init__()
        self.row = row
        self.col = col
        self.grid = grid
        self.tile_size = tile_size
        self.direction = direction

        # Velocidad y movimiento
        if direction == 'top':
            self.dy, self.dx = -1, 0
        elif direction == 'bottom':
            self.dy, self.dx = 1, 0
        elif direction == 'left':
            self.dy, self.dx = 0, -1
        elif direction == 'right':
            self.dy, self.dx = 0, 1
        self.frame_index = 0
        self.frame_rate = 100
        self.last_frame = pygame.time.get_ticks()
        self.animations = animations
        self.image = self.animations[self.direction][self.frame_index]
        self.rect = self.image.get_rect(center=self.pixel_pos())

    def pixel_pos(self):
        x = self.col * self.tile_size + self.tile_size // 2
        y = constans.OFFSET_Y + self.row * self.tile_size + self.tile_size // 2
        return (x, y)

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_frame > self.frame_rate:
            self.frame_index = (self.frame_index + 1) % len(self.animations[self.direction])
            self.image = self.animations[self.direction][self.frame_index]
            new_row = self.row + self.dy
            new_col = self.col + self.dx

            if not (0 <= new_row < len(self.grid)) or not (0 <= new_col < len(self.grid[0])):
                self.kill()
                return

            if self.grid[new_row][new_col] != 0 and self.grid[new_row][new_col] != 'J':
                self.kill()
                return

            self.row = new_row
            self.col = new_col
            self.rect.center = self.pixel_pos()
            self.last_frame = current_time 