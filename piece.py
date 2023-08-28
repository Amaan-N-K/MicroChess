from typing import *
from board import Board
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

  def possible_moves(self, sliding=False):
    moves = []
    curr_pos = self.get_pos()
    board = self.board

    for offset in self.offsets:
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
    self.checks = []
    self.pins = {}

  def __str__(self) -> str:
    return "K" if self.get_color() == WHITE else "k"

  def checks_and_pins(self) -> None:
    curr_pos = self.get_pos()
    checks = []
    pins = {}

    # Checking for checks and pins by sliding pieces
    for offset in self.offsets:
      possible_pos = (curr_pos[0] + offset[0], curr_pos[1] + offset[1])
      shields = []
      while self.board.is_valid_pos(possible_pos):

        piece_at_cell = self.board.lookup(possible_pos)

        if piece_at_cell is None:
          possible_pos = (curr_pos[0] + offset[0], curr_pos[1] + offset[1])

        # If king's teammate is blocking him
        elif piece_at_cell.get_color() == self.get_color():

          if offset[0] == 0:
            shields.append((piece_at_cell, "v"))
          elif offset[1] == 0:
            shields.append((piece_at_cell, "h"))
          else:
            shields.append((piece_at_cell, "d"))

          if len(shields) > 1:
            break
          else:
            possible_pos[0] += offset[0]
            possible_pos[1] += offset[1]

        # Checking for horizontal/vertical (ex. (1 * 0) => 0)) and not same color
        elif (offset[0] * offset[1] == 0) and (isinstance(piece_at_cell, Rook) or isinstance(piece_at_cell, Rook)):
          if len(shields) == 1:
            pins[shields[0][0]] = (shields[0][1], piece_at_cell.get_pos())
          else:
            checks.append(piece_at_cell)
          break

        # Checking for diagonal (ex. (1 * 1) => 1)) and not same color
        elif (offset[0] * offset[1] != 0) and (isinstance(piece_at_cell, Bishop) or isinstance(piece_at_cell, Rook)):
          if len(shields) == 1:
            pins[shields[0][0]] = (shields[0][1], piece_at_cell.get_pos())
          else:
            checks.append(piece_at_cell)

          break

        # When enemy bishop is on horizontal/vertical line or rook on diagonal
        else:
          break

    # Checking for check by knight
    for offset in Knight.MOVE_OFFSETS:
      possible_pos = (curr_pos[0] + offset[0], curr_pos[1] + offset[1])

      if self.board.is_valid_pos(possible_pos) and isinstance(self.board.lookup(possible_pos), Knight):
        checks.append(self.board.lookup(possible_pos))


    # Checking for check by pawn
    vertical_direction = -1 if self.get_color() == "W" else 1

    # Capture moves (diagonal)
    diagonal_moves = [
      (curr_pos[0] + vertical_direction, curr_pos[1] - 1),
      (curr_pos[0] + vertical_direction, curr_pos[1] + 1)
    ]

    for move in diagonal_moves:
      if self.board.is_valid_pos(move):
        piece_at_cell = self.board.lookup(move)
        if piece_at_cell and piece_at_cell.get_color() != self.get_color() and piece_at_cell is Pawn:
          checks.append(piece_at_cell)

    if len(checks) > 2:
      raise ValueError("More than 2 pieces can not check at once")
    else:
      self.checks = checks
      self.pins = pins

  def is_pos_attacked(self, pos: tuple[int, int]) -> bool:

    for offset in self.offsets:
      next_pos = (pos[0] + offset[0], pos[1] + offset[1])
      while self.board.is_valid_pos(next_pos):
        piece = self.board.lookup(pos)
        if piece.get_color() == self.get_color():
          return False
        else:
          if offset[0] * offset[1] == 0 and isinstance(piece, Rook) or isinstance(piece, Queen):
            return True
          elif offset[0] * offset[1] == 1 and  isinstance(piece, Bishop) or isinstance(piece, Queen):
            return True
          elif offset[0] * offset[1] == 1 and (next_pos[0]-offset[0], next_pos[1]-offset[0]) == pos:
            return True
          else:
            next_pos = (next_pos[0] + offset[0], next_pos[1] + offset[1])

    for offset in Knight.MOVE_OFFSETS:
      next_pos = (pos[0] + offset[0], pos[1] + offset[1])
      if pos == next_pos:
        return True

    return False

  def moves(self) -> list[tuple[int, int]]:
    curr_pos = self.get_pos()
    moves = []
    opponent_color = BLACK if self.get_color() == WHITE else WHITE

    for offset in self.offsets:
      possible_pos = (curr_pos[0] + offset[0], curr_pos[1] + offset[1])
      if not self.board.is_valid_pos(possible_pos):
        continue
      elif self.board.lookup(possible_pos) is None and not self.is_pos_attacked(possible_pos):
        moves.append(possible_pos)
      elif self.board.lookup(possible_pos).get_color() == opponent_color and not self.is_pos_attacked(possible_pos):
        moves.append(possible_pos)

    return moves

