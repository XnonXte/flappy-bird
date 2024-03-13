import pygame
from config import (
    SCREEN_HEIGHT,
    GRAVITY_VEL,
    PLAYER_COLLIDED_WITH_PIPE,
    PLAYER_COLLIDED_WITH_GROUND,
    PLAYER_FLAP_GRAVITY,
    GROUND_Y,
    PLAYER_TRANSFORM_SCALE,
    PLAYER_FLAP_COOLDOWN,
    PLAYER_CENTER_X,
    SFX_HIT,
    SFX_WING,
    SFX_DIE,
    SCORE_INCREMENT,
)


class BirdSprite(pygame.sprite.Sprite):
    def __init__(self, pipe_group: pygame.sprite.Group):
        super().__init__()
        self.FLAP_FRAMES = [
            pygame.image.load(
                "./assets/sprites/birds/yellow/yellowbird-upflap.png"
            ).convert_alpha(),
            pygame.image.load(
                "./assets/sprites/birds/yellow/yellowbird-midflap.png"
            ).convert_alpha(),
            pygame.image.load(
                "./assets/sprites/birds/yellow/yellowbird-downflap.png"
            ).convert_alpha(),
        ]
        self.flap_frames_index = 0
        self.image = pygame.transform.scale_by(
            self.FLAP_FRAMES[self.flap_frames_index], PLAYER_TRANSFORM_SCALE
        )
        self.rect = self.image.get_rect(center=(PLAYER_CENTER_X, SCREEN_HEIGHT / 2))
        self.last_flap_time = 0
        self.gravity = 0
        self.pipe_group = pipe_group

    def handle_animation(self):
        self.flap_frames_index += 0.1

        if self.flap_frames_index >= len(self.FLAP_FRAMES):
            # So we don't shot ourself in the foot.
            self.flap_frames_index = 0

        self.image = pygame.transform.scale_by(
            self.FLAP_FRAMES[int(self.flap_frames_index)], PLAYER_TRANSFORM_SCALE
        )

    def handle_flap(self):
        self.gravity += GRAVITY_VEL

        if self.rect.y + self.rect.height < GROUND_Y:
            self.rect.y += self.gravity
        else:
            self.rect.y = GROUND_Y - self.rect.height

        current_time = pygame.time.get_ticks()
        keys = (
            pygame.key.get_pressed()
        )  # It sucks that we can't use pygame.event.get() in a sprite class.

        if (
            keys[pygame.K_SPACE] == True
            and current_time - self.last_flap_time > PLAYER_FLAP_COOLDOWN
        ):
            # Flap within a given interval.
            self.gravity = PLAYER_FLAP_GRAVITY
            SFX_WING.play()
            self.last_flap_time = current_time

    def handle_ground_collision(self):
        # Collision with the ceiling and the sky.
        if self.rect.bottom >= GROUND_Y:
            SFX_DIE.play()
            self.image = pygame.transform.rotate(
                self.image, 270
            )  # TODO: Figure out why this isn't working.
            pygame.event.post(pygame.event.Event(PLAYER_COLLIDED_WITH_GROUND))

    def handle_rotation(self):
        if self.rect.bottom < GROUND_Y:
            if self.gravity <= 0:
                # When flapping.
                self.image = pygame.transform.rotate(self.image, 30)
            elif self.gravity >= 0:
                # When falling down.
                self.image = pygame.transform.rotate(self.image, 330)

    def handle_pipe_collision(self):
        if pygame.sprite.spritecollide(self, self.pipe_group, False):
            SFX_HIT.play()
            pygame.event.post(pygame.event.Event(PLAYER_COLLIDED_WITH_PIPE))

    def handle_score_increment(self):
        for pipe_sprite in self.pipe_group:
            if pipe_sprite.pipe_type == "top":
                if pipe_sprite.rect.right == PLAYER_CENTER_X:
                    if self.rect.y >= 0:
                        # to prevent cheating, check if the player is in the boundary.
                        pygame.event.post(pygame.event.Event(SCORE_INCREMENT))
                    else:
                        SFX_HIT.play()
                        pygame.event.post(pygame.event.Event(PLAYER_COLLIDED_WITH_PIPE))

    def update(self):
        self.handle_animation()
        self.handle_pipe_collision()
        self.handle_ground_collision()
        self.handle_flap()
        self.handle_rotation()
        self.handle_score_increment()
