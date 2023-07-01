
import chess 
from utility import board_metadata 

HUFFMAN_CODES = {
  "s": "1",
  "p": "011", 
  "P": "010", 
  "r": "00111", 
  "R": "00110",
  "n": "00101",
  "N": "00100",
  "b": "00011",
  "B": "00010",
  "q": "000011",
  "Q": "000010",
  "k": "000001",
  "K": "000000"
}

def huffman_piece_info(board):
  """
  64-164 bits for standard chess game. 
  Each piece is encoded as a sequence of bits from its Huffman code. 
  The Huffman codes are based on the starting position of chess. 
  Returns a string of bits. 
  """
  info = ""
  for square in chess.SQUARES:
    piece = board.piece_at(square)
    if piece is None:
      info += HUFFMAN_CODES["s"]
    else:
      info += HUFFMAN_CODES[piece.symbol()]
  return info

def decode_huffman_piece_info(info):
  """ Takes in a string of bits and returns a list of pieces and/or Nones. """
  tuples = []
  while info:
    for symbol, code in HUFFMAN_CODES.items():
      if info.startswith(code):
        if symbol == "s":
          tuples.append(None)
        else:
          tuples.append(chess.Piece.from_symbol(symbol))
        info = info[len(code):]
  return tuples

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

def encode_huffman(board, option=None):
  """ 
  Format: [board metadata] [huffman piece info] 
  70-173 bits = 21.625 bytes for standard chess game (worst case). 
  Returns a string of bits. 
  """
  if option is not None:
    return CALLBACK_DICT[option](encode_huffman(board))
    
  return board_metadata(board) + huffman_piece_info(board) 
  
if __name__ == "__main__":

  print("Testing huffman piece info.")
  print(huffman_piece_info(chess.Board()))
  
  print("Testing decode huffman piece info.")
  print(decode_huffman_piece_info(huffman_piece_info(chess.Board())))
  
  print("Testing encode huffman.")
  print(encode_huffman(chess.Board()))
  print("bits:", encode_huffman(chess.Board(), option='bits'))
  print("bytes:", encode_huffman(chess.Board(), option='bytes'))
  print(encode_huffman(chess.Board(), option='binary'))
  
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
