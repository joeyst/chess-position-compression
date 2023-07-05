
"""
Script for sampling games and finding the most common differences in distance between 
occupied squares. 
E.g., with a board of 
0 0 0 
0 1 0 
0 0 1, 
there is only one difference, which is 4. 
This will be used for Huffman coding the deltas. 
"""

import chess 
def get_differences(board): 
  """ Returns a list of differences between occupied squares. """ 
  squares = [square for square in chess.SQUARES if board.piece_at(square) is not None]
  return [abs(squares[i] - squares[i + 1]) for i in range(len(squares) - 1)]

def get_differences_dict(board):
  """ Returns a dict of differences between occupied squares. """ 
  difs_list = get_differences(board)
  difs_dict = {}
  for dif in difs_list:
    if dif not in difs_dict:
      difs_dict[dif] = 0
    difs_dict[dif] += 1
  return difs_dict 

def get_differences_dict_from_board_list(board_list):
  difs_dict = {} 
  for board in board_list:
    tmp_difs_dict = get_differences_dict(board)
    for dif in tmp_difs_dict:
      difs_dict[dif] = difs_dict.get(dif, 0) + tmp_difs_dict[dif]
  return sorted(difs_dict.items(), key=lambda item: item[1], reverse=True)

"""
print(get_differences(chess.Board()))
print(get_differences_dict(chess.Board()))
print(get_differences_dict_from_board_list([chess.Board() for _ in range(10)]))
"""
MAKE_RANDOM = False
if MAKE_RANDOM: 
  from load_games import load_random_positions 
  NUM_POSS = 50000
  FACTOR = 10
  rand_positions = load_random_positions(NUM_POSS, factor=FACTOR, unique=True)
  # Filtering to positions with 12 pieces or fewer. 
  NUM_PIECES = 12
  rand_positions = [pos for pos in rand_positions if len([square for square in chess.SQUARES if pos.piece_at(square) is not None]) <= NUM_PIECES]
  prop_satis = len(rand_positions) / NUM_POSS 
  print("Proportion of positions with {} pieces or fewer: {}".format(NUM_PIECES, prop_satis))

RUN = False
if RUN:
  num_difs = get_differences_dict_from_board_list(rand_positions)
  print(num_difs)

  cum_difs = {}
  curr_cum = 0
  for count in dict(num_difs).keys():
    if count in dict(num_difs).keys():
      curr_cum += dict(num_difs)[count]
      cum_difs[count] = curr_cum 

  cum_difs = sorted(cum_difs.items(), key=lambda item: item[1], reverse=False)
  # Printing 
  print("Differences between occupied squares:")
  for dif, count in num_difs[0:20]:
    # Max 3 spaces | count 
    print("{:3} | {}".format(dif, count))
    
  print("Cumulative differences between occupied squares:")
  for dif, count in cum_difs[0:20]:
    print("{:3} | {}".format(dif, count))

  noncum_percentages = {}
  for dif, count in num_difs[0:20]:
    noncum_percentages[dif] = count / max(dict(cum_difs).values())
  noncum_percentages = sorted(noncum_percentages.items(), key=lambda item: item[1], reverse=True)
    
  print("Non-cumulative percentages:")
  for dif, count in noncum_percentages[0:20]:
    print("{:3} | {}".format(dif, count))
    
  print("Cumulative percentages:")
  for dif, count in cum_difs[0:20]:
    print("{:3} | {}".format(dif, count / max(dict(cum_difs).values())))

def huffman_code_difs(dif_freq_dict, verbose=False, defaults=True):
  """
  Returns a dictionary of Huffman codes for the differences. 
  Differences are given in the form: {dif: freq, ...}, where dif is an int and freq is an int. 
  First, for any int in the range 1..=63, if it's not in the dict, it's added with a frequency of 1. 
  This is used to ensure that *any* possible encoding is possible. (2 kings are guaranteed to be on the board.) 
  Next, greedy huffman coding is done, creating new "nodes" in the node_dict that have as values: [node|int, node|int, freq] 
  to represent the node's children and its total frequency. 
  """
  dif_freq_dict = dict(dif_freq_dict)
  # Ensuring that all possible differences are in the dict. 
  if defaults:
    for i in range(1, 64):
      if i not in dif_freq_dict:
        dif_freq_dict[i] = 1

  finished_dict = {}
  unfinished_dict = dict(dif_freq_dict)
  
  if verbose:
    print("Dif freq dict:")
    for key, value in dif_freq_dict.items():
      print("{}: {}".format(key, value))

  def extract_two_lowest(dct):
    """ Returns the two lowest frequencies in dct. """
    return sorted(dct.items(), key=lambda item: item[1])[0:2]
  
  while len(unfinished_dict.keys()) > 1:
    # Find the two lowest frequencies. 
    two_lowest = extract_two_lowest(unfinished_dict) 
    # print("two lowest:", two_lowest)
    del unfinished_dict[two_lowest[0][0]]
    del unfinished_dict[two_lowest[1][0]]
    new_node_key = "{},{}".format(two_lowest[0][0], two_lowest[1][0])
    new_node_value = [two_lowest[0][0], two_lowest[1][0], two_lowest[0][1] + two_lowest[1][1]]
    finished_dict[new_node_key] = new_node_value
    unfinished_dict[new_node_key] = new_node_value[2]
    
  # Decoding finished_dict 
  
  # First, sorting the dictionary from most frequent to least frequent. 
  finished_dict = sorted(finished_dict.items(), key=lambda item: item[1][2], reverse=True)
  node_strs = {}
  def get_parent(node):
    """ Returns the parent of node. """
    for node_str, node_value in finished_dict:
      if node in node_value[0:2]:
        return node_str, node_value.index(node)
    return None 
  
  for node_str, node_value in finished_dict:
    if get_parent(node_str) is None:
      node_strs[node_str] = ""
      
  # while there is a node not in the node_strs dict: 
  while len(node_strs.keys()) < len(finished_dict): 
    for node_str, node_value in finished_dict:
      if node_str not in node_strs:
        # If the parent isn't in node_strs, just continue. 
        if get_parent(node_str)[0] not in node_strs:
          continue
        
        # Otherwise, set the node_str to the parent_str + the index of the node in the parent.
        node_strs[node_str] = node_strs[get_parent(node_str)[0]] + str(get_parent(node_str)[1])
  
  # Finally, for the original keys, get their huffman codes. 
  key_codes = {} 
  for key, value in dif_freq_dict.items():
    # finished_dict: {node_name: [l-child, r-child, freq], ...}
    # node_strs    : {node_name: "010", ...}
    # dif_freq_dict: {int_name : 10}
    # So, get the item in finished_dict that has as a l-child or r-child the int_name from dif_freq_dict 
    parent_code, ind = get_parent(key) 
    key_codes[key] = node_strs[parent_code] + str(ind)
    
  if verbose:
    print("Key codes:")
    for key, value in key_codes.items():
      print("{}: {}".format(key, value))
  
  return sorted(key_codes.items(), key=lambda item: item[0])
    
