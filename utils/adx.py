#!/usr/bin/env python

import random

VOLUME = 10000

# notation: AdX, a = num of rolls, X = num of faces

def analyze(A, X):
    A = int(A)
    X = int(X)
    total = 0
    for i in range(0, VOLUME):
        dmg = A * random.randint(1, X)
        total += dmg
    return float(total) / float(VOLUME)

if __name__ == "__main__":
    def usage():
        print 'usage: ./adx.py AdX'

    import sys
    if len(sys.argv) <= 1 or len(sys.argv) == 'help':
        usage()
    else:
      tokens = sys.argv[1].split('d')
      print analyze(int(tokens[0]), int(tokens[1]))
 
