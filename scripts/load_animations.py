from scripts.paths_list import get_path
import pygame
import sys
import os
#Permite el acceso a archivos principales
script_dir = os.path.dirname(__file__)
project_dir = os.path.join(script_dir, '..')
sys.path.append(project_dir)
from constans import PERSON_SCALE, CELL_SIZE, WIDTH, HEIGHT
pygame.init()
pygame.display.set_mode((WIDTH, HEIGHT))

'''
Funcion que carga las imagenes y animaciones de un personaje
'''
def load_character_animations(imgs_paths):
    botton = []
    left = []
    right = []
    top = []

    for img_path in imgs_paths:
        name_img = os.path.basename(img_path)
        if name_img.startswith('B'):
            img = pygame.image.load(img_path).convert_alpha()
            img = pygame.transform.scale(img, (PERSON_SCALE, PERSON_SCALE))
            botton.append(img)
        elif name_img.startswith('L'):
            img = pygame.image.load(img_path).convert_alpha()
            img = pygame.transform.scale(img, (PERSON_SCALE, PERSON_SCALE))
            left.append(img)
        elif name_img.startswith('R'):
            img = pygame.image.load(img_path).convert_alpha()
            img = pygame.transform.scale(img, (PERSON_SCALE, PERSON_SCALE))
            right.append(img)
        elif name_img.startswith('T'):
            img = pygame.image.load(img_path).convert_alpha()
            img = pygame.transform.scale(img, (PERSON_SCALE, PERSON_SCALE))
            top.append(img)
        
        animations = {
            'botton': botton,
            'left': left,
            'right': right,
            'top': top
        }
    return animations

def load_animations(imgs_path, scale = CELL_SIZE):
    animations = []

    for img_path in imgs_path:
        img = pygame.image.load(img_path).convert_alpha()
        img = pygame.transform.scale(img, (scale, scale))
        animations.append(img)
    return animations
#Cargar las animaciones de cada personaje
fast_bomber = load_character_animations(get_path(os.path.join('Assets', 'characters', 'FastChar')))
normal_bomber = load_character_animations(get_path(os.path.join('Assets', 'characters', 'NormalChar')))
strong_bomber = load_character_animations(get_path(os.path.join('Assets', 'characters', 'StrongChar')))

characters = {
    'FastChar': fast_bomber,
    'NormalChar': normal_bomber,
    'StrongChar': strong_bomber
}

all_animations = {
    'bombs': load_animations(get_path(os.path.join('Assets', 'bombs'))),
    'explotions': load_animations(get_path(os.path.join('Assets', 'explotions')), 100)
}
if __name__ == "__main__":
    all_animations
    characters