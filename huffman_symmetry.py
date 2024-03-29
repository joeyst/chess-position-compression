
from utility import is_file_mirrored, huffman_encode_squares, board_metadata 
import chess 

def get_symmetry_squares_to_encode(board):
  """
  Gets a list of squares required to encode when using symmetry. 
  Only four squares in symmetric positions need to be encoded, otherwise all eight. 
  """
  squares = list(range(0, 32))
  not_mirror_file_indices = get_mirror_file_indices(board, flip=True)
  for file_index in not_mirror_file_indices:
    for rank_index in range(4, 8):
      squares.append(chess.square(file_index, rank_index))
  return squares

def get_mirror_file_indices(board, flip=False):
  """ Gets a list of files that are mirrored. """
  return [file_index for file_index in range(8) if is_file_mirrored(board, file_index) ^ flip]

def get_mirror_file_index_bits(board):
  """ Returns a string of bits. (8 bits.) """
  return "".join(["1" if file_index in get_mirror_file_indices(board) else "0" for file_index in range(8)])

def encode_board_to_huffman_symmetry(board):
  """
  Format: [board metadata] [mirror files] [huffman piece info] 
  78-181 bits = 24.5 bytes for standard chess game (worst case).
  Returns a string of bits. 
  """
  return board_metadata(board) + get_mirror_file_index_bits(board) + huffman_encode_squares(board, get_symmetry_squares_to_encode(board))

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
  