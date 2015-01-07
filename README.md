Demonstrate.py
--------------

[![Made at Hacker School](http://img.shields.io/badge/Made_At-Hacker_School-brightgreen.svg)](https://www.hackerschool.com)

Yet another demonstrate project. This one uses pseudo terminals, so
the prompt for the interpreter doesn't need to be faked. Also, the
input of each line is fake typed a la
[hacker typer](http://hackertyper.com/).

After the full line has been "typed" the script will silently eat
input until the enter key is pressed. Blank lines in the script file
will be silently ignored.

You can also switch into "input mode" at any time by hitting the `ESC`
key. This means you can then use whatever line editing facilities your
scripts interpreter provides (like readline hopefully), and type any
ad-libbed commands needed.  When you want to go back to demonstrating
mode press `ESC` again.

Once all of the lines of input from the file have been consumed, the
interpreter will keep running until it's fed two end of lines
(i.e. `ctrl-d`'s). I think it takes two because one signals EOF to the
background process and one signals EOF to the current python process.


An Example
==========

There are several demonstration scripts in the `scripts`
directory. They're not very interesting actually...

    ./demonstrate.py scripts/shscript sh


# WARNING

This script is PROBABLY NOT PORTABLE. I wrote it on a Mac, and the
logic for looking for the enter key being pressed looks exactly for
the byte `0x0D` a.k.a. `13` a.k.a. `\r` a.k.a. ASCII character `DC3`.
This is clearly what my terminal sends, but it might not be true for
yours...
