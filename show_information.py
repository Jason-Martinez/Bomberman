import pygame
from constans import COLORS, BAR_HEIGHT, BAR_LEN
def draw_text(surface, text, size, x, y):
    '''Dibuja texto en una posicion otorgada'''
    font = pygame.font.SysFont('serif', size)
    text_surface = font.render(text, True, COLORS['WHITE'])
    text_rect = text_surface.get_rect()
    text_rect.midtop=(x, y)
    surface.blit(text_surface, text_rect)

def status_bar(surface, x, y, status, max_status, color, bar_len=BAR_LEN, bar_height=BAR_HEIGHT):
    '''Crea una barra de estadisticas (Vida, escudos, etc.). Status es el valor actual y 
    max_status es el maximo posible'''
    fill = (status / max_status) * bar_len
    border = pygame.Rect(x, y, bar_len, bar_height)
    fill = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surface, color, fill)
    pygame.draw.rect(surface, COLORS['WHITE'], border, 1)