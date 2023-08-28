from typing import *


class Board:
  def __init__(self, row_size: int, col_size: int) -> None:
    self.board = [[None for _ in range(col_size)] for _ in range(row_size)]
    self.row_size = row_size
    self.col_size = col_size
    self.pieces = dict()

  def is_valid_pos(self, pos: tuple[int, int]) -> bool:
    return 0 <= pos[0] < self.row_size and 0 <= pos[1] < self.col_size

  def is_empty_pos(self, pos: tuple[int, int]) -> bool:
    return self.board[pos[0]][pos[1]] is None

  def add_piece(self, piece: any) -> None:
    self.pieces.setdefault(str(piece), []).append(piece)

  def forget_piece(self, piece: any) -> None:
    self.pieces[str(piece)] = [p for p in self.pieces.get(
        str(piece), []) if p != piece]

  def get_piece(self, piece: str) -> Optional[any]:
    return self.pieces.get(piece, None)

  def place(self, pos: tuple[int, int], piece: any) -> None:
    self.board[pos[0]][pos[1]] = piece

  def remove(self, pos: tuple[int, int]) -> None:
    self.board[pos[0]][pos[1]] = None

  def lookup(self, pos: tuple[int, int]) -> Optional[any]:
    return self.board[pos[0]][pos[1]]

  def __str__(self) -> str:
    """Converts board state to FEN string for pieces only and expects pieces to have __str__ defined

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

  def print_board(self) -> None:
    """Prints board state in a human readable format and expects pieces to have __str__ defined
    """
    for row in self.board:
      row_string = "|"
      for piece in row:
        piece_char = "." if piece == None else str(piece)
        row_string += piece_char + "|"

      print(row_string)
