from typing import List, Dict

ROW_COUNT = 5
COL_COUNT = 4
STARTING_FEN = "knbr/p3/4/3P/RBNK"


def make_piece(piece_char, pos):
  if piece_char == "p":
    return Pawn("B", pos)
  elif piece_char == "r":
    return Rook("B", pos)
  elif piece_char == "n":
    return Knight("B", pos)
  elif piece_char == "b":
    return Bishop("B", pos)
  elif piece_char == "q":
    return Queen("B", pos)
  elif piece_char == "k":
    return King("B", pos)
  elif piece_char == "P":
    return Pawn("W", pos)
  elif piece_char == "R":
    return Rook("W", pos)
  elif piece_char == "N":
    return Knight("W", pos)
  elif piece_char == "B":
    return Bishop("W", pos)
  elif piece_char == "Q":
    return Queen("W", pos)
  elif piece_char == "K":
    return King("W", pos)


class Board:
  def __init__(self):
    self.board = [[None for _ in range(COL_COUNT)] for _ in range(ROW_COUNT)]
    self.pieces = []
    self.w_king = None
    self.b_king = None
    self._starting_position()

  def _starting_position(self):
    """Place starting position's chess pieces on board
    """
    rows = STARTING_FEN.split("/")

    for row_idx, row in enumerate(rows):
      col_idx = 0
      for c in row:
        if c.isdigit():
          col_idx += int(c)
        else:
          piece = make_piece(c, [row_idx, col_idx])
          if c == "K":
            self.w_king = piece
          if c == "k":
            self.b_king = piece

          self._place_piece(piece, [row_idx, col_idx])
          col_idx += 1


  def is_valid_location(self, pos):
    """Returns whether a list is a valid board location

    Args:
        pos (List[int]): 2-element list of [row, col]

    Returns:
        bool: Whether pos is a valid board location
    """
    return 0 <= pos[0] < ROW_COUNT and 0 <= pos[1] < COL_COUNT

  def get_cell_piece(self, pos):
    """Returns the piece (or None if empty) at a given board position

    Args:
        pos (List[int]): 2-element list of [row, col]

    Raises:
        ValueError: If pos is not a valid board location

    Returns:
        Piece | None: Object at board cell 
    """
    if not self.is_valid_location(pos):
      raise ValueError(f"Invalid board location: {pos}")

    return self.board[pos[0]][pos[1]]

  def is_cell_empty(self, pos):
    """Returns whether is a board cell is empty (ie. None at cell)

    Args:
        pos (List[int]): 2-element list of [row, col]

    Raises:
        ValueError: If pos is not a valid board location

    Returns:
        bool: Returns true if cell is empty (ie. contains None)
    """
    if not self.is_valid_location(pos):
      raise ValueError(f"Invalid board location: {pos}")

    return self.get_cell_piece(pos) == None

  def _place_piece(self, piece, pos):
    """Places a piece at a given pos and updated piece's pos properties

    Args:
        piece (Piece): A chess piece as implemented in Piece class file
        pos (List[int]): 2-element list of [row, col]

    Raises:
        ValueError: If pos is not a valid board location
    """
    if not self.is_valid_location(pos):
      raise ValueError(f"Invalid board location: {pos}")

    piece_at_pos = self.get_cell_piece(pos)
    if piece_at_pos == None:
      self.board[pos[0]][pos[1]] = piece
    elif piece_at_pos.get_color() != piece.get_color():
      self._remove_piece(piece_at_pos)
      self.board[pos[0]][pos[1]] = piece
    else:
      raise ValueError(f"Cannot move piece to same color occupied cell")
    if piece in self.pieces:
      raise ValueError("This piece is being counted twice in self.pieces")
    self.pieces.append(piece)
    piece.set_pos(pos)

  def _remove_from_cell(self, pos):
    """Removes a piece at a given position and returns it

    Args:
        pos (List[int]): A 2-element list of [row, col]

    Raises:
        ValueError: If pos is not a valid board location
        ValueError: If there is no piece to remove at the given pos
    """
    if not self.is_valid_location(pos):
      raise ValueError(f"Invalid board location: {pos}")
    piece = self.board[pos[0]][pos[1]]
    if not piece:
      raise ValueError(f"No piece to remove at location: {pos}")
    self.board[pos[0]][pos[1]] = None
    self.pieces.remove(piece)
    piece.remove_pos()
    return piece

  def _remove_piece(self, piece):
    """Given a piece, remove it from the board

    Args:
        piece (Piece): A chess piece object
    """
    piece_pos = piece.get_pos()
    self._remove_from_cell(piece_pos)

  def get_all_pieces(self):
    """Returns a list of all pieces on board

    Returns:
        List[Piece]: Chess piece
    """
    return self.pieces

  def get_all_pieces_by_color(self, color):
    return list(filter(lambda x: x.get_color() == color, self.get_all_pieces()))

  def move_piece(self, piece, pos):
    """Given a piece and a new pos, move the piece to the new pos and clear the old pos

    Args:
        piece (Piece): A chess piece object
        pos (List[int]): A 2-element list of [row, col]

    Raises:
        ValueError: If pos is not a valid board location
    """
    self._remove_piece(piece)
    self._place_piece(piece, pos)

  def __str__(self):
    """Converts board state to FEN string for pieces only.

    Returns:
        str: FEN-formatted string of board pieces.
    """

    acc = ""
    count = 0
    for row in self.board:
      for piece in row:
        if piece == None:
          count += 1
        else:
          if count != 0:
            acc += str(count)
            count = 0
          acc += str(piece)

      if count != 0:
        acc += str(count)
      count = 0
      acc += "/"

    return acc[:-1]  # Remove last slash

  def print_board(self):
    """Prints board state in a human readable format
    """
    for row in self.board:
      row_string = "|"
      for piece in row:
        piece_char = "." if piece == None else str(piece)
        row_string += piece_char + "|"

      print(row_string)

  def all_moves_by_color(self, color):
    if color == 'W':
      self.w_king.checks_and_pins(self)
      all_moves = []
      pieces = self.get_all_pieces_by_color("W")
      for piece in pieces:
        all_moves.extend(piece.get_legal_moves(self))
    else:
      self.b_king.checks_and_pins(self)
      all_moves = []
      pieces = self.get_all_pieces_by_color("B")
      for piece in pieces:
        all_moves.extend(piece.get_legal_moves(self))

    return all_moves




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
    if self.piece_type is None:
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

    check_line = []

    curr_pos = king_pos

    while curr_pos != checker_pos:
      curr_pos[0] += vector_direction[0]
      curr_pos[1] += vector_direction[1]

      check_line.append(curr_pos)

    return check_line

  def _pin_line(self, pin_pos: List, pinner_pos: List):
    vector = [pinner_pos[0] - pin_pos[0], pinner_pos[1] - pin_pos[1]]
    vector_direction = [0, 0]
    if vector[0] != 0:
      vector_direction[0] = (vector[0]/abs(vector[0]))
    if vector[1] != 0:
      vector_direction[1] = (vector[1]/abs(vector[1]))

    pin_line = []

    curr_pos = pin_pos

    while curr_pos != pinner_pos:
      curr_pos[0] += vector_direction[0]
      curr_pos[1] += vector_direction[1]

      pin_line.append(curr_pos)

    return pin_line

  def get_legal_moves(self, board: Board):
    """Return a list of legal piece moves

    Args:
        board (Board): Board object

    Raises:
        NotImplementedError: Method should be overrided by children classes
    """
    raise NotImplementedError

  def attacking_squares(self, board: Board):
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
      shields = []
      while board.is_valid_location(possible_pos):

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

  def attacking_squares(self, board: Board):
    curr_pos = self.get_pos()
    legal_moves = []
    for offset in King.MOVE_OFFSETS:
      possible_pos = [curr_pos[0] + offset[0], curr_pos[1] + offset[1]]
      if not board.is_valid_location(possible_pos):
        continue
      else:
        legal_moves.append(possible_pos)

    return legal_moves

  def get_legal_moves(self, board: Board):
    curr_pos = self.get_pos()
    legal_moves = []
    opponent_color = "B" if self.get_color() == "W" else "W"
    opponent_pieces = board.get_all_pieces_by_color(opponent_color)

    for offset in King.MOVE_OFFSETS:
      possible_pos = [curr_pos[0] + offset[0], curr_pos[1] + offset[1]]

      if (
          board.is_valid_location(possible_pos) and
          all(possible_pos not in p.attacking_squares(board) for p in opponent_pieces) and
          (board.get_cell_piece(possible_pos) is None or
           board.get_cell_piece(possible_pos).get_color() != self.get_color())
      ):
        legal_moves.append(possible_pos)

    return legal_moves


