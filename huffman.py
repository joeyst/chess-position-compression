
import chess 
from utility import board_metadata, huffman_encode_squares, decode_huffman_piece_info 

def huffman_piece_info(board):
  """
  64-164 bits for standard chess game. 
  Each piece is encoded as a sequence of bits from its Huffman code. 
  The Huffman codes are based on the starting position of chess. 
  Returns a string of bits. 
  """
  return huffman_encode_squares(board)

def return_num_bits(string):
  return len(string)

def return_num_bytes(string):
  return len(string)/8

def return_binary(string):
  return int(string, 2)

CALLBACK_DICT = {
  "bits": return_num_bits,
  "bytes": return_num_bytes,
  "binary": return_binary
}

def encode_board_to_huffman(board, option=None):
  """ 
  Format: [board metadata] [huffman piece info] 
  70-173 bits = 21.625 bytes for standard chess game (worst case). 
  Returns a string of bits. 
  """
  if option is not None:
    return CALLBACK_DICT[option](encode_board_to_huffman(board))
    
  return board_metadata(board) + huffman_piece_info(board) 
  
if __name__ == "__main__":

  print("Testing huffman piece info.")
  print(huffman_piece_info(chess.Board()))
  
  print("Testing decode huffman piece info.")
  print(decode_huffman_piece_info(huffman_piece_info(chess.Board())))
  
  print("Testing encode huffman.")
  print(encode_board_to_huffman(chess.Board()))
  print("bits:", encode_board_to_huffman(chess.Board(), option='bits'))
  print("bytes:", encode_board_to_huffman(chess.Board(), option='bytes'))
  print(encode_board_to_huffman(chess.Board(), option='binary'))
  
  # Testing mirror. 
  board = chess.Board()
  print(board)
  board = board.mirror()
  print(board)
  board = chess.Board()
  board.push_uci("e2e4")
  print(board)
  board = board.mirror()
  print(board)
