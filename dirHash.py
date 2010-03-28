#!/usr/bin/python

import sys
import os
import hashlib
from datetime import datetime

# Display command line usage information.
def usage():
  print "Usage: dirHash.py <directory> [sha1|md5]"

def main(args):

  # get directory
  directory = args[0]

  # determine hashing algorithm - default to sha1
  hashAlg = 'sha1'
  if len(args) > 1:
    hashAlg = args[1]

  if not hashAlg in ['md5','sha1']:
    usage()
    return

  # make sure directory exists
  if not os.path.exists(directory):
    print "Directory doesn't exist: %s" % directory

  # log start time
  start = datetime.now();
  print "Starting: %s" % start

  # calculate hashes for all files in the directory
  hashDir(directory,hashAlg)

  # log finish time
  finish = datetime.now()
  print "Finished: %s" % finish
  print "Total time: %s" % (finish - start)

# Hash a directory with an optionally specified hash algorithm.
def hashDir(directory,hashAlg='sha1'):
  for baseDir, dirs, files in os.walk(directory):
    for file in files:
      fileName = os.path.join(baseDir, file)
      print "%s|%s|%s" % (hashAlg,getHashDigestForFile(fileName,hashAlg),fileName)


# Returns the hash digest for a file in hex format.
def getHashDigestForFile(fileName, hashAlg='sha1', blockSize=2**8):
  try:
    f = open(fileName,'rb')
  except:
    return "  *******  Error opening file! *******  "
  else:
    h = hashlib.new(hashAlg)
    while True:
      data = f.read(blockSize)
      if not data:
        break
      h.update(data)
    f.close()
    return h.hexdigest()


# support running interactively as well as an imported module
if __name__ == '__main__':
  if len(sys.argv) < 2:
    usage()
    sys.exit(2)

  try:
    main(sys.argv[1:])
  except (KeyboardInterrupt, SystemExit):
    print "Exiting..."

