import sys
import random
from enum import Enum
import pygame

from config import *
from sprites import *
from hooks import *
from utils import *


class FlappyBird:
    def main(self) -> None:
        class State(Enum):
            PLAYING = "PLAYING"
            MENU = "MENU"

        pygame.time.set_timer(SPAWN_PIPE, SPAWN_PIPE_INTERVAL)

        pipe_group = pygame.sprite.Group()
        base_group = pygame.sprite.GroupSingle()
        player_group = pygame.sprite.GroupSingle()

        player_floating_group = pygame.sprite.GroupSingle()
        base = ground.GroundSprite()
        player_floating = bird_floating.BirdFloatingSprite()

        player_floating_group.add(player_floating)
        base_group.add(base)

        pygame.display.set_caption("Flappy Bird")
        pygame.display.set_icon(ICON)

        # Game variables.
        score = 0
        running = True
        state = State.MENU

        while running:
            match state:
                case State.PLAYING:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            # Exit.
                            running = False

                        if event.type in [
                            PLAYER_COLLIDED_WITH_PIPE,
                            PLAYER_COLLIDED_WITH_GROUND,
                        ]:
                            use_text.draw_text_with_outline(
                                HEADING,
                                "Game Over!",
                                center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2),
                            )
                            use_text.draw_text_with_outline(
                                BODY,
                                f"Score: {score}",
                                center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / (3 / 2)),
                            )
                            use_text.draw_text_with_outline(
                                BODY,
                                f"Best: {history.get_highest_score()}",
                                center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / (5 / 4)),
                            )

                            history.write_history(
                                score,
                                (
                                    "pipe"
                                    if event.type == PLAYER_COLLIDED_WITH_PIPE
                                    else "ground"
                                ),
                            )

                            # Reset stats.
                            pipe_group.empty()
                            player_group.empty()
                            score = 0
                            state = State.MENU

                            pygame.display.update()
                            pygame.time.wait(5000)

                        if event.type == SPAWN_PIPE:
                            # Generating a pipe.
                            # Create 2 pipes (top and bottom) with a little bit of gap for the player to pass through.
                            random_gap_y = random.randint(
                                10, int(SCREEN_HEIGHT / 4) - 10
                            )  # Create a 10px padding on the top and bottom.
                            top_pipe = pipe.PipeSprite(random_gap_y, "top")
                            bottom_pipe = pipe.PipeSprite(random_gap_y, "bottom")
                            pipe_group.add(top_pipe)
                            pipe_group.add(bottom_pipe)

                        if event.type == SCORE_INCREMENT:
                            # When the player passes a pipe.
                            score += 1
                            SFX_POINT.play()

                    # Background image.
                    SCREEN.fill("Black")
                    SCREEN.blit(
                        pygame.transform.scale(
                            BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT)
                        ),
                        (0, 0),
                    )

                    # Drawing and updating groups.
                    base_group.draw(SCREEN)
                    base_group.update()
                    pipe_group.draw(SCREEN)
                    pipe_group.update()
                    player_group.draw(SCREEN)
                    player_group.update()

                    # Score.
                    use_text.draw_text_with_outline(
                        HEADING,
                        str(score),
                        center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4),
                    )

                case State.MENU:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            # Exit.
                            running = False

                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                player = bird.BirdSprite(pipe_group)
                                player_group.add(player)
                                state = State.PLAYING

                    # Background image.
                    SCREEN.fill("Black")
                    SCREEN.blit(
                        pygame.transform.scale(
                            BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT)
                        ),
                        (0, 0),
                    )

                    base_group.draw(SCREEN)
                    base_group.update()

                    player_floating_group.draw(SCREEN)
                    player_floating_group.update()

                    use_text.draw_text_with_outline(
                        BODY,
                        "Press space to play",
                        center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4),
                    )
                case _:
                    raise NotImplementedError(state)

            # Updating display.
            pygame.display.update()
            pygame.display.flip()

            # Setting up tickrate for our game.
            CLOCK.tick(FPS)

        pygame.quit()
        sys.exit(0)


if __name__ == "__main__":
    FlappyBird().main()
