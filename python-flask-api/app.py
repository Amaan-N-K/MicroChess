from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:5500"])


@app.route('/move', methods=['POST'])
def move():
  data = request.json
  old_coor = data.get('old_coor')
  new_coor = data.get('new_coor')
  print(f"Moving piece from {old_coor} to {new_coor}")

  return jsonify({"message": "Moved successfully"}), 200


if __name__ == "__main__":
  app.run(debug=True)
