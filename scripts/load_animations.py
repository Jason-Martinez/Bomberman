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
def load_character_animations(imgs_paths, scale = PERSON_SCALE):
    botton = []
    left = []
    right = []
    top = []
    no_direction = []

    for img_path in imgs_paths:
        name_img = os.path.basename(img_path)
        if name_img.startswith('B'):
            img = pygame.image.load(img_path).convert_alpha()
            img = pygame.transform.scale(img, (scale, scale))
            botton.append(img)
        elif name_img.startswith('L'):
            img = pygame.image.load(img_path).convert_alpha()
            img = pygame.transform.scale(img, (scale, scale))
            left.append(img)
        elif name_img.startswith('R'):
            img = pygame.image.load(img_path).convert_alpha()
            img = pygame.transform.scale(img, (scale, scale))
            right.append(img)
        elif name_img.startswith('T'):
            img = pygame.image.load(img_path).convert_alpha()
            img = pygame.transform.scale(img, (scale, scale))
            top.append(img)
        elif name_img.startswith('m'):
            img = pygame.image.load(img_path).convert_alpha()
            img = pygame.transform.scale(img, (scale, scale))
            no_direction.append(img)
        
        animations = {
            'bottom': botton,
            'left': left,
            'right': right,
            'top': top,
            'no_direction': no_direction
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

#Cargar las animaciones de los enemigos
easy_en = load_character_animations(get_path(os.path.join('Assets', 'enemy_characters', 'nivel1')))
mid_en = load_character_animations(get_path(os.path.join('Assets', 'enemy_characters', 'nivel2')))
hard_en = load_character_animations(get_path(os.path.join('Assets', 'enemy_characters', 'nivel3')))
hard_en_shoot = load_character_animations(get_path(os.path.join('Assets', 'enemy_characters', 'hard_shoot')))
hard_en_bullet = load_character_animations(get_path(os.path.join('Assets', 'enemy_characters', 'hard_bullet_en')))
boss_buller = load_character_animations(get_path(os.path.join('Assets', 'enemy_characters', 'boss_bullet')))
boss = load_character_animations(get_path(os.path.join('Assets', 'enemy_characters', 'boss')))

characters = {
    'FastChar': fast_bomber,
    'NormalChar': normal_bomber,
    'StrongChar': strong_bomber,
    'EasyEnemy': easy_en,
    'MidEnemy': mid_en,
    'HardEnemy': hard_en,
    'HardEnemyShoot':hard_en_shoot,
    'HardEnemyBullet': hard_en_bullet,
    'BossBullet': boss_buller,
    'Boss': boss
}

all_animations = {
    'bombs': load_animations(get_path(os.path.join('Assets', 'bombs'))),
    'explotions': load_animations(get_path(os.path.join('Assets', 'explotions')), 100),
    'portal': load_animations(get_path(os.path.join('Assets', 'portal'))),
}
if __name__ == "__main__":
    all_animations
    characters