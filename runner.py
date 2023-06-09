from constant import *
from background import *
import pygame, time, sys

class Game():
    screen: pygame.Surface
    clock: pygame.time.Clock
    all_sprites: pygame.sprite.Group

    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Warring Game')
        self.all_sprites = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.camera_sprites = CameraGroup()
        print('1111', self.camera_sprites.sprites())
        Chessboard(self.camera_sprites, (GRID_ROW, GRID_COL))
        print('2222', self.camera_sprites.sprites())

    def run(self):
        prev_time = time.time()
        while True:
            dt = time.time() - prev_time
            prev_time = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            # fixme: draw a temporary bg
            self.screen.fill('Cyan')
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.screen)
            self.camera_sprites.update_offset_keyboard(dt)
            self.camera_sprites.custom_draw()

            pygame.display.update()
            self.clock.tick(50)
