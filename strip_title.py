#!/usr/bin/env python

import sys
import os

def strip_title_line(path):
    with open(path,'r') as f:
        lines = f.readlines()
        first_line = lines[0].rstrip()
        file_title,ext = os.path.splitext(os.path.basename(path))
        file_title = file_title.rstrip()

    if first_line == file_title:
        i = 1
        while not lines[i].rstrip():
            i += 1
        with open(path,'w') as f:
            f.writelines(lines[i:])

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Pass in a list of file paths"
    for p in sys.argv[1:]:
        strip_title_line(p)
