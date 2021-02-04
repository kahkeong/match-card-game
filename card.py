class Card:
    def __init__(self, name, rect):
        self.name = name
        self.is_matched = False
        self.rect = rect
        self.is_selected = False

    def __eq__(self, other):
        return self.name == other.anme
