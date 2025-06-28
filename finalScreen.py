import pygame
import constans
# Configuración básica
constans.WINDOW_WIDTH = 800

def show_end_screen(screen, won, score, time_elapsed, user):
    '''Pantalla final que indica si el usuario ganó o perdió'''
    pygame.init()
    running = True

    title_font = pygame.font.Font(constans.FUENTE_RETRO, 50)
    info_font = pygame.font.Font(constans.FUENTE_RETRO, 25)
    button_font = pygame.font.Font(constans.FUENTE_RETRO, 20)

    title_text = "YOU WIN!" if won else "GAME OVER"
    title_render = title_font.render(title_text, True, constans.COLORS['YELLOW'])

    score_text = info_font.render(f"SCORE: {score}", True, constans.COLORS['WHITE'])
    seconds = int(time_elapsed) % 60
    time_text = info_font.render(f"Segundos: {seconds}", True, constans.COLORS['WHITE'])

    button_rect = pygame.Rect(constans.WINDOW_WIDTH // 2 - 100, 400, 200, 50)
    button_text = button_font.render("Back to Menu", True, constans.COLORS['WHITE'])

    while running:
        screen.fill(constans.COLORS['BG'])
        screen.blit(title_render, title_render.get_rect(center=(constans.WINDOW_WIDTH // 2, 100)))
        screen.blit(score_text, score_text.get_rect(center=(constans.WINDOW_WIDTH // 2, 200)))
        screen.blit(time_text, time_text.get_rect(center=(constans.WINDOW_WIDTH // 2, 250)))

        pygame.draw.rect(screen, (180, 70, 70), button_rect)
        screen.blit(button_text, button_text.get_rect(center=button_rect.center))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                user.update_score(score)
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    running = False
                    user.update_score(score)
                    break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    user.update_score(score)
                    break

        pygame.display.flip()