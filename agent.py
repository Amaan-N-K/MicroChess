from board import Board
from evaluate import *
from piece import *
WHITE, BLACK = 0, 1

class Agent:
  def __init__(self, color: int, board: Board) -> None:
    self.color = color
    self.board = board
    self.info = None

  def get_color(self) -> int:
    return self.color

  def get_info(self) -> any:
    return self.info

  def set_info(self, info: any) -> None:
    self.info = info

  def my_king(self) -> any:
    return self.board.get_piece("K") if self.get_color() == 0 else self.board.get_piece("k")

  def get_move(self) -> list[int, tuple[int, int]]:
    raise NotImplementedError("This method must be override by child classes")


class HumanAgent(Agent):
  def __init__(self, color: int, board: Board) -> None:
    super().__init__(color, board)

  def get_move(self) -> list[int, tuple[int, int]]:
    count = 0
    if self.get_info():
      print(self.get_info())
    while True:
      try:
        choice = input("Enter [OPTION] [row] [col] [row] [col]: ").split(" ")
        option = int(choice[0])
        curr_pos = (int(choice[1]), int(choice[2]))
        new_pos = (int(choice[3]), int(choice[4]))

        if not self.board.is_valid_pos(curr_pos) or not self.board.is_valid_pos(new_pos):
          print("Invalid choice -- try again")
          continue

        return [option, curr_pos, new_pos]

      except:
        print("Invalid choice -- try again")
        count += 1

      if count == 10:
        print("You are trolling")
        break


class MinimaxAgent(Agent):
  def __init__(self, color: int, board: Board, eval_func) -> None:
    super().__init__(color, board)
    self.eval_func = eval_func

  def apply_move(self, curr_pos_piece, new_pos) -> list[tuple[int, int], any, tuple[int, int], any]:
    curr_pos = curr_pos_piece.get_pos()
    new_pos_piece = self.board.lookup(new_pos)
    data = [curr_pos, curr_pos_piece, new_pos, None]

    self.board.remove(curr_pos)
    self.board.forget_piece(curr_pos_piece)
    curr_pos_piece.remove_pos()

    if new_pos_piece is not None:
      self.board.remove(new_pos)
      self.board.forget_piece(new_pos_piece)
      new_pos_piece.remove_pos()
      data[3] = new_pos_piece

    self.board.place(new_pos, curr_pos_piece)
    self.board.add_piece(curr_pos_piece)
    curr_pos_piece.set_pos(new_pos)

    return data

  def undo_move(self, data: list[tuple[int, int], any, tuple[int, int], any]):
    curr_pos, curr_pos_piece, new_pos, new_pos_piece = data

    self.board.remove(new_pos)
    self.board.forget_piece(curr_pos_piece)
    curr_pos_piece.remove_pos()

    if new_pos_piece is not None:
      self.board.place(new_pos, new_pos_piece)
      self.board.add_piece(new_pos_piece)
      new_pos_piece.set_pos(new_pos)

    self.board.place(curr_pos, curr_pos_piece)
    self.board.add_piece(curr_pos_piece)
    curr_pos_piece.set_pos(curr_pos)

  def minimax(self, move_func, depth: int, is_white: bool) -> tuple:

    white_king = self.board.get_piece("K")[0]
    black_king = self.board.get_piece("k")[0]
    white_king.checks_and_pins()
    black_king.checks_and_pins()
    white_moves = move_func(self.board, WHITE)
    black_moves = move_func(self.board, BLACK)

    white_moves_len = sum([len(moves) for moves in white_moves.values()])
    black_moves_len = sum([len(moves) for moves in black_moves.values()])

    # Checkmate
    if white_moves_len == 0 and len(white_king.get_checks()) > 0:
      return (-100000000 * depth - 100000000, (None, None))
    if black_moves_len == 0 and len(black_king.get_checks()) > 0:
      return (100000000 * depth + 100000000, (None, None))


    # Draw
    if is_white and len(white_moves) == 0:
      return (0, (None, None))
    if not is_white and len(black_moves) == 0:
      return (0, (None, None))

    if depth == 0:
      return (self.eval_func(self.board), (None, None))

    if is_white:
      evals = []
      for piece in white_moves:
        for move in white_moves[piece]:
          data = self.apply_move(piece, move)
          evaluation = self.minimax(all_moves_by_color_dict, depth - 1, False)
          self.undo_move(data)
          evals.append((evaluation[0], (piece.get_pos(), move)))
      white_king.checks_and_pins()
      black_king.checks_and_pins()
      if evals == []:
        return (0, (None, None))
      return max(evals, key=lambda x: x[0])
    else:
      evals = []
      for piece in black_moves:
        for move in black_moves[piece]:
          data = self.apply_move(piece, move)
          eval_val = self.minimax(all_moves_by_color_dict, depth - 1, True)
          self.undo_move(data)
          evals.append((eval_val[0], (piece.get_pos(), move), str(piece)))
      white_king.checks_and_pins()
      black_king.checks_and_pins()
      if evals == []:
        return (0, (None, None))
      return min(evals, key=lambda x: x[0])

  def get_move(self):
    move = self.minimax(all_moves_by_color_dict, 3, self.color == 0)
    return (1, move[1][0], move[1][1])

def all_moves_by_color_dict(board: Board, color: int) -> dict:
    white_king = board.get_piece("K")[0]
    black_king = board.get_piece("k")[0]
    white_king.checks_and_pins()
    black_king.checks_and_pins()
    all_moves = {}
    for pieces in board.pieces:
      if color == BLACK and pieces.islower():
        for piece in board.pieces[pieces]:
          all_moves[piece] = piece.moves()
      if color == WHITE and pieces.isupper():
        for piece in board.pieces[pieces]:
          all_moves[piece] = piece.moves()

    return all_moves



