#!/usr/bin/python

import sys
import os
from datetime import datetime
from fileHash import getHashDigestForFile
from urlparse import urlparse
import posixpath
from urllib import urlretrieve

# Display command line usage information.
def _usage():
  print "\nUsage: downloadTest.py <url> [count]\n"

#TODO expose keepFiles flag
def _downloadAndHashFiles(url, count, keepFiles=False):
  baseFileName,fileExt = _extractFileNameAndExt(url)
  hashes = {}

  try:
    for i in range(count):
      downloadName = "{0}-{1}{2}".format(baseFileName, i+1, fileExt)
      hashes[downloadName] = _downloadAndHashFile(url, downloadName, keepFiles)
  except (KeyboardInterrupt):
    print "\r\nDownload canceled.\r\n"

  print "\r\nIntegrity Report"
  for fileName in sorted(hashes):
    print "{0}|{1}".format(fileName, hashes[fileName])

def _downloadAndHashFile(url, fileName, keepFile=False):
  print "Downloading {0}...".format(fileName)
  _downloadFile(url, fileName)
  if os.path.exists(fileName):
    result = getHashDigestForFile(fileName)
    if not keepFile:
      os.remove(fileName)
  else:
    result = "File not downloaded"
  return result

def _extractFileNameAndExt(url):
  filePath = urlparse(url)[2]
  fileName = posixpath.basename(filePath)
  baseFileName, fileExt = posixpath.splitext(fileName)
  return (baseFileName, fileExt)

def _downloadFile(url, fileName):
  urlretrieve(url, fileName, _downloadProgress)
  # print an extra line after the download progress
  print ""

def _downloadProgress(blockCount, blockSize, totalSize):
  percentage = int(((1.0 * blockCount * blockSize) / totalSize) * 100)
  percentage = 100 if percentage > 100.0 else percentage
  print "{0:>3}%\r".format(percentage),

# Handles processing when run from the command line.
def _main(args):
  try:
    url, count = _processArguments(args)
  except ValueError:
    _usage()
    return

  start = datetime.now();
  print "\r\nStarting: %s\r\n" % start
  
  _downloadAndHashFiles(url, count)

  finish = datetime.now()
  print "\r\nFinished: %s" % finish
  print "Total time: %s\r\n" % (finish - start)

# Process command line arguments and return as a tuple.
# Raises a ValueError exception if missing of invalid arguments.
#   First command line argument is the url
#   Second (optional) command line argument is the number of times to
#   downoad the file at the url
def _processArguments(args):
  url = args[0]
  #TODO validate URL

  # defaulting to sha1 for our hashing algorithm
  count = 5 
  if len(args) > 1:
    try:  
      count = int(args[1])
    except ValueError:
      count = 0
    
  if count <= 0:
    print "Please enter a valid count greater than 0."
    raise ValueError('Invalid Count')

  return (url, count)

# support running interactively as well as an imported module
if __name__ == '__main__':
  if len(sys.argv) < 2:
    _usage()
    sys.exit(2)

  try:
    _main(sys.argv[1:])
  except (KeyboardInterrupt, SystemExit):
    print "Exiting..."

