
"""
Used to test the various encoding schemes for their correctness, average size, and speed of encoding, decoding, and both. 
Encoding schemes: 
- FEN 
- Huffman 
  - Huffman w/o optimizations 
  - Huffman w/ symmetry optimization 
  - Huffman w/ default square optimization 
  - Huffman w/ blank rank/file optimization 
  - Huffman w/ piece-centric optimization 
Worth noting is, optimizations work better on some boards than others. E.g., if the sample has a lot of endgames, then 
piece-centric will likely perform well, while default square will perform poorly. 
Naturally, shorter move games will favor default square, so should try sampling longer games extra as one of the tests. 
"""

from load_games import load_random_positions, load_positions, load_games 
from huffman import encode_board_to_huffman 
from huffman_symmetry import encode_board_to_huffman_symmetry 
from fen import get_fen 

def test_average_size(fn, n=1000, factor=100):
  """ Returns the average size of the encoded boards. """ 
  return sum([len(fn(board)) for board in load_random_positions(n, factor)])/n

def print_averages(fn, n=1000, factor=10, iterations=10, divide_by=1):
  bit_sum = 0
  for _ in range(iterations):
    size_of_curr_position_compressed = test_average_size(fn, n, factor) / divide_by
    print(size_of_curr_position_compressed)
    bit_sum += size_of_curr_position_compressed
  print("Average: {}".format(bit_sum/iterations))

print("Huffman w/o optimizations")
print_averages(encode_board_to_huffman, divide_by=8)

print("FEN")
print_averages(get_fen)
