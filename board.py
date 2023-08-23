from piece import *

ROW_COUNT = 5
COL_COUNT = 4


class Board:
  def __init__(self):
    self.board = [[None for _ in range(COL_COUNT)] for _ in range(ROW_COUNT)]

  def is_valid_location(self, pos):
    """Returns whether a list is a valid board location

    Args:
        pos (List[]): 2-element list of [row, col]

    Returns:
        bool: Whether pos is a valid board location
    """
    return 0 <= pos[0] < ROW_COUNT and 0 <= pos[1] < COL_COUNT

  def get_cell_piece(self, pos):
    """_summary_

    Args:
        pos (List[]): 2-element list of [row, col]

    Returns:
        _type_: _description_
    """
    return self.board[pos[0], pos[1]]

  def is_cell_empty(self, pos):
    return self.get_cell_piece(pos[0], pos[1]) == None

  def _place_piece(self, piece, pos):
    self.board[pos[0], pos[1]] = piece
    piece.set_pos(pos)

  def _remove_from_cell(self, pos):
    if not self.is_valid_location(pos):
      raise ValueError(f"Invalid cell location: {pos}")
    piece = self.board[pos[0], pos[1]]
    if not piece:
      raise ValueError(f"No piece to remove at location: {pos}")
    piece.remove_pos()
    self.board[pos[0], pos[1]] = None

  def _remove_piece(self, piece):
    piece_pos = piece.get_pos()
    self._remove_from_cell(piece_pos)

  def move_piece(self, piece, pos):
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
    """Prints board state
    """
    print()
    for row in self.board:
      row_string = "|"
      for piece in row:
        piece_char = "." if piece == None else str(piece)
        row_string += piece_char + "|"

      print(row_string)
