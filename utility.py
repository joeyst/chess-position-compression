
import chess 

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

def huffman_encode_square(board, square):
  if board.piece_at(square) is None:
    return HUFFMAN_CODES["s"]
  else:
    return HUFFMAN_CODES[board.piece_at(square).symbol()]

def huffman_encode_squares(board, squares=None):
  """
  Gets the huffman encoding of the pieces at the provided list of squares. 
  If squares is None, encodes the whole board. 
  Returns a string of bits. 
  """
  if squares is None:
    squares = chess.SQUARES 

  return "".join([huffman_encode_square(board, square) for square in squares])

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

def is_file_mirrored(board, file_index):
  """
  Returns if the file is mirrored. 
  """
  board_mirror = board.mirror() 
  for rank_index in range(4):
    square = chess.square(file_index, rank_index)
    # If the piece type or piece color isn't the same, then it's not mirrored. 
    piece1 = board.piece_at(square)
    piece2 = board_mirror.piece_at(square)
    if piece1 is None and piece2 is None:
      continue

    _1None_2NotNone = piece1 is None and piece2 is not None 
    _1NotNone_2None = piece1 is not None and piece2 is None
    if _1None_2NotNone or _1NotNone_2None:
      return False

    different_types = board.piece_at(square).piece_type != board_mirror.piece_at(square).piece_type
    different_color = board.piece_at(square).color != board_mirror.piece_at(square).color
    if different_types or different_color:
      return False
  return True

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

if __name__ == "__main__":
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

  # Testing is file mirrored. 
  board = chess.Board()
  print("is_file_mirrored:", is_file_mirrored(board, 0))
  board.push_uci("e2e4")
  print("is_file_mirrored:", is_file_mirrored(board, 0))
  print("is_file_mirrored:", is_file_mirrored(board, 4))
