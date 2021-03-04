import config as c
import logging


logger = logging.getLogger(__name__)


class Card:
    def __init__(self, fruit, rect):
        self.fruit = fruit
        self.rect = rect
        self.is_matched = False
        self.is_selected = False
        self.is_showing = False

    def __eq__(self, other):
        return self.fruit == other.fruit

    def draw(self, surface):
        if self.is_matched or self.is_showing or self.is_selected:
            surface.fill(c.WHITE_COLOR, self.rect)
            surface.blit(self.fruit.image, self.rect)
        else:
            surface.fill(c.BLUE_COLOR, self.rect)

    def on_click(self, pos):
        if self.is_matched:
            return

        if self.rect.collidepoint(pos) and not self.is_selected:
            self.is_selected = True
