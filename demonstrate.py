#!/usr/bin/env python3

import sys, os, argparse
import random
import mypty


class HackerReader:

    def __init__(self):
        pass

    def read(self, stdin):
        data = os.read(stdin, 1024)
        return data


# Generator works with "with"
def readgen(fname):
    with open(fname, "r") as f:
        for line in f:
            yield line

# This would be a class, because making a closure like this is sort of
# awkward in Python.  I said "would" because as it turns out, when I
# try to pass a class or class function as the function
def make_reader(file):

    reader = HackerReader()
    # scriptgen = readgen(file)
    # current_line = None
    # end_of_file = False
    # waiting_for_enter = False

    def read_file_or_input(stdin):
        # nonlocal scriptgen
        # nonlocal current_line
        # nonlocal end_of_file
        # nonlocal waiting_for_enter
        nonlocal reader
        return reader.read(stdin)

        # # # This works to identify an "enter", but will probably not be portable
        # # # at all!!!
        # if (waiting_for_enter):
        #     if (data == b"\x0D"):
        #         waiting_for_enter = False
        #         return data
        #     else:
        #         return None

        # if (current_line == None):
        #     try:
        #         # Try to skip blank lines
        #         while not current_line:
        #             current_line = bytes(next(scriptgen)[:-1], "utf-8")
        #     except StopIteration:
        #         end_of_file = True

        # if (not end_of_file):
        #     x = len(data) + random.randint(0, 3)
        #     ret_data = current_line[:x]
        #     current_line = current_line[x:]
        #     data = ret_data

        #     if not data:
        #         data = None

        #     # Reset the line for the next iteration
        #     if (len(current_line) == 0):
        #         current_line = None
        #         waiting_for_enter = True

        # return data

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
