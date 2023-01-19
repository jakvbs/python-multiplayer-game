import pygame as pg

from constants import BG_COLOR


class Canvas:

    def __init__(self, w: int, h: int, name: str = "None"):
        self.width = w
        self.height = h
        self.screen = pg.display.set_mode((w, h))
        pg.display.set_caption(name)

    @staticmethod
    def update() -> None:
        pg.display.update()

    def draw_text(self, text: str, size: int, x: int, y: int) -> None:
        pg.font.init()
        font = pg.font.SysFont("comicsans", size)
        render = font.render(text, True, (0, 0, 0))

        self.screen.blit(render, (x, y))

    def get_canvas(self) -> pg.surface.Surface:
        return self.screen

    def draw_background(self) -> None:
        self.screen.fill(BG_COLOR)
