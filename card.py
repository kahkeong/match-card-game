class Card:
    def __init__(self, name, rect):
        self.name = name
        self.is_matched = False
        self.rect = rect

    def __eq__(self, other):
        return self.name == other.anme
