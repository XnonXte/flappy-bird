import pygame
from config import SCREEN


def draw_text_with_outline(
    font: pygame.font.Font,
    text: str,
    color: tuple = (255, 255, 255),
    outline_color: tuple = (0, 0, 0),
    outline_thickness: int = 2,
    **rectkwargs
):
    """Function to draw text with outline, this function is written by Phind."""
    # Render the text in the outline color
    outline_surface = font.render(text, True, outline_color).convert_alpha()
    outline_size = outline_surface.get_size()

    # Create a surface larger than the text surface to accommodate the outline
    text_surface = pygame.Surface(
        (
            outline_size[0] + outline_thickness * 2,
            outline_size[1] + outline_thickness * 2,
        ),
        pygame.SRCALPHA,
    )
    text_rect = text_surface.get_rect()

    # Blit the outline surface multiple times on the text surface, shifted by the outline thickness
    for dx in range(-outline_thickness, outline_thickness + 1):
        for dy in range(-outline_thickness, outline_thickness + 1):
            if dx != 0 or dy != 0:  # Skip the center to avoid overwriting the text
                text_surface.blit(
                    outline_surface, (dx + outline_thickness, dy + outline_thickness)
                )

    # Render the text with the desired color and convert the surface to a per-pixel alpha format
    inner_text = font.render(text, True, color).convert_alpha()
    text_surface.blit(inner_text, inner_text.get_rect(center=text_rect.center))
    text_rect = text_surface.get_rect(**rectkwargs)

    # Blit the final text surface onto the screen
    SCREEN.blit(text_surface, text_rect)
