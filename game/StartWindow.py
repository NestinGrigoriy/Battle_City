import ctypes

import pygame


def start_window():
    """
    Отрисовывает главное(стартовое) окно
    :return: Нажал ли пользователь кнопку играть(переход к первому урвоню)
    """
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    pygame.init()
    width = 1920
    height = 1080
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    pygame.display.set_caption("Battle City")
    running = True

    button_play_image = pygame.image.load(
        "../main_menu_images/button_play.png"
    )
    button_play_image2 = pygame.image.load(
        "../main_menu_images/main_menu2.jpg"
    )
    main_menu_image = pygame.image.load("../main_menu_images/main_menu1.jpg")
    button_exit_image = pygame.image.load(
        "../main_menu_images/exit_button_sost1.jpg"
    )
    button_exit_image2 = pygame.image.load(
        "../main_menu_images/button_exit_sost2.jpg"
    )

    main_menu_image = pygame.transform.scale(main_menu_image, (1920, 1080))
    button_play_image2 = pygame.transform.scale(
        button_play_image2, (1920, 1080)
    )

    button_play_image = pygame.transform.scale(button_play_image, (250, 100))
    button_exit_image = pygame.transform.scale(button_exit_image, (200, 100))
    button_exit_image2 = pygame.transform.scale(button_exit_image2, (200, 200))

    button_exit_pos1 = button_exit_image.get_rect(
        center=(width // 2, height // 2 + 150)
    )
    button_exit_pos2 = button_exit_image2.get_rect(
        center=(width // 2, height // 2 + 250)
    )
    button_play_pos = button_play_image.get_rect(
        center=(width // 2, height // 2)
    )

    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if button_exit_pos1.collidepoint(mouse_pos):
                    exit()
            if event.type == pygame.QUIT:
                running = False

        screen.blit(main_menu_image, (0, 0))

        mouse_pos = pygame.mouse.get_pos()

        if button_play_pos.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                return "play1"

        if button_play_pos.collidepoint(mouse_pos):
            screen.blit(button_play_image2, (0, 0))
        else:
            screen.blit(button_play_image, button_play_pos.topleft)

        if button_exit_pos1.collidepoint(mouse_pos):
            screen.blit(button_exit_image2, button_exit_pos2.topleft)
        else:
            screen.blit(button_exit_image, button_exit_pos1.topleft)

        screen.blit(button_play_image, button_play_pos.topleft)
        screen.blit(button_exit_image, button_exit_pos1.topleft)
        pygame.display.flip()
