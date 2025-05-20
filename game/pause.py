import pygame

pygame.init()


load_save_image = pygame.image.load("../game_images/save.png")
save_image = pygame.transform.scale(load_save_image, (600, 200))
save_rect = save_image.get_rect(center=(1920 // 2, 1080 // 2))

load_next_image = pygame.image.load("../game_images/next_button.png")
next_image = pygame.transform.scale(load_next_image, (600, 200))
next_rect = next_image.get_rect(center=(1920 // 2, 1080 // 3))


def pause(screen: pygame.Surface) -> bool:
    """Отрисовывает меню паузы"""
    while True:
        screen.blit(save_image, save_rect)
        screen.blit(next_image, next_rect)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if next_rect.collidepoint(mouse_pos):
                    return False
                if save_rect.collidepoint(mouse_pos):
                    return True
        pygame.display.flip()
