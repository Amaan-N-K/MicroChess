from random import choice

from piece import *
from board import *


class Game:
  def __init__(self, p1, p2):
    self.board = Board()
    self.p1 = p1
    self.p2 = p2
  
  def apply_move(self, curr_pos, new_pos):
    self.board.get_cell_piece(curr_pos)
    self.board.move_piece(curr_pos, new_pos)    
  
  def is_game_over(self):
    

  def play(self):
    while not self.is_game_over():
      for player in [self.p1, self.p2]:
        curr_pos, new_pos = player.get_move(self.board)
        self.apply_move(curr_pos, new_pos)
        if self.is_game_over(): 
          break


class Agent:
  def __init__(self, board: Board, color):
    self.board = board
    self.color = color

  def make_move(self):
    raise NotImplementedError("This method must be ovverided by child classes")


class Random_Agent(Agent):
  def __init__(self, board: Board, color):
    super().__init__()

  def make_move(self):
    my_piece = choice(list(filter(lambda x: x.get_color() ==
                                  self.color, self.board.get_all_pieces())))
    my_move = choice(my_piece.get_legal_moves())
    self.board.move_piece(my_piece, my_move)
