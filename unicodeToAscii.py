#!/usr/bin/env python

import sys,codecs
from datetime import datetime

def die(msg):
  print msg
  sys.exit()

if len(sys.argv) != 3: die("Missing parameters")

start = datetime.now()
try:
  input = codecs.open(sys.argv[1], encoding="utf-16")
  output = open(sys.argv[2], "w")
  for line in input:
    output.write(line)
except IOError:
  die("can't open file")
except KeyboardInterrupt:
  print "Cancelling..."
finish = datetime.now()

print "Total time {0}".format(finish - start)
