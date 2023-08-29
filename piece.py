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

  def my_king(self) -> any:
    return self.board.get_piece("K")[0] if self.color == WHITE else self.board.get_piece("k")[0]


class King(Piece):
  def __init__(self, color: int, pos: tuple[int, int], board: Board) -> None:
    super().__init__(color, pos, board)
    self.offsets = [(1, 0), (0, 1), (-1, 0), (0, -1),
                    (1, 1), (1, -1), (-1, 1), (-1, -1)]
    self.checks = []
    self.pins = {}

  def __str__(self) -> str:
    return "K" if self.get_color() == WHITE else "k"

  def get_checks(self) -> list[tuple[int, int]]:
    return self.checks

  def get_pins(self) -> dict:
    return self.pins

  def checks_and_pins(self) -> None:
    """
    >>> board = Board(5, 4)
    >>> R = Rook(WHITE, (0, 0), board)
    >>> k = King(BLACK, (4, 0), board)
    >>> n = Knight(BLACK, (3, 2), board)
    >>> board.add_piece_place_piece((0, 0), R)
    >>> board.add_piece_place_piece((4, 0), k)
    >>> board.add_piece_place_piece((3, 2), n)
    >>> k.checks_and_pins()
    >>> len(k.checks) == 2
    True
    """
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
          possible_pos = (possible_pos[0] + offset[0], possible_pos[1] + offset[1])

        # If king's teammate is blocking him
        elif piece_at_cell.get_color() == self.get_color():

          if offset[1] == 0:
            shields.append((piece_at_cell, "v"))
          elif offset[0] == 0:
            shields.append((piece_at_cell, "h"))
          else:
            shields.append((piece_at_cell, "d"))

          if len(shields) > 1:
            break
          else:
            possible_pos = (possible_pos[0] + offset[0], possible_pos[1] + offset[1])

        # Checking for horizontal/vertical (ex. (1 * 0) => 0)) and not same color
        elif (offset[0] * offset[1] == 0) and (isinstance(piece_at_cell, Rook) or isinstance(piece_at_cell, Queen)):
          if len(shields) == 1:
            pins[shields[0][0]] = (shields[0][1], piece_at_cell.get_pos())
          else:
            checks.append(piece_at_cell)
          break

        # Checking for diagonal (ex. (1 * 1) => 1)) and not same color
        elif (offset[0] * offset[1] != 0) and (isinstance(piece_at_cell, Bishop) or isinstance(piece_at_cell, Queen)):
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
    """
    Doctest:
    >>> board = Board(5, 4)
    >>> R = Rook(WHITE, (0, 0), board)
    >>> k = King(BLACK, (4, 1), board)
    >>> board.place((0, 0), R)
    >>> board.place((4, 1), k)
    >>> k.is_pos_attacked((4, 0))
    True
    >>> board = Board(5, 4)
    >>> k = King(BLACK, (4, 1), board)
    >>> P = Pawn(WHITE, (3, 1), board)
    >>> board.place((4, 1), k)
    >>> board.place((3, 1), P)
    >>> k.is_pos_attacked((4, 0))
    True
    """
    for offset in self.offsets:
      next_pos = (pos[0] + offset[0], pos[1] + offset[1])
      while self.board.is_valid_pos(next_pos):
        piece = self.board.lookup(next_pos)
        if piece is None: next_pos = (next_pos[0] + offset[0], next_pos[1] + offset[1])
        elif piece.get_color() == self.get_color(): break
        else:
          if offset[0] * offset[1] == 0 and (isinstance(piece, Rook) or isinstance(piece, Queen) or isinstance(piece, King)):
            return True
          elif abs(offset[0] * offset[1]) == 1 and (isinstance(piece, Bishop) or isinstance(piece, Queen)) or isinstance(piece, King):
            return True
          elif offset[0] * offset[1] == 1 and isinstance(piece, Bishop) or isinstance(piece, Queen):
            return True
          elif abs(offset[0] * offset[1] == 1) and (next_pos[0] - offset[0], next_pos[1] - offset[0]) == pos:
            return True
          else:
            break

    for offset in Knight.MOVE_OFFSETS:
      next_pos = (pos[0] + offset[0], pos[1] + offset[1])
      if self.board.is_valid_pos(next_pos):
        piece = self.board.lookup(next_pos)
      else:
        continue
      if piece is not None and isinstance(piece, Knight):
        return True

    return False

  def moves(self) -> list[tuple[int, int]]:
    """
    Doctest:
    >>> board = Board(5, 4)
    >>> R = Rook(WHITE, (0, 0), board)
    >>> k = King(BLACK, (4, 1), board)
    >>> board.place((0, 0), R)
    >>> board.place((4, 1), k)
    >>> set(k.moves()) == {(4, 2), (3, 2), (3, 1)}
    True

    """
    curr_pos = self.get_pos()
    moves = []
    opponent_color = BLACK if self.get_color() == WHITE else WHITE
    for offset in self.offsets:
      possible_pos = (curr_pos[0] + offset[0], curr_pos[1] + offset[1])
      if not self.board.is_valid_pos(possible_pos):
        continue
      elif self.board.lookup(possible_pos) is None:
        if not self.is_pos_attacked(possible_pos):
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
    """
    >>> board = Board(5, 4)
    >>> R = Rook(WHITE, (0, 1), board)
    >>> k = King(BLACK, (4, 1), board)
    >>> n = Knight(BLACK, (4, 2), board)
    >>> board.add_piece_place_piece((0, 1), R)
    >>> board.add_piece_place_piece((4, 1), k)
    >>> board.add_piece_place_piece((3, 1), n)
    >>> k.checks_and_pins()
    >>> n.moves()
    []

    >>> board = Board(5, 4)
    >>> R = Rook(WHITE, (0, 1), board)
    >>> k = King(BLACK, (1, 3), board)
    >>> n = Knight(BLACK, (4, 2), board)
    >>> board.add_piece_place_piece((0, 1), R)
    >>> board.add_piece_place_piece((4, 1), k)
    >>> board.add_piece_place_piece((1, 3), n)
    >>> k.checks_and_pins()
    >>> set(n.moves()) == {(0, 1), (2, 1)}
    True

    """
    my_king = self.my_king()
    if my_king is None:
      return []
    checks = my_king.get_checks()
    pins = my_king.get_pins()
    # Knight can never move if pinned

    if len(checks) == 2 or self in pins:
      return []
    elif len(checks) == 1:
      possible_moves = self.possible_moves()
      king_pos = my_king.get_pos()
      check_pos = checks[0].get_pos()
      check_blocks = check_line(king_pos, check_pos)
      moves = []
      for move in possible_moves:
        if move in check_blocks:
          moves.append(move)
      return moves
    else:
      return self.possible_moves()


