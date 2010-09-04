#!/usr/bin/python

import sys
import os
from datetime import datetime
from fileHash import getHashDigestForFile

# Display command line usage information.
def _usage():
  print "\nUsage: dirHash.py <directory> [sha1|md5]\n"


# Handles processing when run from the command line.
def _main(args):
  try:
    directory, hashAlg = _processArguments(args)
  except ValueError:
    _usage()
    return

  start = datetime.now();
  print "Starting: %s" % start

  _printHashDigestForDirectoryContents(directory,hashAlg)

  finish = datetime.now()
  print "Finished: %s" % finish
  print "Total time: %s" % (finish - start)


# Process command line arguments and return as a tuple.
# Raises a ValueError exception if missing of invalid arguments.
#   First command line argument is the directory
#   Second (optional) command line argument is the hashing algorithm
def _processArguments(args):

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
def _printHashDigestForDirectoryContents(directory,hashAlg='sha1'):
  for fileName, hashDigest in getHashDigestForDirectoryContents(directory,hashAlg):
    print "%s|%s|%s" % (hashAlg,hashDigest,fileName)

# Generator function to return a tuple containing the file name (with
# path) and the hash digest for all contents of a directory.
def getHashDigestForDirectoryContents(directory,hashAlg='sha1'):
  for baseDir, dirs, files in os.walk(directory):
    for file in files:
      fileName = os.path.join(baseDir, file)
      yield (fileName, getHashDigestForFile(fileName,hashAlg))

# support running interactively as well as an imported module
if __name__ == '__main__':
  if len(sys.argv) < 2:
    _usage()
    sys.exit(2)

  try:
    _main(sys.argv[1:])
  except (KeyboardInterrupt, SystemExit):
    print "Exiting..."

