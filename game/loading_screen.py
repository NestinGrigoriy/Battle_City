import pygame

pygame.init()


transition_image = pygame.image.load("../game_images/transition_background.jpg")
transition_image = pygame.transform.scale(transition_image, (1920, 1080))


# Функция для отображения экрана перехода
def transition_screen(screen: pygame.Surface, duration: int = 1000) -> None:
    """
    Показывает экран перехода на заданное время.
    :param screen: экран
    :param duration: длительность показа экрана в миллисекундах
    """
    screen.blit(transition_image, (0, 0))
    pygame.display.flip()
    pygame.time.wait(duration)
