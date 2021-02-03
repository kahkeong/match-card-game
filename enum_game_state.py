from enum import Enum


class GameState(Enum):
    MAIN_MENU = 1
    IN_PROGRESS = 2
    PAUSED = 3
    END = 4