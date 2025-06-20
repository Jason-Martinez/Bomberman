import pygame
import pygame_menu
import pygame_menu.events
import pygame_menu.locals
import pygame_menu.themes

#CONSTANTES
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
TITLE = "   Bomberman" 

# COLORES (RGB)
COLOR_FONDO = (0, 0, 0)
COLOR_TITULO = (255, 255, 0)
COLOR_TEXTO = (255, 255, 255)
WHITE = (255,255,255)

FUENTE_RETRO = pygame_menu.font.FONT_8BIT

class Retro_star_screen:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.menu = self.create_menu()
        self.run()
        
    def create_menu(self):
        theme = pygame_menu.themes.Theme(
            background_color=COLOR_FONDO,
            title_background_color=COLOR_FONDO,
            title_font=FUENTE_RETRO,
            title_font_size=60,
            title_font_color=COLOR_TITULO,
            widget_font=FUENTE_RETRO,
            widget_font_size=30,
            widget_font_color=COLOR_TEXTO,
            widget_alignment=pygame_menu.locals.ALIGN_CENTER, # alineación de widgets
            widget_margin=(0, 20)
        )
        

        menu = pygame_menu.Menu(TITLE, WINDOW_WIDTH, WINDOW_HEIGHT, theme=theme)
        
        menu.add.button("PLAY", self.start_game)
        menu.add.button("SETTINGS", self.settings_game)
        menu.add.button("BEST SCORES", self.show_scores)
        menu.add.button("About", self.creators_information)
        menu.add.button("EXIT", pygame_menu.events.EXIT)

        return menu
    
    def run(self):
        while True:
            self.surface.fill(COLOR_FONDO)
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            self.menu.update(events)
            self.menu.draw(self.surface)
            pygame.display.flip()
    
    def start_game(self):
        print("starting game")

    def settings_game(self):
        running = True
        font = pygame.font.SysFont(None, 48)
        text = font.render("Audio Settings", True, (WHITE))
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 50)) #centrado arriba (y=50)
        while running:
            self.surface.fill(COLOR_FONDO)
            self.surface.blit(text, text_rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    running = False
            pygame.display.flip()

    def show_scores(self):
        print("Showing scores")

    def creators_information(self):
        print("Showing information")

if __name__ == '__main__':
    Retro_star_screen()