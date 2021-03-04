import config as c


class Text:
    def __init__(
        self,
        x,
        y,
        text_func,
        font,
        color=c.BLUE_COLOR,
    ):
        self.pos = x, y
        self.text_func = text_func
        self.color = color
        self.font = font

    def draw(self, surface):
        text_surface = self.font.render(self.text_func(), True, self.color)
        surface.blit(text_surface, self.pos)

    def rect(self):
        text_surface = self.font.render(self.text_func(), True, self.color)
        return text_surface.get_rect()
