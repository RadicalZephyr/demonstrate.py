#!/usr/bin/env python3

import sys, argparse
import pty

def main(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('script')
    parser.add_argument('command')

    options = parser.parse_args(args)


if __name__ == "__main__":
    main(sys.argv[1:])
