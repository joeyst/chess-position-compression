
from huffman import encode_board_to_huffman 
from huffman_symmetry import encode_board_to_huffman_symmetry 

def encode_board_to_huffman_best_opt(board):
  """
  Format [Opt?] [Rest of encoding] 
  """

  reg = encode_board_to_huffman(board)
  sym = encode_board_to_huffman_symmetry(board)
  if len(reg) < len(sym):
    return "0" + reg
  else:
    return "1" + sym
