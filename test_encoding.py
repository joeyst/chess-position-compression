
"""
Used to test the various encoding schemes for their correctness, average size, and speed of encoding, decoding, and both. 
Encoding schemes: 
- FEN 
- Huffman 
  - (DONE) Huffman w/o optimizations 
  - (DONE) Huffman w/ symmetry optimization 
  - (DONE) Huffman w/ default square optimization 
  - Huffman w/ blank rank/file optimization 
  - (DONE) Huffman w/ piece-centric optimization 
Worth noting is, optimizations work better on some boards than others. E.g., if the sample has a lot of endgames, then 
piece-centric will likely perform well, while default square will perform poorly. 
Naturally, shorter move games will favor default square, so should try sampling longer games extra as one of the tests. 
"""

from load_games import load_random_positions, load_positions, load_games 
from huffman import encode_board_to_huffman 
from huffman_symmetry import encode_board_to_huffman_symmetry 
from fen import get_fen 
from choose_best_huffman_encoding import encode_board_to_huffman_best_opt 
from huffman_default import encode_board_to_huffman_default 
from huffman_piececentric import encode_board_to_huffman_piececentric 

def test_average_size(fn, n=1000, factor=100):
  """ Returns the average size of the encoded boards. """ 
  positions = load_random_positions(n, factor, unique=True)
  return sum([len(fn(board)) for board in positions])/len(positions)

def compare_huffmans(fns, n=1000, factor=100, truncate_len=10, divide_by=None):
  """
  Gets the list of sizes for each of the functions, and calculates 
  how many times each function beats each other function. 
  Prints permutations like: 
  79  | fn1 < fn2 < fn3
  21  | fn2 < fn1 < fn3 
  """
  if divide_by is None:
    divide_by = [1 for _ in range(len(fns))]
  res_dict = {}
  positions = load_random_positions(n, factor, unique=True)
  for (fn, divide_by) in list(zip(fns, divide_by)):
    res_dict[fn.__name__] = [len(fn(board))/divide_by for board in positions]

  better_dict = {} 
  
  for index in range(len(positions)):
    # Getting the functions in order by their size of this specific board. 
    ordered_fns = sorted(fns, key=lambda fn: res_dict[fn.__name__][index]) 
    # If the function name is too long, truncate it. 
    names = [fn.__name__ for fn in ordered_fns]
    for i in range(len(names)):
      if len(names[i]) > truncate_len:
        names[i] = names[i][len(names[i])-truncate_len:]
    dict_str = " < ".join(names)
    if dict_str not in better_dict:
      better_dict[dict_str] = 0
    better_dict[dict_str] += 1

  print("    BEST <" + ("-" * len(fns) * truncate_len) + "> WORST")
  # Sorting the dict by the number of times each permutation won. 
  for dict_str, count in sorted(better_dict.items(), key=lambda item: item[1], reverse=True):
    print("{:5} | {}".format(count, dict_str))
    
  return res_dict

def print_averages(fn, n=1000, factor=10, iterations=10, divide_by=1, verbose=True):
  bit_sum = 0
  bit_sums = []
  for _ in range(iterations):
    size_of_curr_position_compressed = test_average_size(fn, n, factor) / divide_by
    print(size_of_curr_position_compressed)
    bit_sum += size_of_curr_position_compressed
    bit_sums.append(size_of_curr_position_compressed)
  if verbose: 
    print("Average: {}".format(bit_sum/iterations))
  return bit_sums, bit_sum/iterations

def build_table_string(res_dict, iterations=10, column_size=30):
  table_string = "\n\n\n\n\n\n"
  for fn_name, (bit_sums, avg) in res_dict.items():
    table_string += fn_name[0:column_size-1] + " "*(column_size-min(len(fn_name), column_size-1)) + "| "
  table_string += "\n"
  for i in range(iterations):
    for fn_name, (bit_sums, avg) in res_dict.items():
      # If the fn name's current bit sum has been computed yet, add it. Otherwise, add space. 
      if i < len(bit_sums):
        table_string += str(bit_sums[i]) + " "*(column_size-len(str(bit_sums[i]))) + "| "
      else:
        table_string += " "*column_size + "| "
    table_string += "\n"
  
  table_string += "-"*((2+column_size)*len(res_dict)) + "\n"
  # Add the average row.
  for fn_name, (bit_sums, avg) in res_dict.items():
    # If the fn name's avg has been computed yet, add it. Otherwise, add space.
    if avg is None:
      table_string += " "*column_size + "| "
    else:
      table_string += str(avg) + " "*(column_size-len(str(avg))) + "| "

  return table_string

def print_as_table(fn_list, n=1000, factor=10, iterations=10, divide_by_list=None, column_size=30):
  """ 
  Prints the average size of the encoded boards for each function in fn_list. 
  fn_list is a list of functions. 
  """ 
  res_dict = {}
  for fn in fn_list:
    res_dict[fn.__name__] = ([], None)
  
  for (fn, divide_by) in list(zip(fn_list, divide_by_list)):
    bit_sums = []
    bit_sum = 0
    avg = None 
    for _ in range(iterations):
      size_of_curr_position_compressed = test_average_size(fn, n, factor) / divide_by
      bit_sum += size_of_curr_position_compressed
      bit_sums.append(size_of_curr_position_compressed)
      if len(bit_sums) == iterations:
        avg = bit_sum/iterations

      res_dict[fn.__name__] = (bit_sums, avg)
      print(build_table_string(res_dict, iterations, column_size))
      
fn_list = [get_fen, encode_board_to_huffman, encode_board_to_huffman_symmetry, encode_board_to_huffman_best_opt, encode_board_to_huffman_default, encode_board_to_huffman_piececentric]
divide_by = [1, 8, 8, 8, 8, 8]
# print_as_table(fn_list, n=100, divide_by_list=divide_by)

# print_as_table(fn_list, n=1000, divide_by_list=divide_by, iterations=10)
"""
res_dict = compare_huffmans(fn_list, divide_by=divide_by, n=3000, factor=10)
# Testing how many pieces on average are on the board. 
positions = load_random_positions(1000, 10, unique=True)
print(sum([len(board.piece_map()) for board in positions])/len(positions))
# Collecting frequencies 
freq_dict = {}
for board in positions:
  num_pieces = len(board.piece_map())
  if num_pieces not in freq_dict:
    freq_dict[num_pieces] = 0
  freq_dict[num_pieces] += 1
for num_pieces, count in sorted(freq_dict.items(), key=lambda item: item[0]):
  print("{}: {}".format(num_pieces, count))
# [0 - 10] [10 - 15] [15 - 20] [20 - 25] [25 - 32] via freq_dict 
for l, r in [(0, 10), (10, 15), (15, 20), (20, 25), (25, 32)]:
  print("From {} to {}: {}".format(l, r, sum([count for num_pieces, count in freq_dict.items() if l <= num_pieces < r])))

bucket_dict = {}
for fn_name, bytes_required_list in res_dict.items():
  bucket_dict[fn_name] = {}
  for bytes_required in bytes_required_list:
    if int(bytes_required) not in bucket_dict[fn_name]:
      bucket_dict[fn_name][int(bytes_required)] = 0
    bucket_dict[fn_name][int(bytes_required)] += 1
    
# Printing the bucket dict.
for fn_name, bytes_required_dict in bucket_dict.items():
  print("function:", fn_name)
  for bytes_required, count in sorted(bytes_required_dict.items(), key=lambda item: item[0]):
    print("{}: {} bytes: {}".format(fn_name, bytes_required, count))
"""
