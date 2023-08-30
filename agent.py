from board import Board


class Agent:
  def __init__(self, color: int, board: Board) -> None:
    self.color = color
    self.board = board
    self.info = None

  def get_color(self) -> int:
    return self.color

  def get_info(self) -> any:
    return self.info

  def set_info(self, info: any) -> None:
    self.info = info

  def my_king(self) -> any:
    return self.board.get_piece("K") if self.get_color() == 0 else self.board.get_piece("k")

  def get_move(self) -> list[int, tuple[int, int]]:
    raise NotImplementedError("This method must be ovverided by child classes")


class HumanAgent(Agent):
  def __init__(self, color: int, board: Board) -> None:
    super().__init__(color, board)

  def get_move(self) -> list[int, tuple[int, int]]:
    count = 0
    self.board.print_board()
    if self.get_info():
      print(self.get_info())
    while True:
      try:
        choice = input("Enter [OPTION] [row] [col] [row] [col]: ").split(" ")
        option = int(choice[0])
        curr_pos = (int(choice[1]), int(choice[2]))
        new_pos = (int(choice[3]), int(choice[4]))

        if not self.board.is_valid_pos(curr_pos) or not self.board.is_valid_pos(new_pos):
          print("Invalid choice -- try again")
          continue

        return [option, curr_pos, new_pos]

      except:
        print("Invalid choice -- try again")
        count += 1

      if count == 10:
        print("You are trolling")
        break
