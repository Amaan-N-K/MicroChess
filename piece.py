"""
Chess piece implementations
"""
from board import Board


class Piece:
  def __init__(self, color, pos):
    """Initialize piece 

    Args:
        color (str): 'B' or 'W' for black and white
        pos (List[int]): A 2-element list of [row, col]
        piece_type (str): String representation of piece by FEN 
    """
    self.color = color 
    self.pos = pos
    self.piece_type = None

  def __str__(self):
    if self.piece_type == None:
      raise NotImplementedError("This piece is not yet defined")
    return self.piece_type

  def set_pos(self, new_pos):
    self.pos = new_pos

  def remove_pos(self):
    self.pos = None

  def get_pos(self):
    return self.pos

  def get_color(self):
    return self.color

  def get_legal_moves(self, board):
    """Return a list of legal piece moves

    Args:
        board (Board): Board object

    Raises:
        NotImplementedError: Method should be overrided by children classes
    """
    raise NotImplementedError


class King(Piece):
  MOVE_OFFSETS = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
  def __init__(self, color, pos):
    super().__init__(color, pos)
    self.piece_type = "K" if self.color == "W" else "k"
  
  def get_legal_moves(self, board, opposite_pieces):
    """_summary_

    Args:
        board (_type_): _description_
        opposite_pieces (List[Piece]): _description_
    """
    curr_pos = self.pos
    legal_moves = set()

    for offset in King.MOVE_OFFSETS:
      possible_pos = [curr_pos[0] + offset[0], curr_pos[1] + offset[1]]

      if not board.is_valid_location(possible_pos):
        continue
      elif board.get_cell_piece(possible_pos).get_color() == self.get_color():
        continue
      elif any(possible_pos in p.get_legal_moves for p in opposite_pieces):
        continue
      else:
        legal_moves.add(possible_pos)

class Knight(Piece):
  MOVE_OFFSETS = [(1, 2), (1, -2), (-1, 2), (-1, -2),
                  (2, 1), (2, -1), (-2, 1), (-2, -1)]

  def __init__(self, color, pos):
    super().__init__(color, pos)
    self.piece_type = "N" if self.color == "W" else "n"

  def get_legal_moves(self, board):
    curr_pos = self.get_pos()
    legal_moves = set()

    for offset in Knight.MOVE_OFFSETS:
      possible_pos = [curr_pos[0] + offset[0], curr_pos[1] + offset[1]]

      if not board.is_valid_location(possible_pos):
        continue
      elif board.get_cell_piece(possible_pos).get_color() == self.get_color():
        continue
      else:
        legal_moves.add(possible_pos)

    return legal_moves


class Pawn(Piece):
  def __init__(self, color, pos):
    super().__init__(color, pos)
    self.piece_type = "P" if self.color == "W" else "p"

  def get_legal_moves(self, board):
    legal_moves = set()
    vertical_direction = -1 if self.get_color() == "W" else 1
    curr_pos = self.get_pos()

    # One forward
    forward_move = [curr_pos[0] + vertical_direction, curr_pos[1]]
    if board.is_valid_location(forward_move) and board.is_cell_empty(forward_move):
      legal_moves.add(forward_move)

    # Capture moves (diagonal)
    diagonal_moves = [
        [curr_pos[0] + vertical_direction, curr_pos[1] - 1],
        [curr_pos[0] + vertical_direction, curr_pos[1] + 1]
    ]

    for move in diagonal_moves:
      if board.is_valid_location(move):
        piece_at_cell = board.get_cell_piece(move)
        if piece_at_cell and piece_at_cell.get_color() != self.get_color():
          legal_moves.add(move)

    return legal_moves

  def promote(self):
    print("What piece would you like to promote to:\n1. Queen\n2. Knight\n3. Rook\n4. Bishop")
    promotion_choice = input("Input the number of your choice: ")

    try:
      promotion_choice = int(promotion_choice)

      if not 1 <= promotion_choice <= 4:
        print("Invalid choice. Try again.")
        return

      if promotion_choice == 1:
        new_piece_type = "Q" if self.get_color() == "W" else "q"
      elif promotion_choice == 2:
        new_piece_type = "N" if self.get_color() == "W" else "n"
      elif promotion_choice == 3:
        new_piece_type = "R" if self.get_color() == "W" else "r"
      elif promotion_choice == 4:
        new_piece_type = "B" if self.get_color() == "W" else "b"

      self.change_piece_type(new_piece_type)
      print(f"Piece promoted to {new_piece_type}")

    except ValueError:
      print("Invalid input. Must be a number between 1 and 4.")

    def change_piece_type(self, new_piece_type):
      self.piece_type = new_piece_type


class Sliding_Piece(Piece):
  def __init__(self, color, pos):
    super().__init__(color, pos)

  def get_legal_moves(self, board, move_offsets):
    curr_pos = self.get_pos()
    legal_moves = set()

    for offset in move_offsets:
      possible_pos = [curr_pos[0] + offset[0], curr_pos[1] + offset[1]]

      while board.is_valid_location(possible_pos):
        piece_at_cell = board.get_cell_piece(possible_pos)
        if piece_at_cell == None:
          legal_moves.add(possible_pos)
          possible_pos[0] += offset[0]
          possible_pos[1] += offset[1]
        elif piece_at_cell.get_color() != self.get_color():
          legal_moves.add(possible_pos)
          break
        else:
          break

    return legal_moves


class Queen(Sliding_Piece):
  MOVE_OFFSETS = [(1, 0), (0, 1), (-1, 0), (0, -1),
                  (1, 1), (1, -1), (-1, 1), (-1, -1)]

  def __init__(self, color, pos):
    super().__init__(color, pos)
    self.piece_type = "Q" if self.color == "W" else "q"

  def get_legal_moves(self, board):
    return super().get_legal_moves(board, Queen.MOVE_OFFSETS)


class Rook(Piece):
  MOVE_OFFSETS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

  def __init__(self, color, pos):
    super().__init__(color, pos)
    self.piece_type = "R" if self.color == "W" else "r"

  def get_legal_moves(self, board):
    return super().get_legal_moves(board, Rook.MOVE_OFFSETS)


class Bishop(Piece):
  MOVE_OFFSETS = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

  def __init__(self, color, pos):
    super().__init__(color, pos)
    self.piece_type = "B" if self.color == "w" else "b"

  def get_legal_moves(self, board):
    return super().get_legal_moves(board, Bishop.MOVE_OFFSETS)
