from typing import *
from board import Board
from piece import Piece, King, Knight, Pawn, Queen, Rook, Bishop
from agent import HumanAgent
WHITE, BLACK = 0, 1
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
        game_state = self.is_game_over(p.color)
        if game_state[0]:
          return game_state[1]
        curr_pos, new_pos = p.get_move()
        piece = self.board.lookup(curr_pos)
        if piece.get_color() != p.get_color() or new_pos not in piece.moves():
          print("Invalid choice -- you lose a turn HAHAHA")
          continue
        self.board.remove(curr_pos)
        self.board.remove(new_pos)
        self.board.place(new_pos, piece)

  def make_piece(self, fen_char: str, pos: tuple[int, int]) -> Piece:
    mapping = {
        'P': lambda: Pawn(0, pos, self.board),
        'R': lambda: Rook(0, pos, self.board),
        'N': lambda: Knight(0, pos, self.board),
        'B': lambda: Bishop(0, pos, self.board),
        'Q': lambda: Queen(0, pos, self.board),
        'K': lambda: King(0, pos, self.board),
        'p': lambda: Pawn(1, pos, self.board),
        'r': lambda: Rook(1, pos, self.board),
        'n': lambda: Knight(1, pos, self.board),
        'b': lambda: Bishop(1, pos, self.board),
        'q': lambda: Queen(1, pos, self.board),
        'k': lambda: King(1, pos, self.board),
    }

    return mapping.get(fen_char)()

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
          piece = self.make_piece(c, (row_idx, col_idx))
          self.board.place((row_idx, col_idx), piece)
          self.board.add_piece(piece)
          col_idx += 1

  def is_game_over(self, color) -> list:
    if color == WHITE:
      all_moves = self.all_moves_by_color(WHITE)
      if len(all_moves) == 0 and len(self.board.pieces["K"][0].moves()) > 1:
        return [True, 'White Wins']
      elif len(all_moves) == 0:
        return [True, 'Draw']
      else:
        return [False]
    else:
      all_moves = self.all_moves_by_color(BLACK)
      if len(all_moves) == 0 and len(self.board.pieces["K"][0].moves()) > 1:
        return [True, 'Black Wins']
      elif len(all_moves) == 0:
        return [True, 'Draw']
      else:
        return [False]

  def all_moves_by_color(self, color: int) -> list[tuple[int, int]]:
    all_moves = []
    for pieces in self.board.pieces:
      if color == BLACK and pieces.islower():
        for piece in self.board.pieces[pieces]:
          all_moves.extend(piece.moves())
      elif color == WHITE and pieces.isupper():
        for piece in self.board.pieces[pieces]:
          all_moves.extend(piece.moves())

    return all_moves

# test







