from typing import *
from board import Board
from piece import Piece, King, Knight, Pawn, Queen, Rook, Bishop
from agent import *
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
        p.my_king()[0].checks_and_pins()
        game_state = self.is_game_over(p.color)
        if game_state[0]:
          return game_state[1]
        print("###################################")
        print(
            f"Color to move: {'white' if p.get_color() == WHITE else 'black'}")
        print(
            f"BEFORE My king is checked by: {p.my_king()[0].get_checks()} and pinned by {p.my_king()[0].get_pins()}")
        while self.move(p) != "DONE":
          continue

        print(
            f"AFTER My king is checked by: {p.my_king()[0].get_checks()} and pinned by {p.my_king()[0].get_pins()}")
        print("###################################")

  def move(self, p: Agent) -> None:
    option, curr_pos, new_pos = p.get_move()
    curr_pos_piece = self.board.lookup(curr_pos)
    new_pos_piece = self.board.lookup(new_pos)

    # Get all piece moves given piece coordinates
    if option == 0:
      moves = curr_pos_piece.moves()
      p.set_info(moves)
      return

    # Move a piece to a new coordinate
    elif option == 1:
      if curr_pos_piece.get_color() != p.get_color() or new_pos not in curr_pos_piece.moves():
        p.set_info("Invalid choice -- try again")
        return

      self.board.remove(curr_pos)
      self.board.forget_piece(curr_pos_piece)
      curr_pos_piece.remove_pos()

      if new_pos_piece != None:
        self.board.remove(new_pos)
        self.board.forget_piece(new_pos_piece)
        new_pos_piece.remove_pos()

      self.board.place(new_pos, curr_pos_piece)
      self.board.add_piece(curr_pos_piece)
      curr_pos_piece.set_pos(new_pos)

      return "DONE"

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
          piece.set_pos((row_idx, col_idx))
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
