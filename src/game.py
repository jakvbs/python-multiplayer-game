from typing import Literal, Optional

import numpy as np
from numpy import ndarray

from constants import BOARD_SIZE, GAP, CIRCLE_SIZE, BG_COLOR, PLAYER_COLORS, LINE_COLORS
from elements import Line, VerticalLine, HorizontalLine, AscDiagonalLine, DescDiagonalLine, Circle


class Game:
    def __init__(self) -> None:
        self.board = np.zeros((BOARD_SIZE, BOARD_SIZE))
        self.current_player: Literal[1, 2] = 1
        self.winner_or_draw: Optional[Literal[1, 2, "DRAW"]] = None
        self.game_over = False
        self.p1_score = 0
        self.p2_score = 0
        self.ready: bool = False

        self.circles = [[Circle(row, col, BG_COLOR) for col in range(
            BOARD_SIZE)] for row in range(BOARD_SIZE)]
        self.lines: list[Line] = []

    def connected(self) -> bool:
        return self.ready

    def available_circle(self, row: int, col: int) -> bool:
        return bool(self.board[row][col] == 0)

    def is_board_full(self) -> ndarray | bool:
        return np.all(self.board != 0)

    def vertical_check(self, col: int) -> ndarray | bool:
        return np.all(self.board[:, col] != 0)

    def horizontal_check(self, row: int) -> ndarray | bool:
        return np.all(self.board[row, :] != 0)

    def asc_diagonal_check(self, row: int, col: int) -> bool:
        min_value = min(BOARD_SIZE - 1 - row, col)
        start_row = row + min_value
        start_col = col - min_value
        diag_length = start_row - start_col + 1

        for i in range(diag_length):
            if self.board[start_row - i][start_col + i] == 0:
                return False

        return True

    def desc_diagonal_check(self, row: int, col: int) -> bool:
        min_value = min(row, col)
        start_row = row - min_value
        start_col = col - min_value
        diag_length = BOARD_SIZE - max(start_row, start_col)

        for i in range(diag_length):
            if self.board[start_row + i][start_col + i] == 0:
                return False

        return True

    def mark_circle(self, row: int, col: int) -> None:
        self.board[row][col] = self.current_player
        self.circles[row][col].color = PLAYER_COLORS[self.current_player]

    def check_valid_move(self, x: int, y: int) -> bool:
        row, col = get_row_col_from_coords(x, y)

        if not is_click_in_circle(x, y):
            return False
        if not self.available_circle(row, col):
            return False

        return True

    def handle_click(self, x: int, y: int) -> None:
        row, col = get_row_col_from_coords(x, y)
        if not self.check_valid_move(x, y):
            return

        self.mark_circle(row, col)

        if self.vertical_check(col):
            if self.current_player == 1:
                self.p1_score += np.count_nonzero(
                    self.board[:, col] == 1)
            else:
                self.p2_score += np.count_nonzero(
                    self.board[:, col] == 2)
            color = LINE_COLORS[self.current_player]
            self.lines.append(VerticalLine(
                col, color))

        if self.horizontal_check(row):
            if self.current_player == 1:
                self.p1_score += np.count_nonzero(
                    self.board[row, :] == 1)
            else:
                self.p2_score += np.count_nonzero(
                    self.board[row, :] == 2)
            self.lines.append(HorizontalLine(
                row, LINE_COLORS[self.current_player]))

        if self.asc_diagonal_check(row, col):
            min_value = min(BOARD_SIZE - 1 - row, col)
            start_row = row + min_value
            start_col = col - min_value
            diag_length = start_row - start_col + 1

            player_points = 0
            for i in range(diag_length):
                if self.board[start_row - i][start_col + i] == self.current_player:
                    player_points += 1

            if self.current_player == 1:
                self.p1_score += player_points
            else:
                self.p2_score += player_points

            self.lines.append(
                AscDiagonalLine
                (start_row, start_col, LINE_COLORS[self.current_player]))

        if self.desc_diagonal_check(row, col):
            min_value = min(row, col)
            start_row = row - min_value
            start_col = col - min_value
            diag_length = BOARD_SIZE - max(start_row, start_col)

            player_points = 0
            for i in range(diag_length):
                if self.board[start_row + i][start_col + i] == self.current_player:
                    player_points += 1

            if self.current_player == 1:
                self.p1_score += player_points
            else:
                self.p2_score += player_points

            self.lines.append(
                DescDiagonalLine
                (start_row, start_col, LINE_COLORS[self.current_player]))

        self.current_player = 1 if self.current_player == 2 else 2
        if self.is_board_full():
            self.winner_or_draw = 1 if self.p1_score > self.p2_score \
                else 2 if self.p2_score > self.p1_score else "DRAW"
            self.game_over = True

    def reset(self) -> None:
        self.board = np.zeros((BOARD_SIZE, BOARD_SIZE))
        self.current_player = 1
        self.winner_or_draw = None
        self.game_over = False
        self.circles = [[Circle(row, col, BG_COLOR) for col
                         in range(BOARD_SIZE)] for row in range(BOARD_SIZE)]
        self.lines = []
        self.p1_score = 0
        self.p2_score = 0


def get_row_col_from_coords(x: int, y: int) -> tuple[int, int]:
    row = y // (CIRCLE_SIZE + GAP)
    col = x // (CIRCLE_SIZE + GAP)
    row = row if row < BOARD_SIZE else BOARD_SIZE - 1
    col = col if col < BOARD_SIZE else BOARD_SIZE - 1
    return row, col


def is_click_in_circle(x: int, y: int) -> bool:
    row, col = get_row_col_from_coords(x, y)
    circle_x = col * (CIRCLE_SIZE + GAP) + CIRCLE_SIZE // 2
    circle_y = row * (CIRCLE_SIZE + GAP) + CIRCLE_SIZE // 2
    return (x - circle_x) ** 2 + (y - circle_y) ** 2 <= (CIRCLE_SIZE // 2 - GAP) ** 2
