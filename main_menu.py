import pygame
import pygame_menu
import pygame_menu.events
import pygame_menu.locals
import pygame_menu.themes
from user_manager import Users_data
import json
from game import main
import os
from scripts.paths_list import get_path
import constans


class Retro_star_screen:
    def __init__(self):
        pygame.init()
        pygame.mixer.init() #inicializa el mixer de sonido
        pygame.mixer.music.load(os.path.join('Assets', 'sounds', 'background_music.mp3'))#carga la música
        pygame.mixer.music.play(-1)

        self.surface = pygame.display.set_mode((constans.WINDOW_WIDTH,constans.WINDOW_HEIGHT))
        pygame.display.set_caption(constans.TITLE)
        self.menu = self.create_menu()
        self.selected_skin = 0
        self.player_name = ''
        self.run()
        
    def create_menu(self):
        #configuracion del tema visual del menu
        theme = pygame_menu.themes.Theme(
            background_color=constans.COLORS['BG'],
            title_background_color=constans.COLORS['BG'],
            title_font=constans.FUENTE_RETRO,
            title_font_size=60,
            title_font_color=constans.COLORS['TITLE'],
            widget_font=constans.FUENTE_RETRO,
            widget_font_size=30,
            widget_font_color=constans.COLORS['WHITE'],
            widget_alignment=pygame_menu.locals.ALIGN_CENTER, # alineación de widgets
            widget_margin=(0, 20), #espacio vertical entre botones
            selection_color=(255, 255, 0)  # Color de fondo al hacer hover (amarillo)
        )

        menu = pygame_menu.Menu(constans.TITLE, constans.WINDOW_WIDTH, constans.WINDOW_HEIGHT, theme=theme)
        
        menu.add.button("START", self.start_game),
        menu.add.button("PERSONALIZATION", self.personalization_screen)
        menu.add.button("SETTINGS", self.settings_game)
        menu.add.button("BEST SCORES", self.show_scores)
        menu.add.button("About", self.creators_information)
        menu.add.button("EXIT", pygame_menu.events.EXIT)

        return menu
    
    def run(self):
        while True:
            self.surface.fill(constans.COLORS['BG'])
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
            main(self.selected_skin, self.player_name)
            running = False
            break

    def settings_game(self):
        running = True
        font = pygame.font.Font(constans.FUENTE_RETRO, 30)
        text = font.render("Audio Settings", True, (constans.COLORS['WHITE']))
        text_rect = text.get_rect(center=(constans.WINDOW_WIDTH // 2, 50)) #centrado arriba (y=50)

        #Estado del sonido
        sound_on = pygame.mixer.music.get_busy() #true si la musica esta sonando

        #boton de sonido
        button_font = pygame.font.Font(constans.FUENTE_RETRO,16)
        def get_button_text():
            return "SOUND: ON" if sound_on else "SOUND: OFF"
        button_text = button_font.render(get_button_text(), True, constans.COLORS['WHITE'])
        button_rect = pygame.Rect(constans.WINDOW_WIDTH // 2 - 80, 150, 160, 50)

        #boton de volver
        back_button_rect = pygame.Rect(constans.WINDOW_WIDTH - 150, constans.WINDOW_HEIGHT - 70, 120, 40)   
        back_text = button_font.render("BACK", True, constans.COLORS['WHITE'])     


        while running:
            self.surface.fill(constans.COLORS['BG'])
            self.surface.blit(text, text_rect)
            #dibuja el boton
            pygame.draw.rect(self.surface, (70,136, 180), button_rect)
            button_text = button_font.render(get_button_text(), True, constans.COLORS['WHITE'])
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
        self.selected_skin = 0
        self.player_name = ""
        input_active = False
        msg = ""
        msg_timer = 0

        # Cargar y escalar skins
        skin_paths = get_path(os.path.join('Assets', 'skins'))
        img_size = int(constans.WINDOW_HEIGHT * 0.18)
        skins = [pygame.transform.scale(pygame.image.load(path), (img_size, img_size)) for path in skin_paths]
        skin_names = ["NORMAL", "STRONG", "FAST"]

        # Fuentes
        title_font = pygame.font.Font(constans.FUENTE_RETRO, 32)
        label_font = pygame.font.Font(constans.FUENTE_RETRO, 20)
        input_font = pygame.font.Font(constans.FUENTE_RETRO, 22)
        button_font = pygame.font.Font(constans.FUENTE_RETRO, 18)

        # Botones
        btn_w, btn_h = 120, 40
        confirm_rect = pygame.Rect(constans.WINDOW_WIDTH//2 - btn_w//2, int(constans.WINDOW_HEIGHT*0.80), btn_w, btn_h)
        back_rect = pygame.Rect(constans.WINDOW_WIDTH//2 - btn_w//2, int(constans.WINDOW_HEIGHT*0.87), btn_w, btn_h)

        while running:
            self.surface.fill(constans.COLORS['BG'])
            #pner el nombre en la esquina del usuario actual
            if hasattr(self, "current_user") and self.current_user:
                user_label = label_font.render(f"User: {self.current_user}", True, constans.COLORS['WHITE'])
                self.surface.blit(user_label, (10, 10))
            # Título
            title = title_font.render("Personalization", True, constans.COLORS['TITLE'])
            self.surface.blit(title, (constans.WINDOW_WIDTH//2 - title.get_width()//2, 30))

            # Nombre del jugador
            label = label_font.render("Player Name:", True, constans.COLORS['WHITE'])
            self.surface.blit(label, (constans.WINDOW_WIDTH//2 - 260, 110))
            # Caja de texto
            input_box = pygame.Rect(constans.WINDOW_WIDTH//2 - 60, 105, 220, 36)
            pygame.draw.rect(self.surface, (70, 136, 180) if input_active else (100, 100, 100), input_box, 0, border_radius=6)
            name_surface = input_font.render(self.player_name, True, constans.COLORS['WHITE'])
            self.surface.blit(name_surface, (input_box.x + 10, input_box.y + 5))

            # Skins
            skin_y = 180
            for i, img in enumerate(skins):
                x = constans.WINDOW_WIDTH//2 - img_size - 30 + i*(img_size + 30)
                border_color = (255, 255, 0) if i == self.selected_skin else (100, 100, 100)
                pygame.draw.rect(self.surface, border_color, (x-5, skin_y-5, img_size+10, img_size+10), 3)
                self.surface.blit(img, (x, skin_y))
                # Nombre del skin
                skin_label = button_font.render(skin_names[i], True, constans.COLORS['WHITE'])
                self.surface.blit(skin_label, (x + img_size//2 - skin_label.get_width()//2, skin_y + img_size + 8))

            # Instrucciones para cambiar skin con las flechas
            instr = label_font.render("←  Select Skin  →", True, constans.COLORS['WHITE'])
            self.surface.blit(instr, (constans.WINDOW_WIDTH//2 - instr.get_width()//2, skin_y + img_size + 40))

            # Botón Confirmar guarda el usuario y skin seleccionada
            pygame.draw.rect(self.surface, (70, 180, 70), confirm_rect, border_radius=8)
            confirm_text = button_font.render("CONFIRM", True, constans.COLORS['WHITE'])
            self.surface.blit(confirm_text, (confirm_rect.x + btn_w//2 - confirm_text.get_width()//2, confirm_rect.y + 8))

            # Botón Volver: guarda el usuario y skin seleccionada
            pygame.draw.rect(self.surface, (180, 70, 70), back_rect, border_radius=8)
            back_text = button_font.render("BACK", True, constans.COLORS['WHITE'])
            self.surface.blit(back_text, (back_rect.x + btn_w//2 - back_text.get_width()//2, back_rect.y + 8))
            # ...dibuja botones y demás...

            # Mostrar mensaje si está activo
            if msg and pygame.time.get_ticks() - msg_timer < 2000:
                msg_surface = label_font.render(msg, True, (0, 255, 0))
                self.surface.blit(msg_surface, (constans.WINDOW_WIDTH//2 - msg_surface.get_width()//2, int(constans.WINDOW_HEIGHT*0.75)))
            elif msg and pygame.time.get_ticks() - msg_timer >= 2000:
                msg = ""

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                    #manejo de teclas
                if event.type == pygame.KEYDOWN:
                    if input_active:
                        if event.key == pygame.K_RETURN:
                            input_active = False
                        elif event.key == pygame.K_BACKSPACE:
                            self.player_name = self.player_name[:-1]
                        elif len(self.player_name) < 16 and event.unicode.isprintable():
                            self.player_name += event.unicode
                    else:
                        #cambia skin con las flechas
                        if event.key == pygame.K_LEFT:
                            self.selected_skin = (self.selected_skin - 1) % len(skins)
                        if event.key == pygame.K_RIGHT:
                            self.selected_skin = (self.selected_skin + 1) % len(skins)
                            #salir de la pantalla de personalizacion con       ESC
                        if event.key == pygame.K_ESCAPE:
                            running = False
                            #manejo de clics del mouse
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        input_active = True 
                    else:
                        input_active = False
                    if confirm_rect.collidepoint(event.pos):
                        if self.player_name.strip() != "":
                            # Guardar usuario usando Users_data
                            user = Users_data(self.player_name.strip())
                            existing = user.get_user()
                            if existing:
                                 user.save_or_update_user(score=existing.get("score", 0), skin=self.selected_skin)
                            else:
                                user.save_or_update_user(score=0, skin=self.selected_skin)
                            self.current_user = self.player_name.strip()
                            msg = "Chance applied!"
                            msg_timer = pygame.time.get_ticks()
                    #si se presiona el boton volver
                    if back_rect.collidepoint(event.pos):
                        running = False

    def show_scores(self):
        running = True
        font = pygame.font.Font(constans.FUENTE_RETRO, 25)
        title_text = font.render("BEST SCORES", True, constans.COLORS['WHITE'])
        text_rect = title_text.get_rect(center=(constans.WINDOW_WIDTH // 2, 50))

        #obtener el top 5 usando User_data
        user_manager = Users_data("")
        top5= user_manager.get_top5()
        

        # Botón volver: debajo del texto, alineado a la izquierda con margen
        button_font = pygame.font.Font(constans.FUENTE_RETRO, 16)
        back_button_x = 30  # margen izquierdo
        back_button_y = text_rect.bottom + 30  # debajo del texto, con margen
        back_button_rect = pygame.Rect(back_button_x, back_button_y, 120, 40)
        back_text = button_font.render("BACK", True, constans.COLORS['WHITE'])
        
        while running:
            self.surface.fill(constans.COLORS['BG'])
            self.surface.blit(title_text, text_rect)

            # Mostrar los puntajes alineados
            for i, entry in enumerate(top5):
                name = entry.get('user', '')
                score = entry.get('score', 0)
                # Alineación manual: nombre a la izquierda con 10 espacios, score a la derecha
                line = f"{i+1}. {name:<10} {score:>4} pts"
                score_text = font.render(line, True, constans.COLORS['WHITE'])
                self.surface.blit(score_text, (constans.WINDOW_WIDTH // 2 - 150, 100 + i * 40))
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
        font_title = pygame.font.Font(constans.FUENTE_RETRO, 28)
        font_text = pygame.font.Font(constans.FUENTE_RETRO, 18)
        font_mini = pygame.font.Font(constans.FUENTE_RETRO, 16)

        #cargar imagenes de los autores
        try:
            profiles = get_path(os.path.join('Assets', 'images'))
            img_mainor = pygame.image.load(profiles[1])
            img_jason = pygame.image.load(profiles[0])
        except Exception as e:
            img_mainor = img_jason = pygame.Surface((100,100))
            img_mainor.fill((100,100,100)) #relleno por defecto
            img_jason.fill(100,100,100)
        
        img_mainor = pygame.transform.scale(img_mainor, (100, 100))
        img_jason = pygame.transform.scale(img_jason, (100, 100))
        
        #titulo
        title_text = font_title.render("ABOUT & HELP", True, constans.COLORS['WHITE'])
        title_rect = title_text.get_rect(center=(constans.WINDOW_WIDTH // 2, 40))

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
        button_font = pygame.font.Font(constans.FUENTE_RETRO, 16)
        back_button_rect = pygame.Rect(constans.WINDOW_WIDTH - 160, 520, 120, 40)
        back_text = button_font.render("BACK", True, constans.COLORS['WHITE'])

        while running:
            self.surface.fill(constans.COLORS['BG'])
            self.surface.blit(title_text, title_rect)

            #Mostrar imagenes
            self.surface.blit(img_mainor, (80, 80))
            self.surface.blit(img_jason, (constans.WINDOW_WIDTH - 180, 80))

            # Nombres y carnets debajo de cada foto
            name1 = font_mini.render("Mainor Oliver Martinez Sanchez", True, constans.COLORS['WHITE'])
            id1 = font_mini.render("Carnet: 2025094482", True, constans.COLORS['WHITE'])
            name2 = font_mini.render("Jason Rene Martinez Gutierrez", True, constans.COLORS['WHITE'])
            id2 = font_mini.render("Carnet: 2025105665", True, constans.COLORS['WHITE'])

            # Debajo de la foto izquierda
            self.surface.blit(name1, (50, 185))
            self.surface.blit(id1, (50, 205))

            # Debajo de la foto derecha
            self.surface.blit(name2, (constans.WINDOW_WIDTH - 310, 185))
            self.surface.blit(id2, (constans.WINDOW_WIDTH - 310, 205))

            for i, line in enumerate(info_lines):
                y = 260 + i * 22 
                if y < constans.WINDOW_HEIGHT - 60:
                    line_render = font_text.render(line, True, constans.COLORS['WHITE'])
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
