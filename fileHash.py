#!/usr/bin/python

import sys
import os
import hashlib

# Display command line usage information.
def _usage():
  print "\nUsage: fileHash.py <fileName> [sha1|md5]\n"

# Handles processing when run from the command line.
def _main(args):
  try:
    fileName, hashAlg = _processArguments(args)
  except ValueError:
    _usage()
    return

  hashDigest = getHashDigestForFile(fileName, hashAlg)
  print "%s|%s|%s" % (hashAlg, hashDigest, fileName)


# Process command line arguments and return as a tuple.
# Raises a ValueError exception if missing of invalid arguments.
#   First command line argument is the filename
#   Second (optional) command line argument is the hashing algorithm
def _processArguments(args):
  fileName = args[0]
  if not os.path.exists(fileName):
    print "File doesn't exist: %s" % fileName
    raise ValueError('Invalid File')

  # defaulting to sha1 for our hashing algorithm
  hashAlg = 'sha1'
  if len(args) > 1:
    hashAlg = args[1]

  if not hashAlg in ['md5','sha1']:
    print "Invalid hash algorithm: %s" % hashAlg
    raise ValueError('Invalid Hash Algorithm')

  return (fileName, hashAlg)

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


# support running interactively as well as an imported module
if __name__ == '__main__':
  if len(sys.argv) < 2:
    _usage()
    sys.exit(2)

  try:
    _main(sys.argv[1:])
  except (KeyboardInterrupt, SystemExit):
    print "Exiting..."