class Pawn(Piece):
  def __init__(self, color: int, pos: tuple[int, int], board: Board) -> None:
    super().__init__(color, pos, board)

  def __str__(self) -> str:
    return "P" if self.get_color() == WHITE else "p"

  def possible_moves(self):
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

  def moves(self):
    """
    pin test

    >>> board = Board(5, 4)
    >>> R = Rook(WHITE, (4, 1), board)
    >>> k = King(BLACK, (0, 1), board)
    >>> p = Pawn(BLACK, (1, 1), board)
    >>> board.add_piece_place_piece((4, 1), R)
    >>> board.add_piece_place_piece((0, 1), k)
    >>> board.add_piece_place_piece((1, 1), p)
    >>> k.checks_and_pins()
    >>> set(p.moves()) == {(2, 1)}
    True

    >>> board = Board(5, 4)
    >>> R = Rook(WHITE, (1, 1), board)
    >>> k = King(BLACK, (0, 1), board)
    >>> p = Pawn(BLACK, (0, 0), board)
    >>> board.add_piece_place_piece((1, 1), R)
    >>> board.add_piece_place_piece((0, 1), k)
    >>> board.add_piece_place_piece((0, 0), p)
    >>> k.checks_and_pins()
    >>> p.moves() == [(1, 1)]
    True

    """
    my_king = self.my_king()
    if my_king == None:
      return []
    checks = my_king.get_checks()
    pins = my_king.get_pins()

    if len(checks) == 2 or (len(checks) == 1 and self in pins):
      return []
    elif len(checks) == 1:
      possible_moves = self.possible_moves()
      king_pos = my_king.get_pos()
      check_pos = checks[0].get_pos()

      check_blocks = check_line(king_pos, check_pos)
      return [move for move in possible_moves if move in check_blocks]

    elif self in pins:
      if pins[self][0] == "h":
        return []

      elif pins[self][0] == "v":

        curr_pos = self.get_pos()
        forward_d = -1 if self.get_color() == WHITE else 1

        # Forward
        new_pos = (curr_pos[0] + forward_d, curr_pos[1])
        if self.board.is_valid_pos(new_pos) and self.board.is_empty_pos(new_pos):
          return [new_pos]

      # Check if can capture diagonal pinner
      else:
        possible_moves = self.possible_moves()
        pin_moves = pin_line(self.get_pos(), pins[self][1])
        return [move for move in possible_moves if move in pin_moves]

    else:
      return self.possible_moves()


