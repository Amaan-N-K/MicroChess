"""
Chess piece implementations
"""
from typing import List, Dict
from board import Board


class Piece:
  def __init__(self, color, pos):
    """Initialize piece 

    Args:
        color (str): "B" or "W" for black and white
        pos (List[int]): A 2-element list of [row, col], or None if not on game board
        piece_type (str): String representation of piece by FEN 
    """
    self.color = color
    self.pos = pos
    self.piece_type = None

  def __str__(self):
    if self.piece_type == None:
      raise NotImplementedError("This piece is not yet defined")
    return self.piece_type

  def set_pos(self, new_pos):
    self.pos = new_pos

  def remove_pos(self):
    self.pos = None

  def get_pos(self):
    return self.pos

  def get_color(self):
    return self.color

  def _check_line(self, king_pos: List, checker_pos: List):
    vector = [checker_pos[0] - king_pos[0], checker_pos[1] - king_pos[1]]
    vector_direction = [0, 0]
    if vector[0] != 0:
      vector_direction[0] = (vector[0]/abs(vector[0]))
    if vector[1] != 0:
      vector_direction[1] = (vector[1]/abs(vector[1]))

    check_line = set()

    curr_pos = king_pos

    while curr_pos != checker_pos:
      curr_pos[0] += vector_direction[0]
      curr_pos[1] += vector_direction[1]

      check_line.add(curr_pos)

    return check_line

  def _pin_line(self, pin_pos: List, pinner_pos: List):
    vector = [pinner_pos[0] - pin_pos[0], pinner_pos[1] - pin_pos[1]]
    vector_direction = [0, 0]
    if vector[0] != 0:
      vector_direction[0] = (vector[0]/abs(vector[0]))
    if vector[1] != 0:
      vector_direction[1] = (vector[1]/abs(vector[1]))

    pin_line = set()

    curr_pos = pin_pos

    while curr_pos != pinner_pos:
      curr_pos[0] += vector_direction[0]
      curr_pos[1] += vector_direction[1]

      pin_line.add(curr_pos)

    return pin_line

  def get_legal_moves(self, board: Board):
    """Return a list of legal piece moves

    Args:
        board (Board): Board object

    Raises:
        NotImplementedError: Method should be overrided by children classes
    """
    raise NotImplementedError


class King(Piece):
  MOVE_OFFSETS = [(1, 0), (0, 1), (-1, 0),  (0, -1),
                  (1, 1), (1, -1), (-1, 1), (-1, -1)]

  def __init__(self, color, pos):
    super().__init__(color, pos)
    self.piece_type = "K" if self.get_color() == "W" else "k"
    self.checks = []
    self.pins = {}

  def get_checks(self):
    return self.checks

  def get_pins(self):
    return self.pins

  def checks_and_pins(self, board: Board):
    """Returns all checks and pins for a king in a given board position

    Args:
        board (Board): Board Object

    Raises:
        ValueError: Raises ValueError if there are more than two checks at any given time

    Return:
        List[List[Piece]]: Returns a list that contains a list of checks and a list of pins
    """
    curr_pos = self.get_pos()
    checks = []
    pins = {}

    # Checking for checks and pins by sliding pieces
    for offset in King.MOVE_OFFSETS:
      possible_pos = [curr_pos[0] + offset[0], curr_pos[1] + offset[1]]

      while board.is_valid_location(possible_pos):
        shields = []
        piece_at_cell = board.get_cell_piece(possible_pos)

        if piece_at_cell == None:
          possible_pos[0] += offset[0]
          possible_pos[1] += offset[1]

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
        elif (offset[0] * offset[1] == 0) and (piece_at_cell is Rook or piece_at_cell is Queen):
          if len(shields) == 1:
            pins[shields[0][0]] = (shields[0][1], piece_at_cell.get_pos())
          else:
            checks.append(piece_at_cell)

          break

        # Checking for diagonal (ex. (1 * 1) => 1)) and not same color
        elif (offset[0] * offset[1] != 0) and (piece_at_cell is Bishop or piece_at_cell is Queen):
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
      possible_pos = [curr_pos[0] + offset[0], curr_pos[1] + offset[1]]

      if not board.is_valid_location(possible_pos):
        continue
      if board.get_cell_piece(possible_pos) is Knight:
        checks.append(board.get_cell_piece(possible_pos))

    # Checking for check by pawn
    vertical_direction = -1 if self.get_color() == "W" else 1

    # Capture moves (diagonal)
    diagonal_moves = [
        [curr_pos[0] + vertical_direction, curr_pos[1] - 1],
        [curr_pos[0] + vertical_direction, curr_pos[1] + 1]
    ]

    for move in diagonal_moves:
      if board.is_valid_location(move):
        piece_at_cell = board.get_cell_piece(move)
        if piece_at_cell and piece_at_cell.get_color() != self.get_color() and piece_at_cell is Pawn:
          checks.append(piece_at_cell)

    if len(checks) > 2:
      raise ValueError("More than 2 pieces can not check at once")
    else:
      self.checks = checks
      self.pins = pins

  def get_legal_moves(self, board: Board):
    curr_pos = self.get_pos()
    legal_moves = set()
    opponent_color = "B" if self.get_color() == "W" else "W"
    opponent_pieces = board.get_all_pieces_by_color(opponent_color)

    for offset in King.MOVE_OFFSETS:
      possible_pos = [curr_pos[0] + offset[0], curr_pos[1] + offset[1]]

      if (
          board.is_valid_location(possible_pos)
          and all(possible_pos not in p.get_legal_moves() for p in opponent_pieces)
          and board.get_cell_piece(possible_pos).get_color() != self.get_color()
      ):
        legal_moves.add(possible_pos)

    return legal_moves


