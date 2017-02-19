#!/usr/bin/env python
from __future__ import print_function
import os
import sys
import math
import argparse
import itertools

parser = argparse.ArgumentParser(description='Round-robin some file lines.')

parser.add_argument('-n', '--count', dest='count', type=int, default=10,
                    help='number of output files')

parser.add_argument('input',
                    help='source file name')

def main(input, count):
    '''
    '''
    digits = math.ceil(math.log(count) / math.log(10))
    format = '{base}-{channel:0' + str(int(digits)) + '.0f}{ext}'

    print('Reading from', input, file=sys.stderr)

    with open(input) as infile:
        base, ext = os.path.splitext(input)
        names = [format.format(base=base, channel=i, ext=ext) for i in range(count)]
        files = [open(name, 'w') for name in names]
    
        print('Writing to', *names, file=sys.stderr)
    
        for (outfile, line) in zip(itertools.cycle(files), infile):
            outfile.write(line)
    
    for outfile in files:
        outfile.close()

if __name__ == '__main__':
    args = parser.parse_args()
    exit(main(args.input, args.count))
