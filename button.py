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
        w,
        h,
        text_func,
        font,
        click_callback=lambda x: None,
        centre_x=False,
        background_color=c.BUTTON_COLOR,
        text_color=c.BLUE_COLOR,
    ):
        self.bounds = pygame.Rect(x, y, w, h)
        self.click_callback = click_callback
        self.text = Text(x, y, text_func, font, centre_x)
        self.background_color = background_color
        self.text_color = text_color

    def draw(self, surface):
        pygame.draw.rect(surface, self.background_color, self.bounds)
        self.text.draw(surface)

    def on_click(self, pos):
        if self.bounds.collidepoint(pos):
            self.click_callback()
