
def get_fen_list(board_list):
  return [get_fen(board) for board in board_list]

def get_fen(board):
  return board.fen()

if __name__ == "__main__":
  from load_games import load_random_positions 
  print(get_fen_list(load_random_positions()))
