"""
This file is for the pieces
"""
from board import Board

class Piece():
  
  def __init__(self, color, pos, piece_type):
    """_summary_

    Args:
        color (str): 'B' or 'W' for black and white
        pos (List[int]): a list of length 2 containing row and col
        piece_type (str): str of piece
  
    """
    self.color = color
    self.pos = pos
    self.piece_type = piece_type
    self.legal_moves = self.get_legal_moves()

  
  def __str__(self):
    raise NotImplementedError("")
  # def calculate_moves(self, board, ):
     

  def set_pos(self, new_pos):
    """_summary_

    Args:
        new_pos (List[int]): _description_
    """
    self.pos = new_pos


  def remove_pos(self):
      self.pos = None

  def get_pos(self):
      return self.pos

  def get_color(self):
     return self.color
  
  def get_legal_moves(self, board):
    """_summary_

    Args:
        board (Board): _description_

    Raises:
        NotImplementedError: _description_
    """
    raise NotImplementedError

class King(Piece):
  def __init__(self):
    super().__init__()
  
  
class Knight(Piece):

  MOVE_OFFSETS  = [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]
  def __init__(self):
     super().__init__()
  
  def get_legal_moves(self, board):
    """_summary_

    Args:
        board (Board): _description_
    """

    curr_pos = self.pos

    legal_moves = []

    for offset in Knight.MOVE_OFFSETS:
       possible_pos = [curr_pos[0] + offset[0], curr_pos[1] + offset[1]]

       if not board.is_valid_location(possible_pos):
          continue
       elif board.get_cell_piece() is not None:
          continue
       elif board.get_cell_piece().get_color() == self.get_color():
          continue
       else:
          legal_moves.add(possible_pos)
  
        


       
       


    
  
class Pawn(Piece):
  def __init__(self):
     return 

class Queen(Piece):

class Rook(Piece):
  def __init__(self):
     return 

class Bishop(Piece):
  def __init__(self):
     return 
  
