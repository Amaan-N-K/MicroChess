from board import *

piece_vals = {'k': 50, 'q': 9, 'r': 5, 'b': 3, 'n': 3, 'p': 1}
piece_move_multiplier = {'q': 0.2, 'r': 0.2, 'b': 0.1, 'n': 0.1}


def basic_eval(board: Board) -> int:
  white_val, black_val = 0, 0

  for piece, value in piece_vals.items():
    if piece.upper() in board.pieces:
      white_val += value * len(board.pieces[piece.upper()])
    if piece.lower() in board.pieces:
      black_val += value * len(board.pieces[piece.lower()])

  for piece, scale in piece_move_multiplier.items():
    if piece.upper() in board.pieces:
      white_val += sum(len(piece_instance.moves()) *
                       scale for piece_instance in board.get_piece(piece.upper()))
    if piece.lower() in board.pieces:
      black_val += sum(len(piece_instance.moves()) *
                       scale for piece_instance in board.get_piece(piece.lower()))

  if 'p' in board.pieces:
    for pawn in board.pieces['p']:
      black_val += pawn.get_pos()[0] * 0.3
  if 'P' in board.pieces:
    for pawn in board.pieces['P']:
      white_val += (board.row_size - 1 - pawn.get_pos()[0]) * 0.3

  if 'k' in board.pieces:
    for king in board.pieces['k']:
      king_vector = (king.get_pos()[0] ** 2 + king.get_pos()[1] ** 2) ** 0.5
      black_val += min(king_vector, abs(board.col_size - 1 - king_vector))
  if 'K' in board.pieces:
    for king in board.pieces['K']:
      king_vector = (king.get_pos()[0] ** 2 + king.get_pos()[1] ** 2) ** 0.5
      corner = (board.row_size - 1) ** 2 + (board.col_size - 1) ** 2
      white_val += min(abs(corner - king_vector),
                       abs(board.row_size - 1 - king_vector))

  # Return a value favoring white if positive, and black if negative
  return white_val - black_val
