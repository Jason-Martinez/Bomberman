import pygame
import pygame_menu
import pygame_menu.events
import pygame_menu.locals
import pygame_menu.themes
from user_manager import Users_data
import json

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
        #configuracion del tema visual del menu
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
            widget_margin=(0, 20), #espacio vertical entre botones
            selection_color=(255, 255, 0)  # Color de fondo al hacer hover (amarillo)
        )

        menu = pygame_menu.Menu(TITLE, WINDOW_WIDTH, WINDOW_HEIGHT, theme=theme)
        
        menu.add.button("START", self.start_game),
        menu.add.button("PERSONALIZATION", self.personalization_screen)
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

        while running:


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
        back_button_rect = pygame.Rect(WINDOW_WIDTH - 150, WINDOW_HEIGHT - 70, 120, 40)   
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

    def personalization_screen(self):
        import pygame
        from user_manager import Users_data

        running = True
        selected_skin = 0
        player_name = ""
        input_active = False
        msg = ""
        msg_timer = 0

        # Cargar y escalar skins
        skin_paths = [
            "Bomberman/assets/skins/skin1.png",
            "Bomberman/assets/skins/skin2.png",
            "Bomberman/assets/skins/skin3.png"
        ]
        img_size = int(WINDOW_HEIGHT * 0.18)
        skins = [pygame.transform.scale(pygame.image.load(path), (img_size, img_size)) for path in skin_paths]
        skin_names = ["NORMAL", "STRONG", "FAST"]

        # Fuentes
        title_font = pygame.font.Font(FUENTE_RETRO, 32)
        label_font = pygame.font.Font(FUENTE_RETRO, 20)
        input_font = pygame.font.Font(FUENTE_RETRO, 22)
        button_font = pygame.font.Font(FUENTE_RETRO, 18)

        # Botones
        btn_w, btn_h = 120, 40
        confirm_rect = pygame.Rect(WINDOW_WIDTH//2 - btn_w//2, int(WINDOW_HEIGHT*0.80), btn_w, btn_h)
        back_rect = pygame.Rect(WINDOW_WIDTH//2 - btn_w//2, int(WINDOW_HEIGHT*0.87), btn_w, btn_h)

        while running:
            self.surface.fill(COLOR_FONDO)

            # Título
            title = title_font.render("Personalization", True, COLOR_TITULO)
            self.surface.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2, 30))

            # Nombre del jugador
            label = label_font.render("Player Name:", True, WHITE)
            self.surface.blit(label, (WINDOW_WIDTH//2 - 260, 110))
            # Caja de texto
            input_box = pygame.Rect(WINDOW_WIDTH//2 - 60, 105, 220, 36)
            pygame.draw.rect(self.surface, (70, 136, 180) if input_active else (100, 100, 100), input_box, 0, border_radius=6)
            name_surface = input_font.render(player_name, True, WHITE)
            self.surface.blit(name_surface, (input_box.x + 10, input_box.y + 5))

            # Skins
            skin_y = 180
            for i, img in enumerate(skins):
                x = WINDOW_WIDTH//2 - img_size - 30 + i*(img_size + 30)
                border_color = (255, 255, 0) if i == selected_skin else (100, 100, 100)
                pygame.draw.rect(self.surface, border_color, (x-5, skin_y-5, img_size+10, img_size+10), 3)
                self.surface.blit(img, (x, skin_y))
                # Nombre del skin
                skin_label = button_font.render(skin_names[i], True, WHITE)
                self.surface.blit(skin_label, (x + img_size//2 - skin_label.get_width()//2, skin_y + img_size + 8))

            # Instrucciones para cambiar skin
            instr = label_font.render("←  Select Skin  →", True, WHITE)
            self.surface.blit(instr, (WINDOW_WIDTH//2 - instr.get_width()//2, skin_y + img_size + 40))

            # Botón Confirmar
            pygame.draw.rect(self.surface, (70, 180, 70), confirm_rect, border_radius=8)
            confirm_text = button_font.render("CONFIRM", True, WHITE)
            self.surface.blit(confirm_text, (confirm_rect.x + btn_w//2 - confirm_text.get_width()//2, confirm_rect.y + 8))

            # Botón Volver
            pygame.draw.rect(self.surface, (180, 70, 70), back_rect, border_radius=8)
            back_text = button_font.render("BACK", True, WHITE)
            self.surface.blit(back_text, (back_rect.x + btn_w//2 - back_text.get_width()//2, back_rect.y + 8))
            # ...dibuja botones y demás...

            # Mostrar mensaje si está activo
            if msg and pygame.time.get_ticks() - msg_timer < 2000:
                msg_surface = label_font.render(msg, True, (0, 255, 0))
                self.surface.blit(msg_surface, (WINDOW_WIDTH//2 - msg_surface.get_width()//2, int(WINDOW_HEIGHT*0.75)))
            elif msg and pygame.time.get_ticks() - msg_timer >= 2000:
                msg = ""

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if input_active:
                        if event.key == pygame.K_RETURN:
                            input_active = False
                        elif event.key == pygame.K_BACKSPACE:
                            player_name = player_name[:-1]
                        elif len(player_name) < 16 and event.unicode.isprintable():
                            player_name += event.unicode
                    else:
                        if event.key == pygame.K_LEFT:
                            selected_skin = (selected_skin - 1) % len(skins)
                        if event.key == pygame.K_RIGHT:
                            selected_skin = (selected_skin + 1) % len(skins)
                        if event.key == pygame.K_ESCAPE:
                            running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        input_active = True
                    else:
                        input_active = False
                    if confirm_rect.collidepoint(event.pos):
                        if player_name.strip() != "":
                            # Guardar usuario usando Users_data
                            user = Users_data(player_name.strip())
                            existing = user.get_user()
                            if existing:
                                 user.save_or_update_user(score=existing.get("score", 0), skin=selected_skin)
                            else:
                                user.save_or_update_user(score=0, skin=selected_skin)
                            msg = "Chance applied!"
                            msg_timer = pygame.time.get_ticks()
     
                    if back_rect.collidepoint(event.pos):
                        running = False

    def show_scores(self):
        running = True
        font = pygame.font.Font(FUENTE_RETRO, 25)
        title_text = font.render("BEST SCORES", True, WHITE)
        text_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 50))

        #obtener el top 5 usando User_data
        user_manager = Users_data("")
        top5= user_manager.get_top5()
        

        # Botón volver: debajo del texto, alineado a la izquierda con margen
        button_font = pygame.font.Font(FUENTE_RETRO, 16)
        back_button_x = 30  # margen izquierdo
        back_button_y = text_rect.bottom + 30  # debajo del texto, con margen
        back_button_rect = pygame.Rect(back_button_x, back_button_y, 120, 40)
        back_text = button_font.render("BACK", True, WHITE)
        
        while running:
            self.surface.fill(COLOR_FONDO)
            self.surface.blit(title_text, text_rect)

            # Mostrar los puntajes alineados
            for i, entry in enumerate(top5):
                name = entry.get('user', '')
                score = entry.get('score', 0)
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
            id1 = font_mini.render("Carnet: 2025094482", True, WHITE)
            name2 = font_mini.render("Jason Rene Martinez Gutierrez", True, WHITE)
            id2 = font_mini.render("Carnet: 2025105665", True, WHITE)

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
