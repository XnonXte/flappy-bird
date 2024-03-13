import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, GROUND_Y, GROUND_VEL


class GroundSprite(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load("./assets/sprites/miscs/base.png"),
            (SCREEN_WIDTH * 2, SCREEN_HEIGHT / 4),
        )
        self.rect = self.image.get_rect(topright=(SCREEN_WIDTH, GROUND_Y))

    def handle_movement(self) -> None:
        self.rect.x -= GROUND_VEL

        if self.rect.x <= 0 - SCREEN_WIDTH:
            self.rect.x = 0

    def update(self) -> None:
        self.handle_movement()
