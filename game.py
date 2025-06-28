import pygame
from maps import Maps
from player import Player
from enemy import EnemyType1, EnemyType2, EnemyType3, Boss
from bomb import Bomb
from elements import ScoreManager, Portal, StageIntro
from colisions import CollisionHandler
from show_information import draw_text, status_bar
from finalScreen import show_end_screen
from user_manager import Users_data
import constans

class Game:
    '''Clase principal del juego'''
    def __init__(self, screen, skin):
        self.screen = screen
        self.skin = skin
        self.clock = pygame.time.get_ticks()
        self.running = True
        self.level = 1
        self.max_levels = 4
        self.game_over = False
        self.victory = False
        self.time = 0
        self.scoreManager = ScoreManager()

        # Grupos de sprites
        self.all_sprites = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.key_group = pygame.sprite.Group()
        self.portal_group = pygame.sprite.Group()

        # Inicializar el primer nivel
        self.initialize_level()

    def initialize_level(self):
        """Inicializa un nivel específico"""
        self.map = Maps(self.screen, self.level)
        self.ambientation = self.map.ambientacion
        self.grid = self.map.matriz

        # Limpiar grupos de sprites
        self.all_sprites.empty()
        self.player_group.empty()
        self.enemy_group.empty()
        self.bullet_group.empty()
        self.key_group.empty()
        self.portal_group.empty()

        # Crear jugador
        self.player = Player(1, 1, self.grid, self.screen, constans.CELL_SIZE, self.ambientation, self.skin)
        self.player_group.add(self.player)
        self.all_sprites.add(self.player)

        # Crear portal
        portal_pos = constans.PORTAL_POS[self.level - 1]
        portal = Portal(portal_pos, constans.CELL_SIZE)
        self.portal_group.add(portal)
        self.all_sprites.add(portal)

        # Crear enemigos según el nivel
        self.spawn_enemies()

        # Crear manejador de colisiones
        self.collision_handler = CollisionHandler(
            self.player, self.screen, self.key_group, self.portal_group,
            self.enemy_group, self.bullet_group, self.player_group, self.map
        )

        # Introducción del nivel
        self.stage_intro = StageIntro(self.screen, self.level)

    def spawn_enemies(self):
        """Genera enemigos según el nivel"""
        if self.level == 1:
            self.player.total_bombs = 15
            enemies = [
                EnemyType1(3, 3, self.grid),
                EnemyType1(5, 5, self.grid),
                EnemyType1(7, 7, self.grid)
            ]
        elif self.level == 2:
            self.player.total_bombs = 20
            enemies = [
                EnemyType2(3, 3, self.grid, self.player),
                EnemyType2(5, 5, self.grid, self.player),
                EnemyType1(7, 7, self.grid)
            ]
        elif self.level == 3:
            self.player.total_bombs = 25
            enemies = [
                EnemyType3(3, 3, self.grid, self.player, self.bullet_group, self.all_sprites),
                EnemyType2(5, 5, self.grid, self.player),
                EnemyType1(7, 7, self.grid)
            ]
        elif self.level == 4:
            self.player.total_bombs = 50
            enemies = [
                Boss(3, 3, self.grid, self.player, self.bullet_group, self.all_sprites, self.enemy_group)
            ]

        for enemy in enemies:
            self.enemy_group.add(enemy)
            self.all_sprites.add(enemy)

    def handle_events(self):
        """Maneja los eventos del juego"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.player.existbomb and self.player.total_bombs > 0:
                    bomb = Bomb(
                        self.player.row, self.player.col, self.grid, self.screen,
                        constans.CELL_SIZE, self.player, self.all_sprites,
                        self.key_group, self.enemy_group, self.scoreManager
                    )
                    self.all_sprites.add(bomb)
                    self.player.existbomb = True
                    self.player.total_bombs -= 1

    def update(self):
        """Actualiza el estado del juego"""
        if self.stage_intro.active:
            self.stage_intro.update()
            return
        self.time = pygame.time.get_ticks()
        # Actualizar colisiones
        self.collision_handler.update()

        # Verificar transición de nivel
        if self.collision_handler.player_to_portal() and self.player.existKey and len(self.enemy_group) == 0:
            self.level += 1
            if self.level > self.max_levels:
                self.victory = True
                self.running = False
            else:
                self.initialize_level()

        # Verificar estado del jugador
        if self.player.hp <= 0 or self.player.total_bombs <= 0:
            self.game_over = True
            self.running = False

        # Actualizar todos los sprites
        self.all_sprites.update()

    def draw(self):
        """Dibuja todos los elementos del juego"""
        self.screen.fill(constans.COLORS['GRAY'])
        
        # Dibujar mapa
        self.map.draw(constans.CELL_SIZE)

        # Dibujar sprites
        self.all_sprites.draw(self.screen)

        # Dibujar barra de vida del jugador
        status_bar(
            self.screen, 10, 10, self.player.hp, self.player.max_hp,
            constans.COLORS['GREEN']
        )
        draw_text(self.screen, f"HP: {self.player.hp}", 15, 90, 10)

        # Dibujar cantidad de bombas
        draw_text(self.screen, f"Bombs: {self.player.total_bombs}", 15, 90, 35)

        # Dibujar tiempo
        draw_text(self.screen, f"Tiempo: {self.time // 1000}", 15, 750, 10)

        # Dibujar puntaje
        draw_text(self.screen, f"Puntaje: {self.scoreManager.score}", 15, constans.WIDTH // 2, 10)

        # Dibujar barras de vida de enemigos
        for enemy in self.enemy_group:
            status_bar(
                self.screen,
                enemy.rect.x,
                enemy.rect.y - 20,
                enemy.hp,
                enemy.hp_max,
                constans.COLORS['RED'],
                bar_len=50,
                bar_height=10
            )

        # Dibujar introducción del nivel si está activa
        if self.stage_intro.active:
            self.stage_intro.update()

        pygame.display.flip()

    def run(self):
        """Bucle principal del juego"""
        clock = pygame.time.Clock()
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            clock.tick(60)

        return self.game_over, self.victory

def main(skin, player_name):
    user = Users_data(player_name)
    pygame.init()
    screen = pygame.display.set_mode((constans.WIDTH, constans.HEIGHT))
    pygame.display.set_caption("Bomberman Game")
    game = Game(screen, skin)
    game_over, victory = game.run()

    # Mostrar pantalla final
    screen.fill(constans.COLORS['BLACK'])
    if victory:
        show_end_screen(screen, victory, game.scoreManager.score, game.time, user)
    elif game_over:
        show_end_screen(screen, not game_over, game.scoreManager.score, game.time, user)
    pygame.display.flip()
    pygame.time.wait(200)
    return False

if __name__ == "__main__":
    main