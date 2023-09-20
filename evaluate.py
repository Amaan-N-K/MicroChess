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

  white_piece_val = white_val
  black_piece_val = black_val

  if 'r' in board.pieces:
    for rook in board.pieces['r']:
      black_val += len(rook.moves()) * 0.2
  if 'R' in board.pieces:
    for rook in board.pieces['R']:
      white_val += len(rook.moves()) * 0.2

  if 'q' in board.pieces:
    for queen in board.pieces['q']:
      black_val += len(queen.moves()) * 0.2
  if 'Q' in board.pieces:
    for queen in board.pieces['q']:
      white_val += len(queen.moves()) * 0.2

  if 'n' in board.pieces:
    for knight in board.pieces['n']:
      black_val += len(knight.moves()) * 0.1
  if 'N' in board.pieces:
    for knight in board.pieces['N']:
      white_val += len(knight.moves()) * 0.1

  if 'b' in board.pieces:
    for bishop in board.pieces['b']:
      black_val += len(bishop.moves()) * 0.1
  if 'B' in board.pieces:
    for bishop in board.pieces['B']:
      white_val += len(bishop.moves()) * 0.1

  if 'p' in board.pieces:
    for pawn in board.pieces['p']:
      black_val += pawn.get_pos()[0] * 0.3
  if 'P' in board.pieces:
    for pawn in board.pieces['P']:
      white_val += (board.row_size - 1 - pawn.get_pos()[0]) * 0.3

  if 'k' in board.pieces:
    for king in board.pieces['k']:
      moves = king.moves()
      if black_piece_val >= 52 and len(moves) == 0:
        white_val += 5
      elif black_piece_val <= 51:
        white_val += int(4 * 1/len(moves))
  if 'K' in board.pieces:
    for king in board.pieces['K']:
      moves = king.moves()
      if white_piece_val >= 52 and len(moves) == 0:
        black_val += 5
      elif black_piece_val <= 51:
        black_val += int(4 * 1/len(moves))




  # Return a value favoring white if positive, and black if negative
  return white_val - black_val
