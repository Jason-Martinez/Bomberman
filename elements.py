import pygame
from scripts.load_animations import all_animations
import constans

class Key(pygame.sprite.Sprite):
    '''Llave que te permite abrir el portal'''
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
    '''Crea el portal para avanzar al siguiente nivel'''
    def __init__(self, pos, tile_size):
        super().__init__()
        row, col = pos[0], pos[1]
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

class StageIntro:
    'Clase que muestra en pantalla la introducción del nivel'
    def __init__(self, screen, stage_number, duration=2500):
        self.screen = screen
        self.stage_number = stage_number
        self.duration = duration  # milisegundos
        self.start_time = pygame.time.get_ticks()
        self.active = True

        # Fuente predefinida
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 64, bold=True)
        self.text = f"STAGE {self.stage_number}"
        self.rendered_text = self.font.render(self.text, True, (255, 255, 255))
        self.rect = self.rendered_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

    def update(self):
        if not self.active:
            return False

        elapsed = pygame.time.get_ticks() - self.start_time
        if elapsed >= self.duration:
            self.active = False
            return False

        # Fondo semitransparente
        overlay = pygame.Surface(self.screen.get_size())
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Texto centrado
        self.screen.blit(self.rendered_text, self.rect)
        return True 

class ScoreManager:
    'Clase del puntaje en pantalla'
    def __init__(self):
        self.score = 0
    def add_score(self, points):
        self.score += points