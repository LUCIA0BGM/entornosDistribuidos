# mesa.py

import pygame

class Mesa:
    def __init__(self, numero, x, y):
        self.numero = numero
        self.posicion = (x, y)
        self.width = 60
        self.height = 40

    def get_rect(self):
        return pygame.Rect(
            self.posicion[0] - self.width // 2,
            self.posicion[1] - self.height // 2,
            self.width,
            self.height
        )
