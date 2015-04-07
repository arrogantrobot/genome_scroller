#!/usr/bin/env python

import sys

chunk_size = 1024
lines_to_buffer = 100
class TextNozzleChrom:
  def __init__(self, source, line_width):
    self.line_width = line_width
    self.source = source
    self.char_queue = []
    self.chrom = "blah"
    self.open_file()
    self.readline_set_chrom()

  def open_file(self):
    self.fh = open(self.source, 'r')

  def read_from_queue(self):
    self.check_queue()
    return self.char_queue.pop(0)

  def get_line(self):
    return (self.chrom, "".join([ self.get_char(1) for x in range(self.line_width) ]))

  def get_char(self, v):
    if v == 0:
      return " "
    self.check_queue()
    char = self.read_from_queue()
    #while not char.isalpha():
    #  char = self.read_from_queue()
    return char
  
  def check_queue(self):
    if len(self.char_queue) == 0:
      self.recharge_queue()
    
  def recharge_queue(self):
    if self.fh.closed:
      self.open_file()
    self.char_queue = list(self.readline_set_chrom())

  def readline_set_chrom(self):
    line = self.fh.readline().strip()
    if line.startswith(">"):
      self.chrom = line[1:]
      print self.chrom
      line = self.readline_set_chrom()
    return line

if __name__ == "__main__":
    tn = TextNozzle(sys.argv[1], int(sys.argv[2])) 
    while True:
        print tn.get_line()
