#!/usr/bin/env python3

import sys, os, argparse
import pty

# Generator works with "with"
def readgen(fname):
    with open(fname, "r") as f:
        for line in f:
            yield line

def make_reader(file):
    scriptgen = readgen(file)
    def read_file_or_input(stdin):
        data = os.read(stdin, 1024)

        if (data == "\n"):
            try:
                scriptdata = scriptgen.next()
                print("Returning: ", scriptdata)
                return scriptdata
            except StopIteration:
                pass

        print("Returning: ", data)
        return data

    return read_file_or_input

def main(args):
    parser = argparse.ArgumentParser(description="Demonstrate commands on demand.")
    parser.add_argument('script', help='The script to draw commands from.')
    parser.add_argument('command', nargs='+',
                        help='The interpreter (including any arguments to it)'
                             'to run the lines from script in.')

    options = parser.parse_args(args)

    script_reader = make_reader(options.script)

    pty.spawn(options.command, stdin_read=script_reader)

if __name__ == "__main__":
    main(sys.argv[1:])
