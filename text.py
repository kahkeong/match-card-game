import config as c


class Text:
    def __init__(
        self,
        x,
        y,
        text_func,
        font,
        centre=False,
        color=c.BLACK_COLOR,
    ):
        self.centre = centre
        self.pos = x, y
        self.text_func = text_func
        self.color = color
        self.font = font

    def draw(self, surface):
        if self.centre:
            center = surface.get_rect().center
            text_surface = self.font.render(self.text_func(), True, self.color)
            # relative to middle of screen
            pos = text_surface.get_rect(center=center)
            pos.x += self.pos[0]
            pos.y += self.pos[1]
            surface.blit(text_surface, pos)
        else:
            text_surface = self.font.render(self.text_func(), True, self.color)
            surface.blit(text_surface, self.pos)

    def rect(self, surface):
        text_surface = self.font.render(self.text_func(), True, self.color)
        if self.centre:
            center = surface.get_rect().center
            # relative to middle of screen
            pos = text_surface.get_rect(center=center)
        else:
            pos = text_surface.get_rect()
        pos.x += self.pos[0]
        pos.y += self.pos[1]
        return pos
