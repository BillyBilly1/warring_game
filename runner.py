from constant import *
from background_updated import *
import pygame, time, sys

class Game():
    screen: pygame.Surface
    clock: pygame.time.Clock
    all_sprites: pygame.sprite.Group
    camera_sprites: pygame.sprite.Group
    chessboard: ChessBoard

    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Warring Game')
        self.all_sprites = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.camera_sprites = CameraGroup()
        self.chessboard = ChessBoard(self.camera_sprites, GRID_ROW, GRID_COL)

    def run(self):
        prev_time = time.time()
        while True:
            dt = time.time() - prev_time
            prev_time = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    print('Mouse Position is', pygame.mouse.get_pos())
                    # print(self.chessboard.rect)
                    # print(self.chessboard.rect.collidepoint(pygame.mouse.get_pos()))
                    self.handle_button_up(event.pos)
            # fixme: draw a temporary bg
            self.screen.fill('White')
            # self.all_sprites.update(dt)
            # self.all_sprites.draw(self.screen)
            self.camera_sprites.update(dt)
            self.camera_sprites.draw(self.screen)

            pygame.display.update()
            self.clock.tick(50)

    # def handle_button_up(self, mouse_pos: tuple[int, int]):
    #     if self.chessboard.is_clicked(mouse_pos):
    #         # find each chess square is clicked,
    #         ...