class Knight(Piece):
  MOVE_OFFSETS = [(1, 2), (1, -2), (-1, 2), (-1, -2),
                  (2, 1), (2, -1), (-2, 1), (-2, -1)]

  def __init__(self, color, pos):
    super().__init__(color, pos)
    self.piece_type = "N" if self.get_color() == "W" else "n"

  def possible_legal_moves(self, board: Board):
    curr_pos = self.get_pos()
    legal_moves = []

    for offset in Knight.MOVE_OFFSETS:
      possible_pos = [curr_pos[0] + offset[0], curr_pos[1] + offset[1]]

      if board.is_valid_location(possible_pos) and (
          board.is_cell_empty(possible_pos)
          or board.get_cell_piece(possible_pos).get_color() != self.get_color()
      ):
        legal_moves.append(possible_pos.copy())

    return legal_moves

  def attacking_squares(self, board: Board):
    curr_pos = self.get_pos()
    legal_moves = []

    for offset in Knight.MOVE_OFFSETS:
      possible_pos = [curr_pos[0] + offset[0], curr_pos[1] + offset[1]]

      if board.is_valid_location(possible_pos):
        legal_moves.append(possible_pos)

    return legal_moves

  def get_legal_moves(self, board: Board):
    legal_moves = []
    if self.get_color() == "W": my_king = board.w_king
    else: my_king = board.b_king
    checks = my_king.get_checks()
    pins = my_king.get_pins()

    if len(checks) == 2 or self in pins:
      return []
    elif len(checks) == 1:
      possible_moves = self.possible_legal_moves(board)
      king_pos = my_king.get_pos()
      check_pos = checks[0].get_pos()

      check_blocks = self._check_line(king_pos, check_pos)

      for move in possible_moves:
        if move in check_blocks:
          legal_moves.append(move)

      return legal_moves
    else:
      return self.possible_legal_moves(board)


