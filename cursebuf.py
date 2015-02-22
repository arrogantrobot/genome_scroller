#!/usr/bin/env python

class cursebuf:
    def __init__(self, max_lines, lines):
        self.lines = [lines]
        self.max_lines = max_lines

    def get_line(self, line):
        return self.lines[line]

    def add_line(self, line):
        if len(self.lines) >= self.max_lines:
            self.lines.pop()
        self.lines.insert(0, line)

    def get_buf(self):
        return self.lines
