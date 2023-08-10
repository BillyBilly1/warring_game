import sys
import pygame
import time
pygame.init()

class Square():
    def __init__(self, pos: tuple[int, int]):
        self.length = 50.0
        self.border = 2.0
        self.topleft = pos
        self.rect = pygame.Rect(self.topleft, (self.length, self.length))

        self.length_speed = 20
        self.border_speed = 2

    def zoom_in_by_speed(self, dt: float):
        """Update self.length by speed, then update self.rect."""
        self.length += self.length_speed * dt
        self.border += self.border_speed * dt
        self.rect.size = (round(self.length), round(self.length))

    def zoom_by_factor(self, zoom_scale: float):
        """Update self.zoom_scale"""
        self.rect.size = (round(self.length * zoom_scale), round(self.length * zoom_scale))

class Board():
    topleft: tuple[int, int]
    def __init__(self, row: int, col: int):
        """Create a board wiz """
        self.size = {'row': row, 'col': col}
        self.topleft = (20, 20)
        self.square_length = 50
        self.grid = self._create_grid(row, col)

        self.zoom_scale = 1.0
        self.zoom_scale_speed = 1

    def _create_grid(self, row, col) -> list[list[Square]]:
        grid = []
        for r in range(row):
            line = []
            for c in range(col):
                pos = (self.topleft[0] + c * self.square_length, self.topleft[1] + r * self.square_length)
                line.append(Square(pos))
            grid.append(line)
        return grid

    def zoom_in(self, dt: float):
        """Update self.grid"""
        self.zoom_scale += self.zoom_scale_speed * dt
        # 放大每一个Square
        for i in self.grid:
            for square in i:
                square.zoom_by_factor(self.zoom_scale)
        # 更新每一个Square的位置
        square_length = self.square_length * self.zoom_scale
        for r in range(self.size['row']):
            for c in range(self.size['col']):
                pos = (self.topleft[0] + round(c * square_length), \
                       self.topleft[1] + round(r * square_length))
                self.grid[r][c].rect.topleft = pos
    def zoom_out(self, dt: float):
        self.zoom_scale -= self.zoom_scale_speed * dt
        # 放大每一个Square
        for i in self.grid:
            for square in i:
                square.zoom_by_factor(self.zoom_scale)
        # 更新每一个Square的位置
        square_length = self.square_length * self.zoom_scale
        for r in range(self.size['row']):
            for c in range(self.size['col']):
                pos = (self.topleft[0] + round(c * square_length), \
                       self.topleft[1] + round(r * square_length))
                self.grid[r][c].rect.topleft = pos


    def draw(self, screen: pygame.Surface):
        for i in self.grid:
            for square in i:
                pygame.draw.rect(screen, 'Red', square.rect, round(square.border))

# intialize a screen

screen = pygame.display.set_mode((400, 300))
clock = pygame.time.Clock()
b1 = Board(3, 2)
prev_time = time.time()
while True:
    dt = time.time() - prev_time
    prev_time = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_q:  # zoom in
        #         s1.zoom_in(dt)

    screen.fill('White')
    if pygame.key.get_pressed()[pygame.K_q] is True:
        b1.zoom_in(dt)
    elif pygame.key.get_pressed()[pygame.K_e] is True:
        b1.zoom_out(dt)

    b1.draw(screen)
    pygame.display.update()
    clock.tick(25)


# draw a chess square

# scale it
