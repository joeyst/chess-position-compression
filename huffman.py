
def en_passant(board):
  """
  [en passant] is 1-4 bits. 
    0     => Can en passant? 
    1..3? => Which file? 
  Returns a string of bits. 
  """
  if board.has_legal_en_passant():
    return "1" + bin(board.ep_square % 8)[2:].zfill(3)
  else:
    return "0"
  
def castling_rights(board):
  """ 
  [castling rights] is 4 bits. 
    0 => white kingside 
    1 => white queenside 
    2 => black kingside 
    3 => black queenside 
  Returns a string of bits. 
  """
  rights = ""
  rights += "1" if board.has_kingside_castling_rights(chess.WHITE) else "0"
  rights += "1" if board.has_queenside_castling_rights(chess.WHITE) else "0"
  rights += "1" if board.has_kingside_castling_rights(chess.BLACK) else "0"
  rights += "1" if board.has_queenside_castling_rights(chess.BLACK) else "0"
  return rights
  
def board_metadata(board):
  """
  6-9 bits. [turn] [castling rights] [en passant] 
  Returns a string of bits. 
  """
  return str(int(board.turn)) + castling_rights(board) + en_passant(board)

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
  import chess 
  def make_en_passant_position(file):
    board = chess.Board()
    # Won't work for h file. 
    board.push_uci("{}2{}4".format(chr(ord(file)+1), chr(ord(file)+1)))
    board.push_uci("h7h6")
    board.push_uci("{}4{}5".format(chr(ord(file)+1), chr(ord(file)+1)))
    board.push_uci("{}7{}5".format(file, file))
    return board

  print("Testing no en passant.")
  print(en_passant(chess.Board()))

  print("Testing en passant.")
  for file in "abcdefg":
    print("file {}:".format(file), en_passant(make_en_passant_position(file)))
    
  print("Testing castling rights.")
  print(castling_rights(chess.Board()))
  
  print("Testing board metadata.")
  print(board_metadata(chess.Board()))
  
  board = chess.Board()
  board.push_uci("e2e4")
  print(board_metadata(board))

  print("Testing huffman piece info.")
  print(huffman_piece_info(chess.Board()))
  
  print("Testing decode huffman piece info.")
  print(decode_huffman_piece_info(huffman_piece_info(chess.Board())))
  
  print("Testing encode huffman.")
  print(encode_huffman(chess.Board()))
  print("bits:", encode_huffman(chess.Board(), option='bits'))
  print("bytes:", encode_huffman(chess.Board(), option='bytes'))
  print(encode_huffman(chess.Board(), option='binary'))
