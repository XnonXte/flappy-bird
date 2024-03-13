import pygame
from config import (
    GAP_HEIGHT,
    GROUND_VEL,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    GROUND_Y,
    PIPE_WIDTH,
)


class PipeSprite(pygame.sprite.Sprite):
    def __init__(self, gap_y: int, pipe_type: str) -> None:
        super().__init__()
        self.pipe_type = pipe_type

        if pipe_type.lower() == "top":
            # Top pipe.
            scaled_height = gap_y
            self.image = pygame.transform.flip(
                pygame.transform.scale(
                    pygame.image.load(
                        "./assets/sprites/miscs/pipe-green.png"
                    ).convert_alpha(),
                    (PIPE_WIDTH, scaled_height),
                ),
                False,
                True,
            )  # Flipping it upside down.
            self.rect = self.image.get_rect(midtop=(SCREEN_WIDTH, 0))
        elif pipe_type.lower() == "bottom":
            # Bottom pipe.
            scaled_height = (SCREEN_HEIGHT - SCREEN_HEIGHT / 4) - (gap_y + GAP_HEIGHT)
            self.image = pygame.transform.scale(
                pygame.image.load(
                    "./assets/sprites/miscs/pipe-green.png"
                ).convert_alpha(),
                (
                    PIPE_WIDTH,
                    scaled_height,
                ),  # Basically grow vertically until you hit the gap.
            )
            self.rect = self.image.get_rect(midbottom=(SCREEN_WIDTH, GROUND_Y))
        else:
            raise Exception("Invalid pipe type!")

    def handle_movement(self) -> None:
        self.rect.x -= GROUND_VEL

        if self.rect.right <= 0:
            self.kill()

    def update(self) -> None:
        self.handle_movement()
