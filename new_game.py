from typing import *
from new_board import Board
from new_piece import Piece, King, Knight, Pawn, Queen, Rook, Bishop
from new_agent import HumanAgent

ROW_SIZE = 5
COL_SIZE = 4
STARTING_FEN = "knbr/p3/4/3P/RBNK"


class Game:
  def __init__(self) -> None:
    self.board = Board(ROW_SIZE, COL_SIZE)
    self.players = (HumanAgent(0, self.board), HumanAgent(1, self.board))
    self._starting_position()

  def play(self) -> None:
    while True:
      for p in self.players:
        curr_pos, new_pos = p.get_move()
        piece = self.board.lookup(curr_pos)
        self.board.remove(curr_pos)
        self.board.remove(new_pos)
        self.board.place(new_pos)

  def make_piece(self, fen_char: str, pos: tuple[int]) -> None:
    mapping = {
        'p': lambda: Pawn(0, pos, self.board),
        'r': lambda: Rook(0, pos, self.board),
        'n': lambda: Knight(0, pos, self.board),
        'b': lambda: Bishop(0, pos, self.board),
        'q': lambda: Queen(0, pos, self.board),
        'k': lambda: King(0, pos, self.board),
        'P': lambda: Pawn(1, pos, self.board),
        'R': lambda: Rook(1, pos, self.board),
        'N': lambda: Knight(1, pos, self.board),
        'B': lambda: Bishop(1, pos, self.board),
        'Q': lambda: Queen(1, pos, self.board),
        'K': lambda: King(1, pos, self.board),
    }

    return mapping.get(fen_char)

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
          piece = self.make_piece(c, [row_idx, col_idx])
          self.board.place([row_idx, col_idx], piece)
          col_idx += 1


g = Game()
g.play()
