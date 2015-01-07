#!/usr/bin/env python3

import sys, os, argparse
import random
import mypty


# Generator works with "with"
def readgen(fname):
    with open(fname, "r") as f:
        for line in f:
            yield line

class HackerReader:

    def __init__(self, fname):
        self.fname = fname
        self.scriptgen = readgen(fname)
        self.current_line = None
        self.end_of_file = False
        self.waiting_for_enter = False

    def read(self, stdin):
        data = os.read(stdin, 1024)

        # This works to identify an "enter", but will probably not be portable
        # at all!!!
        if (waiting_for_enter):
            if (data == b"\x0D"):
                waiting_for_enter = False
                return data
            else:
                return None

        if (current_line == None):
            try:
                # Try to skip blank lines
                while not current_line:
                    current_line = bytes(next(scriptgen)[:-1], "utf-8")
            except StopIteration:
                end_of_file = True

        if (not end_of_file):
            x = len(data) + random.randint(0, 3)
            ret_data = current_line[:x]
            current_line = current_line[x:]
            data = ret_data

            if not data:
                data = None

            # Reset the line for the next iteration
            if (len(current_line) == 0):
                current_line = None
                waiting_for_enter = True

        return data

def make_reader(file):

    reader = HackerReader(file)

    def read_file_or_input(stdin):
        nonlocal reader
        return reader.read(stdin)


    return read_file_or_input

def main(args):
    parser = argparse.ArgumentParser(description="Demonstrate commands on demand.")
    parser.add_argument('script', help='The script to draw commands from.')
    parser.add_argument('command', nargs='+',
                        help='The interpreter (including any arguments to it)'
                             'to run the lines from script in.')

    options = parser.parse_args(args)

    script_reader = make_reader(options.script)

    mypty.spawn(options.command, stdin_read=script_reader)

if __name__ == "__main__":
    main(sys.argv[1:])
