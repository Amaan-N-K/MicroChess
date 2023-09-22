from flask import Flask, request, jsonify
from flask_cors import CORS
from agent import Agent, MinimaxAgent
from board import Board
from game import Game
from evaluate import basic_eval
WHITE, BLACK = 0, 1
white_turn = True
app = Flask(__name__)
is_1v1 = True
minimax = False
move_count = 0

CORS(app, resources={
    r"/get_legal_moves/*": {"origins": "http://localhost:63342"},
    r"/move": {"origins": "http://localhost:63342"},
    r"/change_mode": {"origins": "http://localhost:63342"},
    r"/reset_game": {"origins": "http://localhost:63342"}
})


class FrontendAgent(Agent):
  def __init__(self, color: int, board: Board) -> None:
    super().__init__(color, board)


g = Game(FrontendAgent, FrontendAgent)

@app.route('/reset_game', methods=['POST'])
def reset_game():
    global g, white_turn, minimax
    white_turn = True

    g = Game(None, None)
    if not is_1v1:
        minimax = MinimaxAgent(1, g.board, basic_eval)
    return jsonify(message="Game state reset successfully!")

@app.route('/change_mode', methods=['GET'])
def change_mode():
    global is_1v1
    is_1v1 = not is_1v1
    return jsonify({"message": "Mode changed successfully"}), 200



@app.route('/move', methods=['POST'])
def move():
    global white_turn, move_count
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
    move_count += 1

    game_state = g.is_game_over(BLACK if white_turn else WHITE, move_count)
    king_pos = g.board.pieces["k" if white_turn else "K"][0].get_pos()
    if game_state[0]:
        winner_message = game_state[1]
        return jsonify({"game_over": True, "message": winner_message, "king_position": king_pos, "legal_moves": []}), 200

    checks = g.board.pieces["k" if white_turn else "K"][0].checks

    if len(checks) > 0:
        if is_1v1:
            white_turn = not white_turn
            return jsonify({"message": "Moved successfully", "in_check": True, "king_position": king_pos}), 200

    if not is_1v1:
        move_count += 1
        ai_king_pos = g.board.pieces["k"][0].get_pos()  # Get AI's king position
        ai_checks = g.board.pieces["k"][0].checks
        moves = minimax.get_move()
        curr_pos = moves[1]
        new_pos = moves[2]
        g.flask_move(curr_pos, new_pos)
        game_state = g.is_game_over(WHITE, move_count)
        print(game_state)

        # Check if Players king is in check after AI move
        white_king_pos = g.board.pieces["K"][0].get_pos()
        white_king_checks = g.board.pieces["K"][0].checks
        # Convert tuples to dictionaries for JSON serialization
        curr_pos_dict = {"row": curr_pos[0], "col": curr_pos[1]}
        new_pos_dict = {"row": new_pos[0], "col": new_pos[1]}

        # Return the move as structured JSON
        return jsonify({
            "message": "Moved successfully",
            "ai_move": {
                "old_coor": curr_pos_dict,
                "new_coor": new_pos_dict
            },
            "ai_in_check": len(ai_checks) > 0,  # True if AI king is in check
            "ai_king_position": ai_king_pos,  # Add the AI king's position here
            "ai_game_over": game_state[0],
            "result_message": game_state[1],
            "white_king_position": white_king_pos,
            "white_king_checks": len(white_king_checks) > 0

        }), 200

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
