
def en_passant(board):
  """
  [en passant] is 1-4 bits. 
    0     => Can en passant? 
    1..3? => Which file? 
  Returns a string of bits. 
  """
  pass

def castling_rights(board):
  """ 
  [castling rights] is 4 bits. 
    0 => white kingside 
    1 => white queenside 
    2 => black kingside 
    3 => black queenside 
  Returns a string of bits. 
  """
  pass 
  
def board_metadata(board):
  """
  6-9 bits. [turn] [castling rights] [en passant] 
  Returns a string of bits. 
  """
  pass 

def huffman_piece_info(board):
  """
  64-164 bits for standard chess game. 
  Each piece is encoded as a sequence of bits from its Huffman code. 
  The Huffman codes are based on the starting position of chess. 
  Returns a string of bits. 
  """
  pass

def encode_huffman(board):
  """ 
  Format: [board metadata] [huffman piece info] 
  70-173 bits = 21.625 bytes for standard chess game (worst case). 
  Returns a string of bits. 
  """
  pass
  