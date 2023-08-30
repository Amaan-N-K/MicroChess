from board import *

piece_values = {'k': 1000, 'q': 9, 'r': 5, 'b': 3, 'n': 3, 'p': 1}


def basic_evaluate(board: Board) -> int:
    white_pieces_value = 0
    black_piece_value = 0
    for piece in piece_values:
        if piece.isupper() in board.pieces:
            white_pieces_value += len(board.pieces[piece.isupper()]) * piece_values[piece]
        if piece in board.pieces:
            black_piece_value -= len(board.pieces[piece]) * piece_values[piece]

    if 'r' in board.pieces:
        for rook in board.pieces['r']:
            black_piece_value -= len(rook.moves()) * 0.2
    if 'R' in board.pieces:
        for rook in board.pieces['R']:
            white_pieces_value += len(rook.moves()) * 0.2

    if 'q' in board.pieces:
        for queen in board.pieces['q']:
            black_piece_value -= len(queen.moves()) * 0.2
    if 'Q' in board.pieces:
        for queen in board.pieces['q']:
            white_pieces_value += len(queen.moves()) * 0.2

    if 'n' in board.pieces:
        for knight in board.pieces['n']:
            black_piece_value -= len(knight.moves()) * 0.1
    if 'N' in board.pieces:
        for knight in board.pieces['N']:
            white_pieces_value += len(knight.moves()) * 0.1

    if 'b' in board.pieces:
        for bishop in board.pieces['b']:
            black_piece_value -= len(bishop.moves()) * 0.1
    if 'B' in board.pieces:
        for bishop in board.pieces['B']:
            white_pieces_value += len(bishop.moves()) * 0.1

    if 'p' in board.pieces:
        for pawn in board.pieces['p']:
            black_piece_value -= pawn.get_pos()[0] * 0.3
    if 'P' in board.pieces:
        for pawn in board.pieces['P']:
            white_pieces_value += board.row_size - pawn.get_pos()[0] * 0.3

    if 'k' in board.pieces:
        for king in board.pieces['k']:
            king.checks_and_pins()
            black_piece_value += len(king.get_checks()) + len(king.get_pins())
            king_vector = (king.get_pos()[0] ** 2 + king.get_pos()[1] ** 2) ** 0.5
            black_piece_value += min(king_vector, abs(board.col_size - 1 - king_vector))
    if 'K' in board.pieces:
        for king in board.pieces['K']:
            king.checks_and_pins()
            white_pieces_value -= len(king.get_checks()) + len(king.get_pins())
            king_vector = (king.get_pos()[0] ** 2 + king.get_pos()[1] ** 2) ** 0.5
            corner = (board.row_size - 1 ** 2 + board.col_size - 1 ** 2)
            white_pieces_value -= min(abs(corner - king_vector), abs(board.row_size - 1 - king_vector))

    return white_pieces_value + black_piece_value


