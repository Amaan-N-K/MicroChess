from board import Board


class Agent:
  def __init__(self, color: int, board: Board) -> None:
    self.color = color
    self.board = board

  def get_color(self) -> int:
    return self.color

  def my_king(self) -> any:
    return self.board.get_piece("K") if self.get_color() == 0 else self.board.get_piece("k")

  def get_move(self) -> list[tuple[int, int]]:
    raise NotImplementedError("This method must be ovverided by child classes")


class HumanAgent(Agent):
  def __init__(self, color: int, board: Board) -> None:
    super().__init__(color, board)

  def get_move(self) -> list[tuple[int, int]]:
    count = 0
    print("###################################")
    self.board.print_board()
    while True:
      try:
        curr_pos = input(
            "Enter the [row col] of the piece to move: ").split(" ")
        curr_pos[0] = int(curr_pos[0])
        curr_pos[1] = int(curr_pos[1])
        curr_pos = tuple(curr_pos)
        if not self.board.is_valid_pos(curr_pos):
          continue

        piece = self.board.lookup(curr_pos)
        print(f"You chose to move: {str(piece)}")

        new_pos = input("Enter the [row col] to move the piece: ").split(" ")
        new_pos[0] = int(new_pos[0])
        new_pos[1] = int(new_pos[1])
        new_pos = tuple(new_pos)

        if not self.board.is_valid_pos(new_pos):
          continue

        return [curr_pos, new_pos]

      except:
        print("Invalid choice -- try again")
        count += 1

      if count == 10:
        print("You are trolling")
        break
