
import chess.pgn 
import random 
from env import path 

def load_random_positions(n=1000, factor=100):
  """ 
  Loads n random positions. 
  Factor is the chance of a given position being used. 
  """ 
  pgn = open(path)
  positions = []
  while len(positions) < n:
    game = chess.pgn.read_game(pgn)
    board = game.board()
    for move in game.mainline_moves():
      board.push(move)
      if random.randint(0, factor) == 0:
        positions.append(board.copy())
      if len(positions) >= n:
        break
  return positions 

def load_positions(n=1000):
  """ Loads first n positions. """ 
  pgn = open(path)
  positions = []
  while len(positions) < n:
    game = chess.pgn.read_game(pgn)
    board = game.board()
    for move in game.mainline_moves():
      board.push(move)
      positions.append(board.copy())
      if len(positions) >= n:
        break
  return positions 

def load_games(n=1000):
  """ Loads first n games. """ 
  pgn = open(path)
  games = []
  for i in range(n):
    game = chess.pgn.read_game(pgn)
    games.append(game)
  return games

if __name__ == "__main__":
  for pos in load_positions():
    print(pos)