class Knight(Piece):
  MOVE_OFFSETS = [(1, 2), (1, -2), (-1, 2), (-1, -2),
                  (2, 1), (2, -1), (-2, 1), (-2, -1)]

  def __init__(self, color: int, pos: tuple[int, int], board: Board) -> None:
    super().__init__(color, pos, board)
    self.offsets = Knight.MOVE_OFFSETS

  def __str__(self) -> str:
    return "N" if self.get_color() == WHITE else "n"

  def moves(self) -> list[tuple[int, int]]:
    my_king = self.board.get_piece("K") if self.color == WHITE else self.board.get_piece("k")
    if my_king is None:
      return []
    legal_moves = []
    my_king.checks_and_pins()
    checks = my_king.checks
    pins = my_king.pins

    if len(checks) == 2 or self in pins:
      return []
    elif len(checks) == 1:
      possible_moves = self.possible_moves()
      king_pos = my_king.get_pos()
      check_pos = checks[0].get_pos()

      check_blocks = check_line(king_pos, check_pos)

      for move in possible_moves:
        if move in check_blocks:
          legal_moves.append(move)

      return legal_moves
    else:
      return self.possible_moves()




class Pawn(Piece):
  def __init__(self, color: int, pos: tuple[int, int], board: Board) -> None:
    super().__init__(color, pos, board)

  def __str__(self) -> str:
    return "P" if self.get_color() == WHITE else "p"

  def possible_moves(self, sliding=False):
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


class Sliding_Piece(Piece):
  def __init__(self, color: int, pos: tuple[int, int], board: Board):
    super().__init__(color, pos, board)

  def possible_moves(self, sliding=True):
    return super().possible_moves(sliding)


class Queen(Sliding_Piece):

  def __init__(self, color: int, pos: tuple[int, int], board: Board):
    super().__init__(color, pos, board)
    self.offsets = [(1, 0), (0, 1), (-1, 0), (0, -1),
                    (1, 1), (1, -1), (-1, 1), (-1, -1)]

  def __str__(self) -> str:
    return "Q" if self.get_color() == WHITE else "q"


class Rook(Sliding_Piece):
  MOVE_OFFSETS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

  def __init__(self, color: int, pos: tuple[int, int], board: Board) -> None:
    super().__init__(color, pos, board)
    self.offsets = [(1, 0), (0, 1), (-1, 0), (0, -1)]

  def __str__(self) -> str:
    return "R" if self.get_color() == WHITE else "r"


class Bishop(Sliding_Piece):
  MOVE_OFFSETS = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

  def __init__(self, color: int, pos: tuple[int, int], board: Board) -> None:
    super().__init__(color, pos, board)
    self.offsets = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

  def __str__(self) -> str:
    return "B" if self.get_color() == WHITE else "b"


def check_line(king_pos: tuple[int, int], checker_pos: tuple[int, int]) -> list[tuple[int, int]]:
  vector = (checker_pos[0] - king_pos[0], checker_pos[1] - king_pos[1])
  if vector[0] != 0:
    vector = (vector[0] / abs(vector[0]), vector[1])
  if vector[1] != 0:
    vector = (vector[0], vector[1] / abs(vector[1]))

  pin_line = []

  curr_pos = checker_pos

  while curr_pos != checker_pos:
    curr_pos = (int(curr_pos[0] + vector[0]), int(curr_pos[1] + vector[1]))
    pin_line.append(curr_pos)

  return pin_line


def pin_line(pin_pos: tuple[int, int], pinner_pos: tuple[int, int]) -> list[tuple[int, int]]:
  vector = (pinner_pos[0] - pin_pos[0], pinner_pos[1] - pin_pos[1])

  if vector[0] != 0:
    vector = (vector[0] / abs(vector[0]), vector[1])
  if vector[1] != 0:
    vector = (vector[0], vector[1] / abs(vector[1]))

  pin_line = []

  curr_pos = pin_pos

  while curr_pos != pinner_pos:
    curr_pos = (int(curr_pos[0] + vector[0]), int(curr_pos[1] + vector[1]))
    pin_line.append(curr_pos)

  return pin_line
