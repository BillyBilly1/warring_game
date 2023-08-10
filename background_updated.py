from __future__ import annotations
import pygame
from typing import Optional
from constant import *
from characters import *

class ChessSquare():
    def __init__(self, topleft: tuple[int, int]):
        self.length = SQUARE_WIDTH
        self.border = 1
        self.topleft = topleft
        self.rect = pygame.Rect(self.topleft, (self.length, self.length))

        self.length_speed = 20  # 20 pixel per second # todo: 要还是不要
    def zoom_by_factor(self, zoom_scale: float):
        """Update self.rect.size. self.length指的是initial size，不受改变。"""
        self.rect.size = (round(self.length * zoom_scale), round(self.length * zoom_scale))

class ChessBoard(pygame.sprite.Sprite):
    size: dict[str, int]
    topleft: tuple[int, int]
    square_length: int
    grid: list[list[ChessSquare]]
    def __init__(self, group: pygame.sprite.Group, row: int, col: int):
        super().__init__(group)
        self.size = {'row': row, 'col': col}
        self.topleft = (20, 20)  # 在display surface上的初始点
        self.square_length = SQUARE_WIDTH
        self.grid = self._create_grid(row, col)

    def _create_grid(self, row, col) -> list[list[ChessSquare]]:
        grid = []
        for r in range(row):
            line = []
            for c in range(col):
                pos = (self.topleft[0] + c * self.square_length, self.topleft[1] + r * self.square_length)
                line.append(ChessSquare(pos))
            grid.append(line)
        return grid

    def zoom(self, zoom_scale: float):
        """Zoom in/out ChessSquare in self.grid first, update each Square's topleft"""
        for line in self.grid:
            for square in line:
                square.zoom_by_factor(zoom_scale)
        # update each Square's topleft
        square_length = self.square_length * zoom_scale
        for r in range(self.size['row']):
            for c in range(self.size['col']):
                pos = (self.topleft[0] + round(c * square_length),\
                       self.topleft[1] + round(r * square_length))
                self.grid[r][c].rect.topleft = pos

    def draw(self, screen):
        for i in self.grid:
            for square in i:
                pygame.draw.rect(screen, 'Red', square.rect, round(square.border))


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        """
            - zoom_scale: wont be cleared after each update()/draw()
            - offset: cleared everytime after update()/draw()
        """
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        self.keyboard_speed = KEYBOARD_CONTROL_SPEED
        self.zoom_scale = 1.0
        self.zoom_speed = 1  # zoom by 1倍 per second


    def update(self, dt: float):
        """According to keyboard changes, adjust self.zoom_scale and self.offset"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.offset.y = self.keyboard_speed * dt
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.offset.y = -self.keyboard_speed * dt
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.offset.x = -self.keyboard_speed * dt
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.offset.x = self.keyboard_speed * dt
        # zoom
        if keys[pygame.K_q]:  # zoom out
            self.zoom_scale -= self.zoom_speed * dt
        if keys[pygame.K_e]:  # zoom in
            self.zoom_scale += self.zoom_speed * dt

    def draw(self, screen: pygame.Surface) -> None:
        for sprite in self.sprites():
            sprite.zoom(self.zoom_scale)
            sprite.topleft += self.offset  # ChessBoard没有Rect，只有topleft
            sprite.draw(screen)
        self.offset = pygame.math.Vector2()
