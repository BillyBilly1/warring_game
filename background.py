from __future__ import annotations
import pygame, time
from typing import Optional
from constant import *

class Chessboard(pygame.sprite.Sprite):
    size: tuple[int, int]  # (5, 10) is 5 row x 10 columns
    grid: list[list[ChessSquare]]  # from topleft to bottomright
    def __init__(self, group: pygame.sprite.Group, size: tuple[int, int]):
        super().__init__(group)
        self.size = size
        self.topleft = (10, 10)
        # create self.grid
        self.grid = []
        for row in range(self.size[0]):
            row_list = []
            for col in range(self.size[1]):
                row_list.append(ChessSquare((col * SQUARE_WIDTH, row * SQUARE_WIDTH)))
            self.grid.append(row_list)
        # create self.image
        self.image = pygame.Surface((SQUARE_WIDTH * self.size[1], SQUARE_WIDTH * self.size[0]))
        for y in range(self.size[0]):
            for x in range(self.size[1]):
                self.grid[y][x].draw(self.image)
        self.rect = self.image.get_rect(topleft=self.topleft)


class ChessSquare(pygame.sprite.Sprite):
    image: pygame.Surface
    rect: pygame.Rect
    character: Optional[pygame.sprite]

    def __init__(self, pos: tuple[int, int]):
        super().__init__()
        self.image = pygame.Surface((SQUARE_WIDTH, SQUARE_WIDTH))
        self.image.fill('Orange')
        inner_sqaure = pygame.Surface((SQUARE_WIDTH * 0.9, SQUARE_WIDTH * 0.9))
        inner_sqaure.fill(SQUARE_COLOR)
        self.image.blit(inner_sqaure, (SQUARE_WIDTH * 0.1 // 2, SQUARE_WIDTH * 0.1 // 2))
        self.rect = self.image.get_rect(topleft=pos)

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self.rect)
