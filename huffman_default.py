
from utility import is_file_mirrored, huffman_encode_squares, board_metadata 
import chess 

def get_nondefault_squares_to_encode(board, flip=False):
  """
  Gets a list of squares that have not changed from default. 
  """
  default_board = chess.Board()
  squares = []
  for square in chess.SQUARES:
    # If it *is* a square with a default piece, ignore it. 
    if (board.piece_at(square) != default_board.piece_at(square)) ^ flip:
      squares.append(square)
  return squares 

def get_default_square_bits(board):
  """ Returns a string of bits. (64 bits.) """
  return "".join(["1" if square in get_nondefault_squares_to_encode(board, flip=True) else "0" for square in chess.SQUARES])

def encode_board_to_huffman_default(board):
  """
  Format: [board metadata] [default piece bits] [huffman piece info] 
  128-228 bits = 28.5 bytes for standard chess game (worst case).
  Returns a string of bits. 
  """
  return board_metadata(board) + get_default_square_bits(board) + huffman_encode_squares(board, get_nondefault_squares_to_encode(board))

if __name__ == "__main__":
  # Testing getting symmetry squares. 
  board = chess.Board()
  print(get_symmetry_squares_to_encode(board))
  print("len:", len(get_symmetry_squares_to_encode(board)))
  board.push_uci("e2e4")
  print(get_symmetry_squares_to_encode(board))
  print("len:", len(get_symmetry_squares_to_encode(board)))
  
  # Testing encode huffman symmetry. 
  print("Testing encode huffman symmetry.")
  print(encode_board_to_huffman_symmetry(chess.Board()))
  
