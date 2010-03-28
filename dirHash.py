#!/usr/bin/python

import sys
import os
import hashlib
from datetime import datetime

def usage():
  print "Usage: dirHash.py <source> [sha1|md5]"


def main(args):

  # get source
  source = args[0]

  # determine hashing algorithm
  hash = 'sha1'
  if len(args) > 1:
    hash = args[1]

  if not hash in ['md5','sha1']:
    usage()
    return

  # make sure source exists
  if not os.path.exists(source):
    print "Source doesn't exist: %s" % source

  # log start time
  start = datetime.now();
  print "Starting: %s" % start

  # calculate hashes for all files in the source
  hashDir(source,hash)

  # log finish time
  finish = datetime.now()
  print "Finished: %s" % finish
  print "Total time: %s" % (finish - start)


def hashDir(source,hash):
  for base, dirs, files in os.walk(source):
    for file in files:
      fileName = os.path.join(base, file)
      print "%s|%s|%s" % (hash,getHashForFile(fileName,hash),fileName)


def getHashForFile(fileName, hash='sha1', blockSize=2**8):
  try:
    f = open(fileName,'rb')
  except:
    return "  *******  Error opening file! *******  "
  else:
    h = hashlib.new(hash)
    while True:
      data = f.read(blockSize)
      if not data:
        break
      h.update(data)
    f.close()
    return h.hexdigest()


if __name__ == '__main__':
  if len(sys.argv) < 2:
    usage()
    sys.exit(2)

  try:
    main(sys.argv[1:])
  except (KeyboardInterrupt, SystemExit):
    print "Exiting..."

