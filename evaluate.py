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

  white_piece_count = white_val - 50
  black_piece_count = black_val - 50

  if 'r' in board.pieces:
    for rook in board.pieces['r']:
      black_val -= len(rook.moves()) * 0.2
  if 'R' in board.pieces:
    for rook in board.pieces['R']:
      white_val += len(rook.moves()) * 0.2

  if 'q' in board.pieces:
    for queen in board.pieces['q']:
      black_val -= len(queen.moves()) * 0.2
  if 'Q' in board.pieces:
    for queen in board.pieces['q']:
      white_val += len(queen.moves()) * 0.2


  if 'n' in board.pieces:
    for knight in board.pieces['n']:
      black_val -= len(knight.moves()) * 0.1
  if 'N' in board.pieces:
    for knight in board.pieces['N']:
      white_val += len(knight.moves()) * 0.1

  if 'b' in board.pieces:
    for bishop in board.pieces['b']:
      black_val -= len(bishop.moves()) * 0.1
  if 'B' in board.pieces:
    for bishop in board.pieces['B']:
      white_val += len(bishop.moves()) * 0.1


  if 'p' in board.pieces:
    for pawn in board.pieces['p']:
      black_val += pawn.get_pos()[0] * 0.3
  if 'P' in board.pieces:
    for pawn in board.pieces['P']:
      white_val += (board.row_size - 1 - pawn.get_pos()[0]) * 0.3

  # if 'k' in board.pieces:
  #   for king in board.pieces['k']:
  #     if white_piece_count > 9:
  #       king_vector = (king.get_pos()[0] ** 2 + king.get_pos()[1] ** 2) ** 0.5
  #       black_val += min(king_vector, abs(board.col_size - 1 - king_vector))
  # if 'K' in board.pieces:
  #   for king in board.pieces['K']:
  #     if black_piece_count > 9:
  #       king_vector = (king.get_pos()[0] ** 2 + king.get_pos()[1] ** 2) ** 0.5
  #       corner = (board.row_size - 1) ** 2 + (board.col_size - 1) ** 2
  #       white_val += min(abs(corner - king_vector),
  #                        abs(board.row_size - 1 - king_vector))

  # Return a value favoring white if positive, and black if negative
  return white_val - black_val
