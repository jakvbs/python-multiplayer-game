from abc import ABC, abstractmethod
import pygame as pg

from constants import CIRCLE_SIZE, GAP, LINE_WIDTH, HEIGHT, BOTTOM_PANEL_HEIGHT, WIDTH, BOARD_SIZE, CIRCLE_COLOR, \
    CIRCLE_BORDER


class Line(ABC):

    def __init__(self, row: int, col: int, color: tuple[int, int, int]):
        self.row = row
        self.col = col
        self.color = color

    @abstractmethod
    def draw(self, screen: pg.surface.Surface) -> None:
        pass


class VerticalLine(Line):

    def __init__(self, col: int, color: tuple[int, int, int]):
        super().__init__(0, col, color)

    def draw(self, screen: pg.surface.Surface) -> None:
        posX = (CIRCLE_SIZE + GAP) // 2 + self.col * \
               (CIRCLE_SIZE + GAP) - LINE_WIDTH // 2
        pg.draw.line(screen, self.color, (posX, 5),
                     (posX, HEIGHT - BOTTOM_PANEL_HEIGHT - 5), LINE_WIDTH)


class HorizontalLine(Line):

    def __init__(self, row: int, color: tuple[int, int, int]):
        super().__init__(row, 0, color)

    def draw(self, screen: pg.surface.Surface) -> None:
        posY = (CIRCLE_SIZE + GAP) // 2 + self.row * \
               (CIRCLE_SIZE + GAP) - LINE_WIDTH // 2

        pg.draw.line(screen, self.color, (5, posY),
                     (WIDTH - 5, posY), LINE_WIDTH)


class AscDiagonalLine(Line):

    def __init__(self, row: int, col: int, color: tuple[int, int, int]):
        super().__init__(row, col, color)

    def draw(self, screen: pg.surface.Surface) -> None:
        start_x = self.col * (CIRCLE_SIZE + GAP)
        start_y = (self.row + 1) * (CIRCLE_SIZE + GAP)
        end_x = start_y
        end_y = start_x

        pg.draw.line(screen, self.color, (start_x + 15, start_y - 15),
                     (end_x - 15, end_y + 15), LINE_WIDTH)


class DescDiagonalLine(Line):

    def __init__(self, row: int, col: int, color: tuple[int, int, int]):
        super().__init__(row, col, color)

    def draw(self, screen: pg.surface.Surface) -> None:
        diag_length = BOARD_SIZE - max(self.row, self.col)
        start_x = self.col * (CIRCLE_SIZE + GAP)
        start_y = self.row * (CIRCLE_SIZE + GAP)
        end_x = start_x + diag_length * (CIRCLE_SIZE + GAP)
        end_y = start_y + diag_length * (CIRCLE_SIZE + GAP)

        pg.draw.line(screen, self.color, (start_x + 15, start_y + 15),
                     (end_x - 15, end_y - 15), LINE_WIDTH)


class Circle:

    def __init__(self, row: int, col: int, color: tuple[int, int, int]):
        self.row = row
        self.col = col
        self.color = color

    def draw(self, screen: pg.surface.Surface) -> None:
        x = (self.col + 1) * GAP + self.col * CIRCLE_SIZE + CIRCLE_SIZE // 2
        y = (self.row + 1) * GAP + self.row * CIRCLE_SIZE + CIRCLE_SIZE // 2
        pg.draw.circle(screen, self.color, (x, y), CIRCLE_SIZE // 2 - GAP)
        pg.draw.circle(screen, CIRCLE_COLOR, (x, y),
                       CIRCLE_SIZE // 2 - GAP, CIRCLE_BORDER)
