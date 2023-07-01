
from huffman import encode_board_to_huffman 
from huffman_symmetry import encode_board_to_huffman_symmetry 
from huffman_default import encode_board_to_huffman_default 

def encode_board_to_huffman_best_opt(board):
  """
  Format [Opt?] [Rest of encoding] 
  """

  encoding_dict = {
    encode_board_to_huffman: "0",
    encode_board_to_huffman_symmetry: "10",
    encode_board_to_huffman_default: "110",
  }

  best_encode_fn = best_encode_fn_from_list(board, encoding_dict.keys())
  best_encoding = best_encode_fn(board)
    
  return encoding_dict[best_encode_fn] + best_encoding

def best_encode_fn_from_list(board, encoding_list):
  """
  Returns the best encoding from the list. 
  """
  return min(encoding_list, key=lambda encoding : len(encoding(board)))
