#!/usr/bin/python

import sys
import os
import hashlib

def usage():
  print "Usage: dirHash.py <source>"


def main(args):

  # get source
  source = args[0]

  # make sure source exists
  if not os.path.exists(source):
    print "Source doesn't exist: %s" % source

  # calculate hashes for all files in the source
  hashDir(source)


def hashDir(source):
  for base, dirs, files in os.walk(source):
    for file in files:
      fileName = os.path.join(base, file)
      print "%s|%s" % (getHashForFile(fileName),fileName)


def getHashForFile(fileName, blockSize=2**8):
  try:
    f = open(fileName,'rb')
  except:
    return "  *******  Error opening file! *******  "
  else:
    h = hashlib.sha1()
    while True:
      data = f.read(blockSize)
      if not data:
        break
      h.update(data)
    f.close()
    return h.hexdigest()


if __name__ == '__main__':
  if len(sys.argv) != 2:
    usage()
    sys.exit(2)

  try:
    main(sys.argv[1:])
  except (KeyboardInterrupt, SystemExit):
    print "Exiting..."