class Pawn(Piece):
  def __init__(self, color, pos):
    super().__init__(color, pos)
    self.piece_type = "P" if self.get_color() == "W" else "p"

  def possible_legal_moves(self, board: Board):

    legal_moves = []

    vertical_direction = -1 if self.get_color() == "W" else 1
    curr_pos = self.get_pos()

    # One forward
    forward_move = [curr_pos[0] + vertical_direction, curr_pos[1]]
    if board.is_valid_location(forward_move) and board.is_cell_empty(forward_move):
      legal_moves.append(forward_move.copy())

    # Capture moves (diagonal)
    diagonal_moves = [
        [curr_pos[0] + vertical_direction, curr_pos[1] - 1],
        [curr_pos[0] + vertical_direction, curr_pos[1] + 1]
    ]

    for move in diagonal_moves:
      if board.is_valid_location(move):
        piece_at_cell = board.get_cell_piece(move)
        if piece_at_cell and piece_at_cell.get_color() != self.get_color():
          legal_moves.append(move)

    return legal_moves

  def attacking_squares(self, board: Board):
    legal_moves = []

    vertical_direction = -1 if self.get_color() == "W" else 1
    curr_pos = self.get_pos()

    diagonal_moves = [
      [curr_pos[0] + vertical_direction, curr_pos[1] - 1],
      [curr_pos[0] + vertical_direction, curr_pos[1] + 1]
    ]

    for move in diagonal_moves:
      if board.is_valid_location(move):
        legal_moves.append(move)

    return legal_moves


  def get_legal_moves(self, board: Board):
    legal_moves = []
    if self.get_color() == "W":
      my_king = board.w_king
    else:
      my_king = board.b_king
    checks = my_king.get_checks()
    pins = my_king.get_pins()

    if len(checks) == 2:
      return []
    elif len(checks) == 1 and self in pins:
      return []
    # A pawn can only move in a pin if the attacker is ahead of it vertically
    elif self in pins and pins[self][0] == "v":
      direction = -1 if self.get_color() == "W" else 1
      possible_pos = [self.get_pos()[0] + direction, self.get_pos()[1]]
      if board.is_cell_empty(possible_pos):
        return [possible_pos]
      else:
        return []
    elif self in pins:
      return []
    elif len(checks) == 1:
      possible_moves = self.possible_legal_moves(board)
      king_pos = my_king.get_pos()
      check_pos = checks[0].get_pos()

      check_blocks = self._check_line(king_pos, check_pos)

      for move in possible_moves:
        if move in check_blocks:
          legal_moves.append(move)

      return legal_moves

    else:
      return self.possible_legal_moves(board)

