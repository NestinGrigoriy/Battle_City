import ctypes

import pygame
from states import States


def end_screen() -> States:
    """
    Отображает экран прохождения игры
    :return статус экрана:
    """
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    pygame.init()
    width = 1920
    height = 1080
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    pygame.display.set_caption("Battle City")

    end_image = pygame.image.load("../game_images/end.jpg")
    end_image = pygame.transform.scale(end_image, (1920, 1080))
    end_rect = end_image.get_rect(topleft=(0, 0))

    back_image = pygame.image.load("../game_images/back.png")
    back_image = pygame.transform.scale(back_image, (300, 300))
    back_rect = back_image.get_rect(center=((width // 2), (height * 2) // 3))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if back_rect.collidepoint(mouse_pos):
                    return States.MENU
            if event.type == pygame.QUIT:
                running = False
        screen.blit(end_image, end_rect)
        screen.blit(back_image, back_rect)
        pygame.display.flip()
