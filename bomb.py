from scripts.load_animations import all_animations
from elements import Key
import pygame
import constans
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
    def __init__(self, row, col, grid, screen, tile_size, player_instance_ref, all_sprites, object_group, enemy_group, score):
        super().__init__()
        self.row = row
        self.col = col
        self.grid = grid
        self.screen = screen
        self.tile_size = tile_size
        self.all_sprites = all_sprites  # Grupo de sprites para agregar explosiones
        self.group = object_group
        self.enemy_group = enemy_group
        self.score = score

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
        self.player = player_instance_ref

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
            self.player.existbomb = False
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
            for i in range(0, self.range + 1):
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
                    self.player.hp -= 25
                    explosion = Explosion(target_y, target_x, self.tile_size, all_animations['explotions'])
                    self.all_sprites.add(explosion)
                elif cell_type == 'LS':
                    llave = Key(target_x, target_y, self.tile_size)
                    self.group.add(llave)
                    self.all_sprites.add(llave)
                    self._apply_destruction(target_x, target_y, grid_width, grid_height)
                elif cell_type == 'E':
                    for enemy in self.enemy_group:
                        if (enemy.row == target_y and enemy.col == target_x):
                            enemy.hp -= self.player.dammage
                            if enemy.hp <= 0:
                                if enemy.type == 'boss':
                                    llave = Key(target_x, target_y, self.tile_size)
                                    self.group.add(llave)
                                    self.all_sprites.add(llave)
                                self.grid[enemy.row][enemy.col] = 0
                                self.score.add_score(enemy.points)
                                enemy.kill()
                                                         
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
