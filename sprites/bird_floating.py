import pygame
from config import (
    PLAYER_CENTER_X,
    SCREEN_HEIGHT,
    PLAYER_FLOATING_VEL,
    PLAYER_TRANSFORM_SCALE,
)


class BirdFloatingSprite(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.transform.scale_by(
            pygame.image.load(
                "./assets/sprites/birds/yellow/yellowbird-midflap.png"
            ).convert_alpha(),
            PLAYER_TRANSFORM_SCALE,
        )
        self.rect = self.image.get_rect(center=(PLAYER_CENTER_X, SCREEN_HEIGHT / 2))
        self.float_direction = -1

    def handle_floating(self) -> None:
        if self.float_direction == -1:
            self.rect.y -= PLAYER_FLOATING_VEL
            if self.rect.y <= SCREEN_HEIGHT / 2 - 10:
                self.float_direction = 1
        elif self.float_direction == 1:
            self.rect.y += PLAYER_FLOATING_VEL
            if self.rect.y >= SCREEN_HEIGHT / 2 + 10:
                self.float_direction = -1

    def update(self) -> None:
        self.handle_floating()
