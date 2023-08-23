"""
Chess piece implementations
"""
from board import Board


class Piece:
  def __init__(self, color, pos):
    """Initialize piece 

    Args:
        color (str): 'B' or 'W' for black and white
        pos (List[int]): A 2-element list of [row, col]
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

  def get_legal_moves(self, board):
    """Return a list of legal piece moves

    Args:
        board (Board): Board object

    Raises:
        NotImplementedError: Method should be overrided by children classes
    """
    raise NotImplementedError


class King(Piece):
  MOVE_OFFSETS = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
  def __init__(self):
    super().__init__()
    self.piece_type = "K" if self.color == "W" else "k"
  
  def get_legal_moves(self, board, opposite_pieces):
    """_summary_

    Args:
        board (_type_): _description_
        opposite_pieces (List[Piece]): _description_
    """
    curr_pos = self.pos
    legal_moves = set()

    for offset in King.MOVE_OFFSETS:
      possible_pos = [curr_pos[0] + offset[0], curr_pos[1] + offset[1]]

      if not board.is_valid_location(possible_pos):
        continue
      elif board.get_cell_piece(possible_pos).get_color() == self.get_color():
        continue
      elif any(possible_pos in p.get_legal_moves for p in opposite_pieces):
        continue
      else:
        legal_moves.add(possible_pos)

class Knight(Piece):

  MOVE_OFFSETS = [(1, 2), (1, -2), (-1, 2), (-1, -2),
                  (2, 1), (2, -1), (-2, 1), (-2, -1)]

  def __init__(self):
    super().__init__()
    self.piece_type = "N" if self.color == "W" else "n"

  def get_legal_moves(self, board):
    """Return a list of legal piece moves

    Args:
        board (Board): Board object
    """

    curr_pos = self.pos
    legal_moves = []

    for offset in Knight.MOVE_OFFSETS:
      possible_pos = [curr_pos[0] + offset[0], curr_pos[1] + offset[1]]

      if not board.is_valid_location(possible_pos):
        continue
      elif board.get_cell_piece(possible_pos).get_color() == self.get_color():
        continue
      else:
        legal_moves.add(possible_pos)


class Pawn(Piece):
  def __init__(self):
    super().__init__()
    self.piece_type = "P" if self.color == "W" else "p"


class Queen(Piece):
  def __init__(self):
    super().__init__()
    self.piece_type = "Q" if self.color == "W" else "q"


class Rook(Piece):
  def __init__(self):
    super().__init__()
    self.piece_type = "R" if self.color == "W" else "r"


class Bishop(Piece):
  def __init__(self):
    super().__init__()
    self.piece_type = "B" if self.color == "w" else "b"
