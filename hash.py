#!/usr/bin/python

import sys
import os
import hashlib
from datetime import datetime


# Returns the hash digest for a file in hex format.
# Set blockSize to adjust size of data read in and hashed while
# processing the file.
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


# Generator function to return a tuple containing the file name (with
# path) and the hash digest for all contents of a directory.
def getHashDigestForDirectoryContents(directory,hashAlg='sha1'):
  for baseDir, dirs, files in os.walk(directory):
    for file in files:
      fileName = os.path.join(baseDir, file)
      yield (fileName, getHashDigestForFile(fileName,hashAlg))


# Process command line arguments and return as a tuple.
# Raises a ValueError exception if missing of invalid arguments.
#   First command line argument is the filename
#   Second (optional) command line argument is the hashing algorithm
def _processArguments(args):
  path = args[0]
  if not os.path.exists(path):
    print "Path doesn't exist: %s" % path
    raise ValueError('Invalid Path')

  # defaulting to sha1 for our hashing algorithm
  hashAlg = 'sha1'
  if len(args) > 1:
    hashAlg = args[1]

  if not hashAlg in ['md5','sha1']:
    print "Invalid hash algorithm: %s" % hashAlg
    raise ValueError('Invalid Hash Algorithm')

  return (path, hashAlg)


def _printHashDigestForPath(path, hashAlg='sha1'):
    if os.path.isfile(path):
      hashDigest = getHashDigestForFile(path, hashAlg)
      _printHashDigestForFile(hashAlg, hashDigest, path)
    else:
      _printHashDigestForDirectoryContents(path, hashAlg)
        

# Prints the hash digests for all contents of a directory.
def _printHashDigestForDirectoryContents(directory,hashAlg='sha1'):
  for fileName, hashDigest in getHashDigestForDirectoryContents(directory,hashAlg):
    _printHashDigestForFile(hashAlg, hashDigest, fileName)


def _printHashDigestForFile(hashAlg, hashDigest, fileName):
  print "%s | %s | %s" % (hashAlg,hashDigest,fileName)


# Display command line usage information.
def _usage():
  print "\nUsage: hash.py <path> [sha1|md5]\n"


# Handles processing when run from the command line.
def _main(args):
  try:
    path, hashAlg = _processArguments(args)
  except ValueError:
    _usage()
    return

  start = datetime.now();
  print "\nStarting: %s\n" % start

  _printHashDigestForPath(path,hashAlg)  

  finish = datetime.now()
  print "\nFinished: %s" % finish
  print "Total time: %s\n" % (finish - start)


# support running interactively as well as an imported module
if __name__ == '__main__':
  if len(sys.argv) < 2:
    _usage()
    sys.exit(2)

  try:
    _main(sys.argv[1:])
  except (KeyboardInterrupt, SystemExit):
    print "Exiting..."

