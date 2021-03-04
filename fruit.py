import pygame
from dataclasses import dataclass


@dataclass
class Fruit:
    name: str
    image: pygame.Surface
