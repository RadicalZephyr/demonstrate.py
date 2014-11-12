#!/usr/bin/env python3

import sys, argparse
import pty


# Generator works with "with"
def readgen(fname):
    with open(fname, "r") as f:
        for line in f:
            yield line

def main(args):
    parser = argparse.ArgumentParser(description="Demonstrate commands on demand.")
    parser.add_argument('script', help='The script to draw commands from.')
    parser.add_argument('command', nargs='+',
                        help='The interpreter (including any arguments to it)'
                             'to run the lines from script in.')

    options = parser.parse_args(args)

    # pty.spawn(options.command)

if __name__ == "__main__":
    main(sys.argv[1:])
