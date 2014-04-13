#!/usr/bin/env python
import re

LINE_REGEX = re.compile(r'^(\s*)(\d+\.\s+|\-\s+|\+\s+|\*\s+)?(.*)$')
SAMPLE_TEXT = """
6. Line 0
2. Line 1
    3. Sub-line 1
    - Sub-line with bullet
    Sub-line without prefix
        + Subline with plus
        * Subline with asterix
3. Line 2
"""

def main():
    input_string = SAMPLE_TEXT
    nested_list = parse_list(input_string)
    nested_list.set_prefix('1')
    output_string = str(nested_list)
    print output_string

def parse_list(list_string):
    input_lines = list_string.split('\n')
    nested_list = NestedList(None)
    stack = [(nested_list, -1)]
    for line in input_lines:
        if len(line.strip()) == 0: 
            continue # ignore empty lines
        match = LINE_REGEX.match(line)
        if not match: 
            raise ValueError('Line with unknown formatting: ' + line)
        cur_level = len(match.group(1))
        list_item = NestedList(line)
        while True:
            parent, level = stack[-1]
            if cur_level > level: 
                break
            del stack[-1]
        parent.children.append(list_item)
        stack.append((list_item, cur_level))
    return nested_list

class NestedList(object):

    def __init__(self, line):
        self.line = line
        self.children = []

    def __str__(self):
        output = ''
        if self.line != None:
            output = '{0}\n'.format(self.line)
        for child in self.children:
            output += '{0}'.format(child)
        return output

    def set_prefix(self, prefix):
        if self.line != None:
            self._set_prefix(prefix)
        child_prefix = prefix

        try:
            # if this is a number, reset back to 1 for the children
            int(child_prefix)
            child_prefix = 1
        except Exception:
            pass

        for child in self.children:
            child.set_prefix(child_prefix)
            try:
                child_prefix += 1
            except Exception:
                pass

    def _set_prefix(self, prefix):
        try:
            i = int(prefix)
            prefix = '{0}.'.format(prefix)
        except:
            pass
        repl_string = r'\g<1>' + prefix + r' \3'
        self.line = LINE_REGEX.sub(repl_string, self.line)

if __name__ == '__main__':
    main()


