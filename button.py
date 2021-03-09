import logging
import pygame
import config as c
from text import Text

logger = logging.getLogger(__name__)


class Button:
    def __init__(
        self,
        x,
        y,
        text_func,
        font,
        click_callback=lambda x: None,
        centre=False,
        background_color=c.BUTTON_COLOR,
        text_color=c.BLACK_COLOR,
    ):
        self.click_callback = click_callback
        self.text = Text(x, y, text_func, font, centre, text_color)
        self.background_color = background_color

    def draw(self, surface):
        pygame.draw.rect(surface, self.background_color, self.text.rect(surface))
        self.text.draw(surface)

    def on_click(self, surface, pos):
        if self.text.rect(surface).collidepoint(pos):
            self.click_callback()
