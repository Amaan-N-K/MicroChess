from typing import *
from new_board import Board


class Piece:
  # 0 is White, 1 is Black
  def __init__(self, color: int, pos: List[int], board: Board) -> None:
    self.color = color
    self.pos = pos
    self.board = board

  def __str__(self) -> str:
    raise NotImplementedError(
        "The parent piece class has no piece type yet defined")

  def get_color(self) -> int:
    return self.color

  def get_pos(self) -> List[int]:
    return self.pos

  def set_pos(self, pos: List[int]) -> None:
    self.pos = pos

  def remove_pos(self) -> None:
    self.pos = None


class King(Piece):
  MOVE_OFFSETS = [(1, 0), (0, 1), (-1, 0), (0, -1),
                  (1, 1), (1, -1), (-1, 1), (-1, -1)]

  def __init__(self, color: int, pos: List[int], board: Board) -> None:
    super().__init__(color, pos, board)

  def __str__(self) -> str:
    return "K" if self.color == 1 else "k"


class Knight(Piece):
  MOVE_OFFSETS = [(1, 2), (1, -2), (-1, 2), (-1, -2),
                  (2, 1), (2, -1), (-2, 1), (-2, -1)]

  def __init__(self, color: int, pos: List[int], board: Board) -> None:
    super().__init__(color, pos, board)

  def __str__(self) -> str:
    return "N" if self.color == 1 else "n"


class Pawn(Piece):
  def __init__(self, color: int, pos: List[int], board: Board) -> None:
    super().__init__(color, pos, board)

  def __str__(self) -> str:
    return "P" if self.color == 1 else "p"


class Sliding_Piece(Piece):
  def __init__(self, color: int, pos: List[int], board: Board):
    super().__init__(color, pos, board)


class Queen(Sliding_Piece):
  MOVE_OFFSETS = [(1, 0), (0, 1), (-1, 0), (0, -1),
                  (1, 1), (1, -1), (-1, 1), (-1, -1)]

  def __init__(self, color: int, pos: List[int], board: Board):
    super().__init__(color, pos, board)

  def __str__(self) -> str:
    return "Q" if self.color == 1 else "q"


class Rook(Sliding_Piece):
  MOVE_OFFSETS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

  def __init__(self, color: int, pos: List[int], board: Board) -> None:
    super().__init__(color, pos, board)

  def __str__(self) -> str:
    return "R" if self.color == 1 else "r"


class Bishop(Sliding_Piece):
  MOVE_OFFSETS = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

  def __init__(self, color: int, pos: List[int], board: Board) -> None:
    super().__init__(color, pos, board)

  def __str__(self) -> str:
    return "B" if self.color == 1 else "b"
