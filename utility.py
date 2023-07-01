
import chess 

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
