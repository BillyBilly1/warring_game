from __future__ import annotations
import pygame, time
from typing import Optional
from constant import *
from characters import *

class Chessboard(pygame.sprite.Sprite):
    size: tuple[int, int]
    grid: list[list[ChessSquare]]  # from topleft to bottomright
    square_size: int
    def __init__(self, group: pygame.sprite.Group, size: tuple[int, int]):
        """
        Instance Attributes:
            - size: size[0] is number of rows, size[1] is number of columns. (5, 10) is 5 row x 10 columns
        """
        super().__init__(group)
        self.size = size
        # create self.grid
        self.grid = []
        for row in range(self.size[0]):
            row_list = []
            for col in range(self.size[1]):
                row_list.append(ChessSquare())
            self.grid.append(row_list)
        # create self.image
        self.square_size = SQUARE_WIDTH
        self.image = pygame.Surface((self.square_size * self.size[1], self.square_size * self.size[0]))
        for row in range(self.size[0]):  # row is y
            for col in range(self.size[1]):  # column is x
                self.grid[row][col].draw(self.image, 1, (col * self.square_size, row * self.square_size))
        center = (WINDOW_WIDTH, WINDOW_HEIGHT)
        self.rect = self.image.get_rect(center=center)

    def is_clicked(self, mouse_pos) -> bool:
        return True
    def zoom(self, zoom_scale: float) -> None:
        """Redraw self.image. self.rect doesn't determine the size of this sprite"""
        # update square_size
        print(self.square_size, zoom_scale)
        self.square_size = int(self.square_size * zoom_scale)
        print(self.square_size)
        size = (self.size[1] * self.square_size, self.size[0] * self.square_size)
        self.image = pygame.Surface(size)
        for row in range(self.size[0]):
            for col in range(self.size[1]):
                self.grid[row][col].draw(self.image, zoom_scale, (col * self.square_size, row * self.square_size))




class ChessSquare():
    image: pygame.Surface
    rect: pygame.Rect
    character: Optional[CombatUnit]  # None: Nothing is placed here; CombatUnit: Something is placed on this square

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((SQUARE_WIDTH, SQUARE_WIDTH))
        self.image.fill('Orange')
        inner_sqaure = pygame.Surface((SQUARE_WIDTH * 0.9, SQUARE_WIDTH * 0.9))
        inner_sqaure.fill(SQUARE_COLOR)
        self.image.blit(inner_sqaure, (SQUARE_WIDTH * 0.1 // 2, SQUARE_WIDTH * 0.1 // 2))
        self.rect = self.image.get_rect()

    def draw(self, screen: pygame.Surface, zoom_scale: float, pos: tuple[int, int]) -> None:
        """Draw a chess square on the given screen by size scaled by zoom_scale, where self.rect.topleft is the given pos
        Precondition:
            - zoom_scale >= 0
            - 0 <= pos[0] <= screen.get_size()[0]
            - 0 <= pos[1] <= screen.get_size()[1]
        """
        self.image = pygame.transform.scale(self.image, (self.image.get_size()[0] * zoom_scale,
                                                         self.image.get_size()[1] * zoom_scale))
        self.rect = self.image.get_rect(topleft=pos)
        screen.blit(self.image, self.rect)

class CameraGroup(pygame.sprite.Group):
    display_screen: pygame.Surface
    offset: pygame.math.Vector2
    keyboard_speed: int
    zoom_scale: float
    internal_surf_size: tuple[int, int]
    internal_surf: pygame.Surface
    internal_rect: pygame.Rect
    internal_surf_vector: pygame.math.Vector2
    # internal_offset: pygame.math.Vector2

    def __init__(self):
        super().__init__()
        self.display_screen = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        self.keyboard_speed = KEYBOARD_CONTROL_SPEED

        # todo: internal surf缩小小于display surf时，会有种被框住了的感觉。目前解决方式是把internal surf的size弄得很大
        self.zoom_scale = 1
        # self.internal_surf_size = INTERNAL_SURF_SIZE
        # self.internal_surf = pygame.Surface(self.internal_surf_size)
        # fixme: center=self.display_surf // 2 or center=self.internal_surf // 2
        # self.internal_rect = self.internal_surf.get_rect(center=(self.internal_surf_size[0] // 2, self.internal_surf_size[1] // 2))
        # self.internal_surf_vector = pygame.math.Vector2(self.internal_surf_size)
    def update_offset_keyboard(self, dt: float):
        """self.offset changes according to the keyboard up/down/left/right"""
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
            self.zoom_scale -= 1 * dt
        if keys[pygame.K_e]:  # zoom in
            self.zoom_scale += 2 * dt

    def custom_draw(self) -> None:
        """Draw all the sprites in self by a movement against self.offset"""
        self.display_screen.fill('White')
        # todo: directly draw on self.display_screen
        for sprite in self.sprites():
            # draw sprite on self.display_screen
            sprite.rect.topleft += self.offset
            # print("before", sprite.image.get_size())
            print(self.zoom_scale)
            sprite.zoom(self.zoom_scale)
            # print(sprite.image.get_size())
            self.display_screen.blit(sprite.image, sprite.rect)
        # reset self.offset
        self.offset = pygame.math.Vector2()
        self.zoom_scale = 1
