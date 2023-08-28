from typing import *
from new_board import Board
WHITE, BLACK = 0, 1


class Piece:
  def __init__(self, color: int, pos: tuple[int, int], board: Board) -> None:
    self.color = color
    self.pos = pos
    self.board = board
    self.offsets = None

  def __str__(self) -> str:
    raise NotImplementedError(
        "The parent piece class has no piece type yet defined")

  def get_color(self) -> int:
    return self.color

  def get_pos(self) -> tuple[int, int]:
    return self.pos

  def set_pos(self, pos: tuple[int, int]) -> None:
    self.pos = pos

  def remove_pos(self) -> None:
    self.pos = None

  def attacking_squares(self) -> list[tuple[int, int]]:
    raise NotImplementedError

  def possible_moves(self, offsets, sliding=False):
    moves = []
    curr_pos = self.get_pos()
    board = self.board

    for offset in offsets:
      new_pos = (curr_pos[0] + offset[0], curr_pos[1] + offset[1])

      if sliding:
        while board.is_valid_pos(new_pos):
          if board.is_empty_pos(new_pos) or board.lookup(new_pos).get_color() != self.get_color():
            moves.append(new_pos)

          if not board.is_empty_pos(new_pos):
            break

          new_pos = (new_pos[0] + offset[0], new_pos[1] + offset[1])

      else:
        if board.is_valid_pos(new_pos) and \
                (board.is_empty_pos(new_pos) or board.lookup(new_pos).get_color() != self.get_color()):
          moves.append(new_pos)

    return moves

  def moves(self) -> list[tuple[int, int]]:
    raise NotImplementedError("The parent piece class can not move")

class King(Piece):
  def __init__(self, color: int, pos: tuple[int, int], board: Board) -> None:
    super().__init__(color, pos, board)
    self.offsets = [(1, 0), (0, 1), (-1, 0), (0, -1),
                  (1, 1), (1, -1), (-1, 1), (-1, -1)]

  def __str__(self) -> str:
    return "K" if self.color == 1 else "k"

  def __str__(self) -> str:
    return "K" if self.get_color() == WHITE else "k"

  def attacking_squares(self) -> list[tuple[int, int]]:
    attacking_squares = []

    for offset in self.offsets:
      pos = (self.pos[0] + offset[0], self.pos[1] + offset[1])

      if self.board.is_valid_pos(pos):
        attacking_squares.append(pos)

    return attacking_squares

  def possible_moves(self) -> list[tuple[int, int]]:
    return super().possible_moves(self.offsets)


class Knight(Piece):

  def __init__(self, color: int, pos: tuple[int, int], board: Board) -> None:
    super().__init__(color, pos, board)
    self.offsets = [(1, 2), (1, -2), (-1, 2), (-1, -2),
                  (2, 1), (2, -1), (-2, 1), (-2, -1)]

  def __str__(self) -> str:
    return "N" if self.color == 1 else "n"


class Pawn(Piece):
  def __init__(self, color: int, pos: tuple[int, int], board: Board) -> None:
    super().__init__(color, pos, board)
    self.offsets = [(1, 0), (1, -1), (1, 1)] if self.color == "B" else [(-1, 0), (-1, -1), (-1, 1)]

  def __str__(self) -> str:
    return "P" if self.color == 1 else "p"


class Sliding_Piece(Piece):
  def __init__(self, color: int, pos: tuple[int, int], board: Board):
    super().__init__(color, pos, board)


class Queen(Sliding_Piece):

  def __init__(self, color: int, pos: tuple[int, int], board: Board):
    super().__init__(color, pos, board)
    self.offsets = [(1, 0), (0, 1), (-1, 0), (0, -1),
                  (1, 1), (1, -1), (-1, 1), (-1, -1)]

  def __str__(self) -> str:
    return "Q" if self.color == 1 else "q"


class Rook(Sliding_Piece):
  MOVE_OFFSETS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

  def __init__(self, color: int, pos: tuple[int, int], board: Board) -> None:
    super().__init__(color, pos, board)
    self.offsets = [(1, 0), (0, 1), (-1, 0), (0, -1)]

  def __str__(self) -> str:
    return "R" if self.color == 1 else "r"


class Bishop(Sliding_Piece):
  MOVE_OFFSETS = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

  def __init__(self, color: int, pos: tuple[int, int], board: Board) -> None:
    super().__init__(color, pos, board)
    self.offsets = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

  def __str__(self) -> str:
    return "B" if self.color == 1 else "b"