class Sliding_Piece(Piece):
  def __init__(self, color, pos):
    super().__init__(color, pos)

  def possible_legal_moves(self, board: Board, move_offsets):
    curr_pos = self.get_pos()
    legal_moves = []

    for offset in move_offsets:
      possible_pos = [curr_pos[0] + offset[0], curr_pos[1] + offset[1]]

      while board.is_valid_location(possible_pos):
        piece_at_cell = board.get_cell_piece(possible_pos)
        if piece_at_cell is None:
          legal_moves.append(possible_pos.copy())
          possible_pos = [possible_pos[0] + offset[0], possible_pos[1] + offset[1]]
        elif piece_at_cell.get_color() != self.get_color():
          legal_moves.append(possible_pos.copy())
          break
        else:
          break

    return legal_moves

  def get_legal_moves(self, board: Board):
    raise NotImplementedError

  def attacking_squares(self, board: Board):
    raise NotImplementedError




class Queen(Sliding_Piece):
  MOVE_OFFSETS = [(1, 0), (0, 1), (-1, 0), (0, -1),
                  (1, 1), (1, -1), (-1, 1), (-1, -1)]

  def __init__(self, color, pos):
    super().__init__(color, pos)
    self.piece_type = "Q" if self.get_color() == "W" else "q"

  def possible_legal_moves(self, board: Board, offsets):
    return super().possible_legal_moves(board, offsets)

  def get_legal_moves(self, board: Board):
    legal_moves = []
    if self.get_color() == "W":
      my_king = board.w_king
    else:
      my_king = board.b_king
    checks = my_king.get_checks()
    pins = my_king.get_pins()

    if len(checks) == 2:
      return []
    elif len(checks) == 1 and self in pins:
      return []

    # Queen can always take a pinner piece
    elif self in pins:
      return self._pin_line(self.get_pos(), pins[self][1])
    elif len(checks) == 1:
      possible_pos = self.possible_legal_moves(board, Queen.MOVE_OFFSETS)
      king_pos = my_king.get_pos()
      check_pos = checks[0].get_pos()

      check_blocks = self._check_line(king_pos, check_pos)

      for pos in possible_pos:
        if pos in check_blocks:
          legal_moves.append(pos)

      return legal_moves

    else:
      return self.possible_legal_moves(board, Queen.MOVE_OFFSETS)

  def attacking_squares(self, board: Board):
    curr_pos = self.get_pos()
    legal_moves = []

    for offset in Queen.MOVE_OFFSETS:
      possible_pos = [curr_pos[0] + offset[0], curr_pos[1] + offset[1]]

      while board.is_valid_location(possible_pos):
        piece_at_cell = board.get_cell_piece(possible_pos)
        if piece_at_cell is None:
          legal_moves.append(possible_pos.copy())
          possible_pos = [possible_pos[0] + offset[0], possible_pos[1] + offset[1]]
        else:
          legal_moves.append(possible_pos.copy())
          break
    return legal_moves


