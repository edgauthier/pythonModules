#!/usr/bin/python

import sys
import os
import hashlib
from datetime import datetime

# Display command line usage information.
def usage():
  print "\nUsage: dirHash.py <directory> [sha1|md5]\n"


# Handles processing when run from the command line.
def main(args):
  try:
    directory, hashAlg = processArguments(args)
  except ValueError:
    usage()
    return

  start = datetime.now();
  print "Starting: %s" % start

  printHashDigestForDirectoryContents(directory,hashAlg)

  finish = datetime.now()
  print "Finished: %s" % finish
  print "Total time: %s" % (finish - start)


# Process command line arguments and return as a tuple.
# Raises a ValueError exception if missing of invalid arguments.
#   First command line argument is the directory
#   Second (optional) command line argument is the hashing algorithm
def processArguments(args):

  directory = args[0]
  if not os.path.exists(directory):
    print "Directory doesn't exist: %s" % directory
    raise ValueError('Invalid Directory')

  # defaulting to sha1 for our hashing algorithm
  hashAlg = 'sha1'
  if len(args) > 1:
    hashAlg = args[1]

  if not hashAlg in ['md5','sha1']:
    print "Invalid hash algorithm: %s" % hashAlg
    raise ValueError('Invalid Hash Algorithm')

  return (directory, hashAlg)

# Prints the hash digests for all contents of a directory.
def printHashDigestForDirectoryContents(directory,hashAlg='sha1'):
  for fileName, hashDigest in getHashDigestForDirectoryContents(directory,hashAlg):
    print "%s|%s|%s" % (hashAlg,hashDigest,fileName)

# Generator function to return a tuple containing the file name (with
# path) and the hash digest for all contents of a directory.
def getHashDigestForDirectoryContents(directory,hashAlg='sha1'):
  for baseDir, dirs, files in os.walk(directory):
    for file in files:
      fileName = os.path.join(baseDir, file)
      yield (fileName, getHashDigestForFile(fileName,hashAlg))

# Returns the hash digest for a file in hex format.
def getHashDigestForFile(fileName, hashAlg='sha1', blockSize=2**8):
  try:
    f = open(fileName,'rb')
    h = hashlib.new(hashAlg)
    while True:
      data = f.read(blockSize)
      if not data:
        break
      h.update(data)
    f.close()
    return h.hexdigest()
  except:
    return "  *******  Error opening file! *******  "


# support running interactively as well as an imported module
if __name__ == '__main__':
  if len(sys.argv) < 2:
    usage()
    sys.exit(2)

  try:
    main(sys.argv[1:])
  except (KeyboardInterrupt, SystemExit):
    print "Exiting..."

