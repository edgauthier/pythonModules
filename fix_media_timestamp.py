#!/usr/bin/env python

from PIL import Image
from PIL.ExifTags import TAGS
import sys
from datetime import datetime
import os
import time
from cr2 import GetDateTimeFromCR2

def main():
    if len(sys.argv) != 2:
        sys.exit(1)
    fname = sys.argv[1]
    process_file(fname)

def get_exif_data(fname):
    ret = {}
    try:
        img = Image.open(fname)
        if hasattr(img, '_getexif'):
            exifinfo = img._getexif()
            if exifinfo != None:
                for tag, value in exifinfo.items():
                    decoded = TAGS.get(tag, tag)
                    ret[decoded] = value
    except IOError:
        # print 'IOERROR getting exif data: ' + fname
        pass
    return ret

def get_exif_DateTimeOriginal(fname):
    exif_data = get_exif_data(fname)
    if 'DateTimeOriginal' in exif_data.keys():
        return datetime.strptime(exif_data['DateTimeOriginal'], '%Y:%m:%d %H:%M:%S')
    return None

def get_cr2_DateTimeOriginal(fname):
    cr2_datetime = GetDateTimeFromCR2(fname)
    if cr2_datetime != None:
        return datetime.strptime(cr2_datetime, '%Y:%m:%d %H:%M:%S')
    return None

def process_file(fname):
    timestamp = get_exif_DateTimeOriginal(fname)
    if timestamp == None:
        (_,ext) = os.path.splitext(fname)
        if str.lower(ext) == '.cr2':
            timestamp = get_cr2_DateTimeOriginal(fname)
    if timestamp != None:
        set_file_timestamp(fname, timestamp)

def set_file_timestamp(fname, timestamp):
    modtime = time.mktime(timestamp.timetuple())
    os.utime(fname, (modtime, modtime))

if __name__ == '__main__':
    main()
