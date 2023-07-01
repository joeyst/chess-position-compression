
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
