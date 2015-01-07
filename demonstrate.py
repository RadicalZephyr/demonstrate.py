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
        self.done_char = b"\x04\x04"

    def ensure_current_line(self):
        if (self.current_line == None):
            try:
                # Try to skip blank lines
                while not self.current_line:
                    self.current_line = bytes(next(self.scriptgen)[:-1], "utf-8")
            except StopIteration:
                self.end_of_file = True


    def reset_line(self):
        # Reset the line for the next iteration
        if (len(self.current_line) == 0):
            self.current_line = None
            self.waiting_for_enter = True


    def random_file_read(self, datalen):
        x = datalen + random.randint(0, 3)
        ret_data = self.current_line[:x]
        self.current_line = self.current_line[x:]
        return ret_data


    def is_ctrl_d(self, data):
        return data == b"\x04"


    def is_enter(self, data):
        # This works to identify an "enter", but will probably not be portable
        # at all!!!
        return (data == b"\x0D") or (data == b"\x0A") or (data == b"\x0D\x0A")


    def read(self, stdin):
        data = os.read(stdin, 1024)
        print (data[0])
        if self.is_ctrl_d(data):
            return self.done_char

        if (self.waiting_for_enter):
            if self.is_enter(data):
                self.waiting_for_enter = False
                return data
            else:
                return None

        self.ensure_current_line()

        if (not self.end_of_file):

            data = self.random_file_read(len(data))

            if not data:
                data = None

            self.reset_line()

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
