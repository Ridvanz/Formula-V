import pygame



def __game_over_overlay(window):
    font_size
    go_font = pygame.font.Font(pygame.font.get_default_font(), 44)
    txt_go  = go_font.render("Game Over", 1, s.COLOURS["red"])
    x       = (s.DIMENSIONS[0] - txt_go.get_size()[0]) / 2
    y       = (s.DIMENSIONS[1] - txt_go.get_size()[1]) / 2
    overlay = pygame.Surface(s.DIMENSIONS, pygame.SRCALPHA)

    overlay.fill((255, 255, 255, 90))
    overlay.blit(txt_go, (x, y))
    window.blit(overlay, (0,0))