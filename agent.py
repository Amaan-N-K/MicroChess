from board import Board
from evaluate import *

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
    raise NotImplementedError("This method must be overided by child classes")


class HumanAgent(Agent):
  def __init__(self, color: int, board: Board) -> None:
    super().__init__(color, board)

  def get_move(self) -> list[int, tuple[int, int]]:
    count = 0
    self.board.print_board()
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
  def __init__(self, color: int, board: Board, eval_func: callable()) -> None:
    super().__init__(color, board)
    self.eval_func = eval_func

  def apply_move(self, curr_pos, new_pos) -> List[tuple(int, int), any, tuple(int, int), any]:

    data = [curr_pos, curr_pos_piece, new_pos, None]

    curr_pos_piece = self.board.lookup(curr_pos)
    new_pos_piece = self.board.lookup(new_pos)

    self.board.remove(curr_pos)
    self.board.forget_piece(curr_pos_piece)
    curr_pos_piece.remove_pos()

    if new_pos_piece != None:
      self.board.remove(new_pos)
      self.board.forget_piece(new_pos_piece)
      new_pos_piece.remove_pos()
      data[3] = new_pos_piece

    self.board.place(new_pos, curr_pos_piece)
    self.board.add_piece(curr_pos_piece)
    curr_pos_piece.set_pos(new_pos)

    return data

  def undo_move(self, data: List[tuple(int, int), any, tuple(int, int), any]):
    curr_pos, curr_pos_piece, new_pos, new_pos_piece = data

    self.board.remove(new_pos)
    self.board.forget_piece(curr_pos_piece)
    curr_pos_piece.remove_pos()

    if new_pos_piece != None:
      self.board.place(new_pos, new_pos_piece)
      self.board.add_piece(new_pos_piece)
      new_pos_piece.set_pos(new_pos)

    self.board.place(curr_pos, curr_pos_piece)
    self.board.add_piece(curr_pos_piece)
    curr_pos_piece.set_pos(curr_pos)

  def minimax(self, all_moves_by_color, depth: int, isWhite: bool):
    white_moves = all_moves_by_color(WHITE)
    black_moves = all_moves_by_color(BLACK)
    white_king = self.board.get("K")[0]
    black_king = self.board.get("k")[0]
    white_king.checks_and_pins()
    black_king.checks_and_pins()

    if depth == 0:
      return self.eval_func(self.board)

    # Checkmate
    if len(white_moves) == 0 and len(white_king.get_checks() > 0):
      return -100000000
    if len(black_moves) == 0 and len(black_king.get_checks() > 0):
      return 100000000

    # Draw
    if isWhite and len(white_moves) == 0:
      return 0
    if not isWhite and len(black_moves) == 0:
      return 0

    if isWhite:
      evals = []
      for move in white_moves:
        curr_pos, new_pos = move
        data = self.apply_move(curr_pos, new_pos)
        eval_val = self.minimax(all_moves_by_color, depth-1, not isWhite)
        evals.append(eval_val)
        self.undo_move(data)

      # Pick the best eval
