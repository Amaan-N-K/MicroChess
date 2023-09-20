from flask import Flask, request, jsonify
from flask_cors import CORS
from agent import Agent
from board import Board
from game import Game

app = Flask(__name__)
CORS(app, resources={r"/get_legal_moves/*": {"origins": "http://localhost:63342"},
                     r"/move": {"origins": "http://localhost:63342"}})


class FrontendAgent(Agent):
  def __init__(self, color: int, board: Board) -> None:
    super().__init__(color, board)


g = Game(FrontendAgent, FrontendAgent)

@app.route('/move', methods=['POST'])
def move():
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

    g.board.print_board()

    return jsonify({"message": "Moved successfully"}), 200



@app.route('/get_legal_moves/<int:row>/<int:col>', methods=['GET'])
def get_legal_moves(row, col):
    # Call a function to calculate legal moves based on the given piece and position
    piece = g.board.lookup((row, col))
    print(piece)
    print(row, col)
    legal_moves = piece.moves()
    print(legal_moves)

    return jsonify({"legal_moves": legal_moves}), 200


if __name__ == "__main__":
  app.run(debug=True)