class Rook(Sliding_Piece):
  MOVE_OFFSETS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

  def __init__(self, color, pos):
    super().__init__(color, pos)
    self.piece_type = "R" if self.get_color() == "W" else "r"

  def possible_legal_moves(self, board: Board, offsets):
    return super().possible_legal_moves(board, offsets)

  def get_legal_moves(self, board: Board):
    legal_moves = []
    if self.get_color() == "W":
      my_king = board.w_king
    else:
      my_king = board.b_king
    checks = my_king.get_checks()
    pins = my_king.get_pins()

    if (
        len(checks) == 2
        or (len(checks) == 1 and self in pins)
        or (self in pins and (pins[self][0] == "d"))
    ):
      return []
    elif self in pins:
      return self._pin_line(self.get_pos(), pins[self][1])
    elif len(checks) == 1:
      possible_moves = self.possible_legal_moves(board, Rook.MOVE_OFFSETS)
      king_pos = my_king.get_pos()
      check_pos = checks[0].get_pos()

      check_blocks = self._check_line(king_pos, check_pos)

      for move in possible_moves:
        if move in check_blocks:
          legal_moves.append(move)

      return legal_moves
    else:
      return self.possible_legal_moves(board, Rook.MOVE_OFFSETS)

  def attacking_squares(self, board: Board):
    curr_pos = self.get_pos()
    legal_moves = []

    for offset in Rook.MOVE_OFFSETS:
      possible_pos = [curr_pos[0] + offset[0], curr_pos[1] + offset[1]]

      while board.is_valid_location(possible_pos):
        piece_at_cell = board.get_cell_piece(possible_pos)
        if piece_at_cell is None:
          legal_moves.append(possible_pos.copy())
          possible_pos = [possible_pos[0] + offset[0], possible_pos[1] + offset[1]]
        else:
          legal_moves.append(possible_pos.copy())
          break
    return legal_moves


class Bishop(Sliding_Piece):
  MOVE_OFFSETS = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

  def __init__(self, color, pos):
    super().__init__(color, pos)
    self.piece_type = "B" if self.get_color() == "W" else "b"

  def possible_legal_moves(self, board: Board, offsets):
    return super().possible_legal_moves(board, offsets)

  def get_legal_moves(self, board: Board):
    legal_moves = []
    if self.get_color() == "W":
      my_king = board.w_king
    else:
      my_king = board.b_king
    checks = my_king.get_checks()
    pins = my_king.get_pins()

    if (
        len(checks) == 2
        or (len(checks) == 1 and self in pins)
        or (self in pins and pins[self][0] != "d")
    ):
      return []
    elif self in pins:
      return self._pin_line(self.get_pos(), pins[self][1])
    elif len(checks) == 1:
      possible_moves = self.possible_legal_moves(board, Bishop.MOVE_OFFSETS)
      king_pos = my_king.get_pos()
      check_pos = checks[0].get_pos()

      check_blocks = self._check_line(king_pos, check_pos)

      for move in possible_moves:
        if move in check_blocks:
          legal_moves.append(move)
      return legal_moves
    else:
      return self.possible_legal_moves(board, Bishop.MOVE_OFFSETS)

  def attacking_squares(self, board: Board):
    curr_pos = self.get_pos()
    legal_moves = []

    for offset in Bishop.MOVE_OFFSETS:
      possible_pos = [curr_pos[0] + offset[0], curr_pos[1] + offset[1]]

      while board.is_valid_location(possible_pos):
        piece_at_cell = board.get_cell_piece(possible_pos)
        if piece_at_cell is None:
          legal_moves.append(possible_pos.copy())
          possible_pos = [possible_pos[0] + offset[0], possible_pos[1] + offset[1]]
        else:
          legal_moves.append(possible_pos.copy())
          break
    return legal_moves



