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
    current_line = None
    end_of_file = False

    def read_file_or_input(stdin):
        nonlocal scriptgen
        nonlocal current_line
        nonlocal end_of_file

        data = os.read(stdin, 1024)

        if (current_line == None):
            try:
                current_line = next(scriptgen)
            except StopIteration:
                end_of_file = True

        if (not end_of_file):
            x = len(data)
            ret_data = current_line[:x]
            current_line = current_line[x:]
            data = ret_data

        # # This works to identify it, but will probably not be portable
        # # at all!!!
        # if (data == b"\r"):
        #     outfile.write(b"\\n")
        # else:
        #     outfile.write(data)

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
