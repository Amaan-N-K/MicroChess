from flask import Flask, request, jsonify
from flask_cors import CORS
from agent import Agent
from board import Board
from game import Game
WHITE, BLACK = 0, 1
white_turn = True
app = Flask(__name__)
CORS(app, resources={r"/get_legal_moves/*": {"origins": "http://localhost:63342"},
                     r"/move": {"origins": "http://localhost:63342"}})


class FrontendAgent(Agent):
  def __init__(self, color: int, board: Board) -> None:
    super().__init__(color, board)


g = Game(FrontendAgent, FrontendAgent)

@app.route('/move', methods=['POST'])
def move():
    global white_turn
    data = request.json
    old_coor = data.get('old_coor')
    new_coor = data.get('new_coor')
    curr_pos = []
    new_pos = []
    for k in old_coor:
        curr_pos.append(int(old_coor[k]))
    for k in new_coor:
        new_pos.append(int(new_coor[k]))
    g.flask_move(curr_pos, new_pos)
    print(f"Moving piece from {old_coor} to {new_coor}")

    game_state = g.is_game_over(BLACK if white_turn else WHITE)
    print(game_state)
    if game_state[0]:
        winner_message = "Black wins!" if not white_turn else "White wins!"
        # If the game is over, send the king's position
        king_pos = g.board.pieces["k" if white_turn else "K"][0].get_pos()
        return jsonify({"game_over": True, "message": winner_message, "king_position": king_pos, "legal_moves": []}), 200

    white_turn = not white_turn

    return jsonify({"message": "Moved successfully"}), 200



@app.route('/get_legal_moves/<int:row>/<int:col>', methods=['GET'])
def get_legal_moves(row, col):
    piece = g.board.lookup((row, col))

    # Check if it's the correct color's turn
    if (piece.get_color() == WHITE and not white_turn) or (piece.get_color() == BLACK and white_turn):
        return jsonify({"error": "Not your turn!", "legal_moves": []}), 400

    # Calculate legal moves based on the given piece and position
    legal_moves = piece.moves()

    return jsonify({"legal_moves": legal_moves}), 200


if __name__ == "__main__":
  app.run(debug=True)