class SlidingPiece(Piece):
  def __init__(self, color: int, pos: tuple[int, int], board: Board):
    super().__init__(color, pos, board)

  def possible_moves(self, sliding=True):
    return super().possible_moves(sliding)

  def moves(self) -> list[tuple[int, int]]:
    """
    >>> board = Board(5, 4)
    >>> R = Rook(WHITE, (0, 3), board)
    >>> k = King(BLACK, (0, 1), board)
    >>> b = Bishop(BLACK, (0, 2), board)
    >>> board.add_piece_place_piece((0, 3), R)
    >>> board.add_piece_place_piece((0, 1), k)
    >>> board.add_piece_place_piece((0, 2), b)
    >>> k.checks_and_pins()
    >>> b.moves() == []
    True

    >>> board = Board(5, 4)
    >>> R = Rook(WHITE, (0, 3), board)
    >>> k = King(BLACK, (0, 1), board)
    >>> b = Bishop(BLACK, (2, 1), board)
    >>> board.add_piece_place_piece((0, 3), R)
    >>> board.add_piece_place_piece((0, 1), k)
    >>> board.add_piece_place_piece((2, 1), b)
    >>> k.checks_and_pins()
    >>> b.moves() == [(0, 3)]
    True

    """
    my_king = self.my_king()
    if my_king is None:
      return []
    checks = my_king.get_checks()
    pins = my_king.get_pins()

    if len(checks) == 2 or (len(checks) == 1 and self in pins):
      return []
    elif len(checks) == 1:
      possible_moves = self.possible_moves()
      king_pos = my_king.get_pos()
      check_pos = checks[0].get_pos()
      check_blocks = check_line(king_pos, check_pos)
      moves = [move for move in possible_moves if move in check_blocks]
      return moves
    elif self in pins:
      curr_pos = self.get_pos()
      pinner_pos = pins[self][1]

      if len(self.offsets) == 8:
        return pin_line(curr_pos, pinner_pos)

      else:
        piece_type = "vh" if self.offsets[0][0] * \
            self.offsets[0][1] == 0 else "d"
        pin_type = pins[self][0]

        if ((pin_type == "v" or pin_type == "h") and piece_type == "vh") or \
                (pin_type == "d" and piece_type == "d"):
          return pin_line(curr_pos, pinner_pos)
        else:
          return []

    else:
      return self.possible_moves()


class Queen(SlidingPiece):

  def __init__(self, color: int, pos: tuple[int, int], board: Board):
    super().__init__(color, pos, board)
    self.offsets = [(1, 0), (0, 1), (-1, 0), (0, -1),
                    (1, 1), (1, -1), (-1, 1), (-1, -1)]

  def __str__(self) -> str:
    return "Q" if self.get_color() == WHITE else "q"


class Rook(SlidingPiece):
  MOVE_OFFSETS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

  def __init__(self, color: int, pos: tuple[int, int], board: Board) -> None:
    super().__init__(color, pos, board)
    self.offsets = [(1, 0), (0, 1), (-1, 0), (0, -1)]

  def __str__(self) -> str:
    return "R" if self.get_color() == WHITE else "r"


class Bishop(SlidingPiece):
  MOVE_OFFSETS = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

  def __init__(self, color: int, pos: tuple[int, int], board: Board) -> None:
    super().__init__(color, pos, board)
    self.offsets = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

  def __str__(self) -> str:
    return "B" if self.get_color() == WHITE else "b"


def check_line(king_pos: tuple[int, int], checker_pos: tuple[int, int]) -> list[tuple[int, int]]:
  vector = (checker_pos[0] - king_pos[0], checker_pos[1] - king_pos[1])
  if vector[0] != 0:
    vector = (vector[0] // abs(vector[0]), vector[1])
  if vector[1] != 0:
    vector = (vector[0], vector[1] // abs(vector[1]))

  pin_line = []

  curr_pos = king_pos

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