class Knight(Piece):
  MOVE_OFFSETS = [(1, 2), (1, -2), (-1, 2), (-1, -2),
                  (2, 1), (2, -1), (-2, 1), (-2, -1)]

  def __init__(self, color, pos):
    super().__init__(color, pos)
    self.piece_type = "N" if self.get_color() == "W" else "n"

  def possible_legal_moves(self, board: Board):
    curr_pos = self.get_pos()
    legal_moves = set()

    for offset in Knight.MOVE_OFFSETS:
      possible_pos = [curr_pos[0] + offset[0], curr_pos[1] + offset[1]]

      if board.is_valid_location(possible_pos) and (
          board.is_cell_empty(possible_pos)
          or board.get_cell_piece(possible_pos).get_color() != self.get_color()
      ):
        legal_moves.add(possible_pos)

    return legal_moves

  def get_legal_moves(self, board: Board):
    legal_moves = set()
    my_pieces = board.get_all_pieces_by_color(self.get_color())
    my_king = [piece for piece in my_pieces if piece is King][0]
    checks = my_king.get_checks()
    pins = my_king.get_pins()

    if len(checks) == 2 or self in pins:
      return set()
    elif len(checks) == 1:
      possible_moves = self.possible_legal_moves(board)
      king_pos = my_king.get_pos()
      check_pos = checks[0].get_pos()

      check_blocks = self._check_line(king_pos, check_pos)

      for move in possible_moves:
        if move in check_blocks:
          legal_moves.add(move)

      return legal_moves
    else:
      return self.possible_legal_moves(board)


class Pawn(Piece):
  def __init__(self, color, pos):
    super().__init__(color, pos)
    self.piece_type = "P" if self.get_color() == "W" else "p"

  def possible_legal_moves(self, board: Board):

    legal_moves = set()

    vertical_direction = -1 if self.get_color() == "W" else 1
    curr_pos = self.get_pos()

    # One forward
    forward_move = [curr_pos[0] + vertical_direction, curr_pos[1]]
    if board.is_valid_location(forward_move) and board.is_cell_empty(forward_move):
      legal_moves.add(forward_move)

    # Capture moves (diagonal)
    diagonal_moves = [
        [curr_pos[0] + vertical_direction, curr_pos[1] - 1],
        [curr_pos[0] + vertical_direction, curr_pos[1] + 1]
    ]

    for move in diagonal_moves:
      if board.is_valid_location(move):
        piece_at_cell = board.get_cell_piece(move)
        if piece_at_cell and piece_at_cell.get_color() != self.get_color():
          legal_moves.add(move)

    return legal_moves

  def get_legal_moves(self, board: Board):
    legal_moves = set()
    my_pieces = board.get_all_pieces_by_color(self.get_color())
    my_king = [piece for piece in my_pieces if piece is King][0]
    checks = my_king.get_checks()
    pins = my_king.get_pins()

    if len(checks) == 2:
      return set()
    elif len(checks) == 1 and self in pins:
      return set()
    # A pawn can only move in a pin if the attacker is ahead of it vertically
    elif self in pins and pins[self][0] == "v":

      possible_moves = self.possible_legal_moves(board)
      direction = -1 if self.get_color() == "W" else 1
      possible_pos = [self.get_pos()[0] + direction, self.get_pos()[1]]
      if board.is_cell_empty(possible_moves):
        return {possible_pos}
      else:
        return set()
    elif self in pins:
      return set()
    elif len(checks) == 1:
      possible_moves = self.possible_legal_moves(board)
      king_pos = my_king.get_pos()
      check_pos = checks[0].get_pos()

      check_blocks = self._check_line(king_pos, check_pos)

      for move in possible_moves:
        if move in check_blocks:
          legal_moves.add(move)

      return legal_moves

    else:
      return self.possible_legal_moves()

