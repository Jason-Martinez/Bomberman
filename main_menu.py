import pygame
import pygame_menu
import pygame_menu.events
import pygame_menu.locals
import pygame_menu.themes
from user_manager import Users_data

#CONSTANTES
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
TITLE = "             Bomberman" 

# COLORES (RGB)
COLOR_FONDO = (50, 50, 100)  
COLOR_TITULO = (255, 255, 0)
COLOR_TEXTO = (255, 255, 255)
AMARILLO = (255,255,0)
WHITE = (255,255,255)

FUENTE_RETRO = "Bomberman/assets/fonts/Minecraftia-Regular.ttf"   #esta es la fuente que llevara todo el juego

class Retro_star_screen:
    def __init__(self):
        pygame.init()
        pygame.mixer.init() #inicializa el mixer de sonido
        pygame.mixer.music.load("Bomberman/assets/sounds/background_music.mp3")#carga la música
        pygame.mixer.music.play(-1)

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
            widget_margin=(0, 20),
            selection_color=(255, 255, 0)  # Color de fondo al hacer hover (amarillo)
        )
        

        menu = pygame_menu.Menu(TITLE, WINDOW_WIDTH, WINDOW_HEIGHT, theme=theme)
        
        menu.add.button("START", self.start_game)
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
        running = True
        font = pygame.font.Font(FUENTE_RETRO, 30)
        text = font.render("USER REGISTRATION ", True, (WHITE))
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 50)) #centrado arriba (y=50)

        while running:
            self.surface.fill(COLOR_FONDO)
            self.surface.blit(text, text_rect)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            pygame.display.flip() 

    def settings_game(self):
        running = True
        font = pygame.font.Font(FUENTE_RETRO, 30)
        text = font.render("Audio Settings", True, (WHITE))
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 50)) #centrado arriba (y=50)

        #Estado del sonido
        sound_on = pygame.mixer.music.get_busy() #true si la musica esta sonando

        #boton de sonido
        button_font = pygame.font.Font(FUENTE_RETRO,16)
        def get_button_text():
            return "SOUND: ON" if sound_on else "SOUND: OFF"
        button_text = button_font.render(get_button_text(), True, WHITE)
        button_rect = pygame.Rect(WINDOW_WIDTH // 2 - 80, 150, 160, 50)

        #boton de volver
        back_button_rect = pygame.Rect(WINDOW_WIDTH // 2 - 60, 300, 120, 40)   
        back_text = button_font.render("BACK", True, WHITE)     


        while running:
            self.surface.fill(COLOR_FONDO)
            self.surface.blit(text, text_rect)
            #dibuja el boton
            pygame.draw.rect(self.surface, (70,136, 180), button_rect)
            button_text = button_font.render(get_button_text(), True, WHITE)
            self.surface.blit(button_text, (button_rect.x + 15, button_rect.y + 10))
            #boton volver
            pygame.draw.rect(self.surface, (180, 70, 70), back_button_rect)
            self.surface.blit(back_text, (back_button_rect.x + 20, back_button_rect.y + 5))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        if sound_on:
                            pygame.mixer.music.pause()
                            sound_on = False
                        else:
                            pygame.mixer.music.unpause()
                            sound_on = True
                    if back_button_rect.collidepoint(event.pos):
                        running = False
            
            pygame.display.flip()

    def show_scores(self):
        running = True
        font = pygame.font.Font(FUENTE_RETRO, 25)
        title_text = font.render("BEST SCORES", True, WHITE)
        text_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 50))

        #obtener el top 5 usando User_data
        user = Users_data("")
        top5= user.get_top5()
        

        # Botón volver: debajo del texto, alineado a la izquierda con margen
        button_font = pygame.font.Font(FUENTE_RETRO, 16)
        back_button_x = 30  # margen izquierdo
        back_button_y = text_rect.bottom + 30  # debajo del texto, con margen
        back_button_rect = pygame.Rect(back_button_x, back_button_y, 120, 40)
        back_text = button_font.render("BACK", True, WHITE)
        
        while running:
            self.surface.fill(COLOR_FONDO)
            self.surface.blit(title_text, text_rect)

            # Mostrar los puntajes alineados manualmente sin usar ':' que puede generar errores visuales
            for i, entry in enumerate(top5):
                name = entry['user']
                score = entry['score']
                # Alineación manual: nombre a la izquierda con 10 espacios, score a la derecha
                line = f"{i+1}. {name:<10} {score:>4} pts"
                score_text = font.render(line, True, WHITE)
                self.surface.blit(score_text, (WINDOW_WIDTH // 2 - 150, 100 + i * 40))
            #boton de vovler
            pygame.draw.rect(self.surface, (180,70,70), back_button_rect)
            self.surface.blit(back_text, (back_button_rect.x + 20, back_button_rect.y + 5))
            
    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button_rect.collidepoint(event.pos):
                        running = False

            pygame.display.flip()


    def creators_information(self):
        running = True

        #cargar fuentes
        font_title = pygame.font.Font(FUENTE_RETRO, 28)
        font_text = pygame.font.Font(FUENTE_RETRO, 18)
        font_mini = pygame.font.Font(FUENTE_RETRO, 16)

        #cargar imagenes de los autores
        try:
            img_mainor = pygame.image.load("Bomberman/assets/images/Mainor.jpg")
            img_jason = pygame.image.load("Bomberman/assets/images/Jason.jpg")
        except Exception as e:
            img_mainor = img_jason = pygame.Surface((100,100))
            img_mainor.fill((100,100,100)) #relleno por defecto
            img_jason.fill(100,100,100)
        
        img_mainor = pygame.transform.scale(img_mainor, (100, 100))
        img_jason = pygame.transform.scale(img_jason, (100, 100))
        
        #titulo
        title_text = font_title.render("ABOUT & HELP", True, WHITE)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 40))

        #texto
        info_lines = [
            "Instituto Tecnológico de Costa Rica",
            "Carrera: Ingeniería en Computación",
            "Curso: Introducción a la Programación",
            "Profesor: Diego Mora Rojas",
            "País: Costa Rica",
            "Versión 1.0 - Junio 2025",
            "",
            "controles del Juego:",
            "W - Mover arriba",
            "A - Mover izquierda",
            "S - Mover abajo",
            "D - Mover derecha",
            "Espacio - Colocar Bomba"
            "",
            "Objetivo: Encuentra la llave y abre la puerta.",
            "Evita trampas y enemigos, y usa tus ítems estratégicamente."
        ]


        #boton de volver
        button_font = pygame.font.Font(FUENTE_RETRO, 16)
        back_button_rect = pygame.Rect(WINDOW_WIDTH - 160, 520, 120, 40)
        back_text = button_font.render("BACK", True, WHITE)

        while running:
            self.surface.fill(COLOR_FONDO)
            self.surface.blit(title_text, title_rect)

            #Mostrar imagenes
            self.surface.blit(img_mainor, (80, 80))
            self.surface.blit(img_jason, (WINDOW_WIDTH - 180, 80))

            # Nombres y carnets debajo de cada foto
            name1 = font_mini.render("Mainor Oliver Martinez Sanchez", True, WHITE)
            id1 = font_mini.render("Carnet: 2022000001", True, WHITE)
            name2 = font_mini.render("Jason Rene Martinez Gutierrez", True, WHITE)
            id2 = font_mini.render("Carnet: 2022000002", True, WHITE)

            # Debajo de la foto izquierda
            self.surface.blit(name1, (50, 185))
            self.surface.blit(id1, (50, 205))

            # Debajo de la foto derecha
            self.surface.blit(name2, (WINDOW_WIDTH - 310, 185))
            self.surface.blit(id2, (WINDOW_WIDTH - 310, 205))

            for i, line in enumerate(info_lines):
                y = 260 + i * 22 
                if y < WINDOW_HEIGHT - 60:
                    line_render = font_text.render(line, True, WHITE)
                    self.surface.blit(line_render, (60, y))

            #boton volver
            pygame.draw.rect(self.surface, (200, 70, 70), back_button_rect)
            self.surface.blit(back_text, (back_button_rect.x + 20, back_button_rect.y + 5))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button_rect.collidepoint(event.pos):
                        running = False

            pygame.display.flip()            

if __name__ == '__main__':
    Retro_star_screen()