if RUN:
  # huffman_code_difs({1: 1, 2: 2, 3: 1, 4: 3, 5: 0}, verbose=True)
  # With actual vals: 
  res = huffman_code_difs(dict(num_difs), verbose=True)
  hc_digits_reqed = 0

  for dif, code in res:
    hc_digits_reqed += len(code) * dict(num_difs).get(dif, 0)
    
  print("Huffman coding digits required: {}".format(hc_digits_reqed))
  six_bits_reqed = 0

  for dif, code in res:
    six_bits_reqed += 6 * dict(num_difs).get(dif, 0)
    
  print("Six bits required: {}".format(six_bits_reqed))
  total_difs = 0

  for dif, code in res:
    total_difs += dict(num_difs).get(dif, 0)
    
  print("Total difs: {}".format(total_difs))
  print("HC/total avg: {}".format(hc_digits_reqed / total_difs))

  # Getting the average number of each piece across games with 12 pieces or fewer. 
  piece_sums = {}
  for board in rand_positions:
    for piece in board.piece_map().values():
      if piece.symbol() not in piece_sums:
        piece_sums[piece.symbol()] = 0
      piece_sums[piece.symbol()] += 1
      
  print("Piece sums:")
  for piece, count in piece_sums.items():
    print("{}: {}".format(piece, count))

piece_stats = {
  "R": 3197, 
  "p": 15022, 
  "B": 1441, 
  "K": 6330, 
  "b": 1347, 
  "k": 6330, 
  "P": 14610, 
  "r": 3345, 
  "N": 865, 
  "q": 984, 
  "n": 932, 
  "Q": 1058 
}

total_pieces = sum(piece_stats.values())
for piece, count in sorted(piece_stats.items(), key=lambda item: item[1], reverse=True):
  print("{}: {}".format(piece, count / piece_stats['k']))

print(huffman_code_difs(piece_stats, verbose=True, defaults=False))
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

IF_START_SQUARE = False 

if IF_START_SQUARE:
  # Getting the most common start square out of 60000 random positions. 
  from load_games import load_random_positions
  positions = load_random_positions(60000, 1, unique=True) 
  # Keeping only positions with 12 pieces or fewer.
  positions = [pos for pos in positions if len([square for square in chess.SQUARES if pos.piece_at(square) is not None]) <= 12]
  start_squares = {}
  for board in positions:
    for square in chess.SQUARES:
      if board.piece_at(square) is not None:
        if square not in start_squares:
          start_squares[square] = 0
        start_squares[square] += 1
        break

  for i in range(0, 6000, 100):
    print(positions[i])

  print("Start squares:")
  for square, count in sorted(start_squares.items(), key=lambda item: item[1], reverse=True):
    print("{}: {}".format(square, count))
  
start_square_freqs = {
  8: 871,
  14: 448,
  13: 410,
  6: 390,
  9: 361,
  4: 352,
  0: 336,
  2: 297,
  10: 292,
  1: 284,
  5: 283,
  16: 281,
  3: 267,
  21: 265,
  11: 248,
  12: 244,
  7: 241,
  15: 219,
  22: 211,
  17: 204,
  18: 159,
  20: 152,
  19: 128,
  24: 108,
  25: 105,
  23: 85,
  27: 61,
  26: 60,
  28: 48,
  30: 48,
  29: 48,
  34: 30,
  33: 22,
  36: 20,
  32: 19,
  31: 16,
  35: 15,
  37: 11,
  43: 10,
  45: 7,
  38: 6,
  44: 4,
  41: 4,
  42: 2,
  40: 2,
  39: 1,
  47: 1
}

for i in range(0, 62):
  if i not in start_square_freqs:
    start_square_freqs[i] = 0
    
print("Start square huffman codes:")
ss_codes = huffman_code_difs(start_square_freqs, verbose=True, defaults=False)
for square, code in sorted(ss_codes, key=lambda item: item[0]):
  print("{}: {}".format(square, code))
