from random import choice
from board import *


class Game:
  def __init__(self, p1, p2):
    self.p1 = p1
    self.p2 = p2
    self.board = p1.board
    self.moves = []
    self.half_move_count = 0
    self.full_move_count = 0

  def apply_move(self, curr_pos, new_pos):
    piece = self.board.get_cell_piece(curr_pos)
    piece_at_new_pos = self.board.get_cell_piece(new_pos)
    self.board.move_piece(piece, new_pos)
    return 1 if not piece_at_new_pos or piece is Pawn else 0

  def is_game_over(self, color) -> list:
    if color == "W":
      all_moves = self.board.all_moves_by_color('W')
      if len(all_moves) == 0 and len(self.board.w_king.get_checks()) > 1:
        return [True, 'W']
      elif len(all_moves) == 0:
        return [True, 'D']
      else:
        return [False]
    else:
      all_moves = self.board.all_moves_by_color('B')

      if len(all_moves) == 0 and len(self.board.b_king.get_checks()) > 1:
        return [True, 'B']
      elif len(all_moves) == 0:
        return [True, 'D']
      else:
        return [False]

  def play(self):
    # while not game_state[0]:
    #   for player in [self.p1, self.p2]:
    #     turn = player.color
    #     curr_pos, new_pos = player.get_move()
    #     self.apply_move(curr_pos, new_pos)
    #     game_state = self.is_game_over(turn)
    #     if game_state[0]:
    #       break
    #
    #   turn = self.p1.color
    #   game_state = self.is_game_over(turn)
    #
    # return game_state[1]

        # if move_type == 0:
        #   self.half_move_count += 1
        # else:
        #   self.half_move_count = 0


      # self.full_move_count += 1
    while True:
      game_state = self.one_round()
      if game_state[0]:
        return 'Result:' + game_state[1]

  def one_round(self):
    for player in [self.p1, self.p2]:
      game_state = self.is_game_over(player.color)
      if game_state[0]:
        return game_state
      curr_pos, new_pos = player.get_move()
      self.apply_move(curr_pos, new_pos)


  def promote(self, pawn):
    """Takes agent input on what piece to promote the pawn to

    Args:
        pawn (Piece): The chess piece pawn that is to be promoted
    """
    pawn_color = pawn.get_color()
    pawn_pos = pawn.get_pos()

    print("What piece would you like to promote to:\n1. Queen\n2. Knight\n3. Rook\n4. Bishop")
    promotion_choice = input("Input the number of your choice: ")

    try:
      promotion_choice = int(promotion_choice)

      if not 1 <= promotion_choice <= 4:
        print("Invalid choice. Try again.")
        return

      self.board._remove_piece(pawn)
      if promotion_choice == 1:
        new_piece = Queen(pawn_color, pawn_pos)
      elif promotion_choice == 2:
        new_piece = Knight(pawn_color, pawn_pos)
      elif promotion_choice == 3:
        new_piece = Rook(pawn_color, pawn_pos)
      elif promotion_choice == 4:
        new_piece = Bishop(pawn_color, pawn_pos)

      self.board._place_piece(new_piece, new_piece.get_pos())

      print(f"Piece promoted to {str(new_piece)}")

    except ValueError:
      print("Invalid input. Must be a number between 1 and 4.")


class Agent:
  def __init__(self, board: Board, color):
    self.board = board
    self.color = color

  def get_move(self):
    raise NotImplementedError("This method must be ovverided by child classes")


class Random_Agent(Agent):
  def __init__(self, board: Board, color):
    super().__init__(board, color)

  def get_move(self):
    my_piece = choice(list(filter(lambda x: x.get_color() ==
                                  self.color, self.board.get_all_pieces())))
    my_move = choice(my_piece.get_legal_moves())
    self.board.move_piece(my_piece, my_move)


class Human_Agent(Agent):
  def __init__(self, board: Board, color):
    super().__init__(board, color)

  def get_move(self):
    count = 0
    self.board.print_board()
    print("###################################")
    while True:
      try:
        curr_pos = input("Enter the [row col] of the piece to move").split(" ")
        curr_pos[0] = int(curr_pos[0])
        curr_pos[1] = int(curr_pos[1])

        piece = self.board.get_cell_piece(curr_pos)
        piece_legal_moves = piece.get_legal_moves(self.board)
        if piece.get_color() != self.color:
          print(f"You can not move the other colors pieces")
          continue
        print(f"You chose to move: {str(piece)}")
        print(f"It can move to locations: {piece_legal_moves}")
        new_pos = input("Enter the [row col] to move the piece").split(" ")
        new_pos[0] = int(new_pos[0])
        new_pos[1] = int(new_pos[1])

        if new_pos not in piece_legal_moves:
          print("Invalid choice -- try again")

        return [curr_pos, new_pos]

      except:
        print("Invalid choice -- try again")
        count += 1

      if count == 10:
        print("You are trolling")
        break