class Sliding_Piece(Piece):
  def __init__(self, color, pos):
    super().__init__(color, pos)

  def possible_legal_moves(self, board: Board, move_offsets):
    curr_pos = self.get_pos()
    legal_moves = set()

    for offset in move_offsets:
      possible_pos = [curr_pos[0] + offset[0], curr_pos[1] + offset[1]]

      while board.is_valid_location(possible_pos):
        piece_at_cell = board.get_cell_piece(possible_pos)
        if piece_at_cell == None:
          legal_moves.add(possible_pos)
          possible_pos[0] += offset[0]
          possible_pos[1] += offset[1]
        elif piece_at_cell.get_color() != self.get_color():
          legal_moves.add(possible_pos)
          break
        else:
          break

    return legal_moves


class Queen(Sliding_Piece):
  MOVE_OFFSETS = [(1, 0), (0, 1), (-1, 0), (0, -1),
                  (1, 1), (1, -1), (-1, 1), (-1, -1)]

  def __init__(self, color, pos):
    super().__init__(color, pos)
    self.piece_type = "Q" if self.get_color() == "W" else "q"

  def possible_legal_moves(self, board: Board):
    return super().possible_legal_moves(board, Queen.MOVE_OFFSETS)

  def get_legal_moves(self, board: Board):
    legal_moves = set()
    my_pieces = board.get_all_pieces_by_color(self.get_color())
    my_king = [piece for piece in my_pieces if piece is King][0]
    checks = my_king.get_checks()
    pins = my_king.get_pins()

    if len(checks) == 2:
      return set()
    elif len(checks) == 1 and self in pins:
      return set()

    # Queen can always take a pinner piece
    elif self in pins:
      return self._pin_line(self.get_pos(), pins[self][1])
    elif len(checks) == 1:
      possible_pos = self.possible_legal_moves(board)
      king_pos = my_king.get_pos()
      check_pos = checks[0].get_pos()

      check_blocks = self._check_line(king_pos, check_pos)

      for pos in possible_pos:
        if pos in check_blocks:
          legal_moves.add(pos)

      return legal_moves

    else:
      return self.possible_legal_moves()


class Rook(Sliding_Piece):
  MOVE_OFFSETS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

  def __init__(self, color, pos):
    super().__init__(color, pos)
    self.piece_type = "R" if self.get_color() == "W" else "r"

  def possible_legal_moves(self, board: Board):
    return super().possible_legal_moves(board, Rook.MOVE_OFFSETS)

  def get_legal_moves(self, board: Board):
    legal_moves = set()
    my_pieces = board.get_all_pieces_by_color(self.get_color())
    my_king = [piece for piece in my_pieces if piece is King][0]
    checks = my_king.get_checks()
    pins = my_king.get_pins()

    if (
        len(checks) == 2
        or (len(checks) == 1 and self in pins)
        or (self in pins and (pins[self][0] == "d"))
    ):
      return set()
    elif self in pins:
      return self._pin_line(self.get_pos(), pins[self][1])
    elif len(checks) == 1:
      possible_moves = self.possible_legal_moves(board)
      king_pos = my_king.get_pos()
      check_pos = checks[0].get_pos()

      check_blocks = self._check_line(king_pos, check_pos)

      for move in possible_moves:
        if move in check_blocks:
          legal_moves.add(move)
    else:
      return self.possible_legal_moves()


class Bishop(Sliding_Piece):
  MOVE_OFFSETS = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

  def __init__(self, color, pos):
    super().__init__(color, pos)
    self.piece_type = "B" if self.get_color() == "W" else "b"

  def possible_legal_moves(self, board: Board):
    return super().possible_legal_moves(board, Bishop.MOVE_OFFSETS)

  def get_legal_moves(self, board: Board):
    legal_moves = set()
    my_pieces = board.get_all_pieces_by_color(self.get_color())
    my_king = [piece for piece in my_pieces if piece is King][0]
    checks = my_king.get_checks()
    pins = my_king.get_pins()

    if (
        len(checks) == 2
        or (len(checks) == 1 and self in pins)
        or (self in pins and pins[self][0] != "d")
    ):
      return set()
    elif self in pins:
      return self._pin_line(self.get_pos(), pins[self][1])
    elif len(checks) == 1:
      possible_moves = self.possible_legal_moves(board)
      king_pos = my_king.get_pos()
      check_pos = checks[0].get_pos()

      check_blocks = self._check_line(king_pos, check_pos)

      for move in possible_moves:
        if move in check_blocks:
          legal_moves.add(move)
    else:
      return self.possible_legal_moves()
