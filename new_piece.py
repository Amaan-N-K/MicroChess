from typing import *
from new_board import Board
WHITE, BLACK = 0, 1

class Piece:
  # 0 is White, 1 is Black
  def __init__(self, color: int, pos: List[int], board: Board) -> None:



class Piece:
  # 0 is White, 1 is Black
  def __init__(self, color: int, pos: tuple[int], board: Board) -> None:
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

  def get_pos(self) -> tuple[int]:
    return self.pos

  def set_pos(self, pos: tuple[int]) -> None:
    self.pos = pos

  def remove_pos(self) -> None:
    self.pos = None
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

  def moves(self) -> list[tuple[int]]:
    raise NotImplementedError("The parent piece class can not move")

class King(Piece):
  MOVE_OFFSETS = [(1, 0), (0, 1), (-1, 0), (0, -1),
                  (1, 1), (1, -1), (-1, 1), (-1, -1)]
  def __init__(self, color: int, pos: List[int], board: Board) -> None:
    super().__init__(color, pos, board)

  def __str__(self) -> str:
    return "K" if self.color == 1 else "k"
  def __init__(self, color: int, pos: tuple[int], board: Board) -> None:
    super().__init__(color, pos, board)

  def __str__(self) -> str:
    return "K" if self.get_color() == WHITE else "k"

  def possible_moves(self) -> list[tuple[int]]:
    return super().possible_moves(King.MOVE_OFFSETS)


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

  def __init__(self, color: int, pos: tuple[int], board: Board) -> None:
    super().__init__(color, pos, board)

  def __str__(self) -> str:
    return "N" if self.get_color() == WHITE else "n"

  def possible_moves(self) -> list[tuple[int]]:
    return super().possible_moves(Knight.MOVE_OFFSETS)


class Pawn(Piece):
  def __init__(self, color: int, pos: tuple[int], board: Board) -> None:
    super().__init__(color, pos, board)

  def __str__(self) -> str:
    return "P" if self.get_color() == WHITE else "p"

  def possible_moves(self) -> list[tuple[int]]:
    moves = []
    curr_pos = self.get_pos()
    forward_d = -1 if self.get_color() == WHITE else 1

    # Forward
    new_pos = (curr_pos[0] + forward_d, curr_pos[1])
    if self.board.is_valid_pos(new_pos) and self.board.is_empty_pos(new_pos):
      moves.append(new_pos)

    # Capture
    for horizontal_d in [1, -1]:
      new_pos = (curr_pos[0] + forward_d, curr_pos[1] + horizontal_d)
      if self.board.is_valid_pos(new_pos) and not self.board.is_empty_pos(new_pos) and self.board.lookup(new_pos).get_color() != self.get_color():
        moves.append(new_pos)

    return moves


class Queen(Piece):
  MOVE_OFFSETS = [(1, 0), (0, 1), (-1, 0), (0, -1),
                  (1, 1), (1, -1), (-1, 1), (-1, -1)]

  def __init__(self, color: int, pos: tuple[int], board: Board):
    super().__init__(color, pos, board)

  def __str__(self) -> str:
    return "Q" if self.get_color() == WHITE else "q"

  def possible_moves(self) -> list[tuple[int]]:
    return super().possible_moves(Queen.MOVE_OFFSETS, sliding=True)


class Rook(Piece):
  MOVE_OFFSETS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

  def __init__(self, color: int, pos: tuple[int], board: Board) -> None:
    super().__init__(color, pos, board)

  def __str__(self) -> str:
    return "R" if self.get_color() == WHITE else "r"

  def possible_moves(self) -> list[tuple[int]]:
    return super().possible_moves(Rook.MOVE_OFFSETS, sliding=True)


class Bishop(Piece):
  MOVE_OFFSETS = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

  def __init__(self, color: int, pos: tuple[int], board: Board) -> None:
    super().__init__(color, pos, board)

  def __str__(self) -> str:
    return "B" if self.get_color() == WHITE else "b"

  def possible_moves(self) -> list[tuple[int]]:
    return super().possible_moves(Bishop.MOVE_OFFSETS, sliding=True)
