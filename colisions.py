import pygame
class CollisionHandler:
    def __init__(self, player, screen, key_group, portal_group, enemy_group, bullet_group, player_group, maps):
        self.player = player
        self.screen = screen
        self.key_group = key_group
        self.portal_group = portal_group
        self.enemy_group = enemy_group
        self.bullet_group = bullet_group
        self.player_group = player_group
        self.map = maps

    def player_to_key(self):
        hits = pygame.sprite.groupcollide(self.player_group, self.key_group, False, True)
        if hits:
            for _ in hits:
                self.player.existKey = True
            print(f'Tiene la llave? {self.player.existKey}')

    def player_to_portal(self):
        hits = pygame.sprite.groupcollide(self.player_group, self.portal_group, False, False)
        if hits:
            for _ in hits:
                if self.player.existKey:
                    return True
            return False

    def player_to_enemy(self):
        hits = pygame.sprite.groupcollide(self.player_group, self.enemy_group, False, True)
        if hits:
            for _ in hits:
                self.player.hp -= 25

    def player_to_bullet(self):
        hits = pygame.sprite.groupcollide(self.player_group, self.bullet_group, False, True)
        if hits:
            for _ in hits:
                self.player.hp -= 25

    def update(self):
        self.player_to_key()
        self.player_to_bullet()
        self.player_to_enemy()
        self.player_to_portal()