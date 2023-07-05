
from utility import is_file_mirrored, huffman_encode_squares, board_metadata 
import chess 

SQUARE_DIFS = {
  1:  "01",
  2:  "101",
  3:  "001",
  4:  "1111",
  5:  "1110",
  6:  "1100",
  7:  "1001",
  8:  "1000",
  9:  "11011",
  10: "00001",
  11: "110101",
  12: "000111",
  13: "000110",
  14: "000100",
  15: "000001",
  16: "1101000",
  17: "0001011",
  18: "0000000",
  19: "00010101",
  20: "00000011",
  21: "110100111",
  22: "110100101",
  23: "110100100",
  24: "000101000",
  25: "000000101",
  26: "1101001101",
  28: "0000001000",
  27: "11010011001",
  29: "11010011000",
  31: "00010100110",
  30: "00010100101",
  33: "00000010011",
  32: "000101001110",
  34: "000101001000",
  35: "0001010011110",
  37: "0001010010010",
  38: "0000001001010",
  36: "0000001001001",
  39: "0000001001000",
  40: "00010100111110",
  41: "00010100100110",
  43: "00000010010111",
  42: "000101001111111",
  46: "000000100101101",
  44: "000000100101100",
  49: "0001010010011111",
  45: "0001010011111100",
  48: "00010100111111011",
  51: "0001010010011100",
  47: "00010100100111011",
  50: "000101001001110101",
  53: "000101001001111000",
  55: "0001010010011110010",
  52: "0001010010011110011",
  54: "0001010010011110100",
  56: "0001010010011110101",
  57: "0001010010011110110",
  58: "0001010010011110111",
  59: "0001010011111101000",
  60: "0001010011111101001",
  61: "0001010011111101010",
  62: "0001010011111101011",
  63: "000101001001110100"
}

PIECE_CODES_U12 = {
  "R": "0001",
  "p": "11",
  "B": "00001",
  "K": "001",
  "b": "00000",
  "k": "010",
  "P": "10",
  "r": "0110",
  "N": "011100",
  "q": "011110",
  "n": "011101",
  "Q": "011111"
}

START_SQUARE_CODES = {
  0: "11110",
  1: "11010",
  2: "11100",
  3: "10111",
  4: "11111",
  5: "11001",
  6: "0010",
  7: "10010",
  8: "011",
  9: "0000",
  10: "11011",
  11: "10100",
  12: "10011",
  13: "0011",
  14: "1000",
  15: "01010",
  16: "11000",
  17: "01000",
  18: "111011",
  19: "101010",
  20: "111010",
  21: "10110",
  22: "01001",
  23: "000100",
  24: "010110",
  25: "000111",
  26: "0101111",
  27: "1010110",
  28: "0001011",
  29: "0001101",
  30: "0001100",
  31: "101011101",
  32: "101011110",
  33: "00010101",
  34: "01011101",
  35: "010111001",
  36: "101011111",
  37: "000101001",
  38: "0101110000",
  39: "0101110001011",
  40: "101011100111",
  41: "10101110010",
  42: "101011100110",
  43: "000101000",
  44: "01011100011",
  45: "1010111000",
  46: "01011100010100010",
  47: "010111000100",
  48: "01011100010100011",
  49: "01011100010100100",
  50: "01011100010100101",
  51: "01011100010100110",
  52: "01011100010100111",
  53: "01011100010101000",
  54: "01011100010101001",
  55: "01011100010101010",
  56: "01011100010101011",
  57: "01011100010101100",
  58: "01011100010101101",
  59: "01011100010101110",
  60: "01011100010101111",
  61: "0101110001010000" 
}

def huffman_encode_from_prev_and_curr_square(board, prev, curr):
  """ 
  Returns a string of bits. 
  """
  return SQUARE_DIFS[curr - prev] + PIECE_CODES_U12[board.piece_at(curr).symbol()]

def get_string_for_difs_and_pieces(board):
  occupied_squares = [square for square in chess.SQUARES if board.piece_at(square) is not None]
  start_square = occupied_squares[0]
  # Getting the starting square as a string of bits. 
  start_square_str = START_SQUARE_CODES[start_square]
  # Starting square piece 
  start_square_str += PIECE_CODES_U12[board.piece_at(start_square).symbol()]
  # Iterating through each pair of (prev, curr) squares.
  for prev, curr in zip(occupied_squares[:-1], occupied_squares[1:]):
    start_square_str += huffman_encode_from_prev_and_curr_square(board, prev, curr)
  return start_square_str

def get_number_of_pieces_on_board(board):
  return len(board.piece_map())

def get_number_of_pieces_on_board_as_binary_string(board):
  """ Returns four digit string of binary numbers. """
  return "{0:04b}".format(get_number_of_pieces_on_board(board))

def encode_board_to_huffman_piececentric(board):
  """
  Format: [board metadata] [huffman piece/square info]
  """
  return board_metadata(board) + get_number_of_pieces_on_board_as_binary_string(board) + get_string_for_difs_and_pieces(board)

if __name__ == "__main__":
  print(get_string_for_difs_and_pieces(chess.Board()))
  print(len(get_string_for_difs_and_pieces(chess.Board())) / 8)
  print(encode_board_to_huffman_piececentric(chess.Board()))
  print(len(encode_board_to_huffman_piececentric(chess.Board())) / 8)
  print(encode_board_to_huffman_piececentric(chess.Board()))
  
  # Testing binary string function. 
  print(get_number_of_pieces_on_board_as_binary_string(chess.Board()))
