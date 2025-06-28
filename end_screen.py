import pygame
from main_menu import Retro_star_screen
# Configuración básica
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
COLOR_FONDO = (50,50,100)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
FUENTE_RETRO = "Bomberman/assets/fonts/Minecraftia-Regular.ttf"

def show_end_screen(screen, won, score, time_elapsed):
    pygame.init()
    running = True

    title_font = pygame.font.Font(FUENTE_RETRO, 50)
    info_font = pygame.font.Font(FUENTE_RETRO, 25)
    button_font = pygame.font.Font(FUENTE_RETRO, 20)

    title_text = "YOU WIN!" if won else "GAME OVER"
    title_render = title_font.render(title_text, True, YELLOW)

    score_text = info_font.render(f"SCORE: {score}", True, WHITE)
    minutes = int(time_elapsed) // 60
    seconds = int(time_elapsed) % 60
    time_str = f"{minutes:02}:{seconds:02}"
    time_text = info_font.render(f"TIME: {time_str}", True, WHITE)

    button_rect = pygame.Rect(WINDOW_WIDTH // 2 - 100, 400, 200, 50)
    button_text = button_font.render("Back to Menu", True, WHITE)

    while running:
        screen.fill(COLOR_FONDO)
        screen.blit(title_render, title_render.get_rect(center=(WINDOW_WIDTH // 2, 100)))
        screen.blit(score_text, score_text.get_rect(center=(WINDOW_WIDTH // 2, 200)))
        screen.blit(time_text, time_text.get_rect(center=(WINDOW_WIDTH // 2, 250)))

        pygame.draw.rect(screen, (180, 70, 70), button_rect)
        screen.blit(button_text, button_text.get_rect(center=button_rect.center))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        pygame.display.flip()



if __name__ == "__main__":
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Test End Screen")
    
    show_end_screen(screen, won=True, score=1250, time_elapsed=100)
    # Cuando termina la pantalla final, abre el menú principal
    Retro_star_screen()