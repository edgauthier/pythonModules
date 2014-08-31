#!/usr/bin/env python

import sys, os
from script_utils import get_password, run_command
from tempfile import NamedTemporaryFile
from time import sleep
from getpass import getpass

QPDF = '/usr/local/bin/qpdf'

def main():
    in_file = sys.argv[1]
    mtime = os.path.getmtime(in_file)
    # TODO test input file for access
    out_file =  get_temp_path()
    # TODO add validation to password method  throw exception if missing password
    password = get_password(account='encrypted_pdfs')
    if len(sys.argv) == 3:
        if sys.argv[2] == '-p':
            password = getpass('Password: ')
    cmd = '{} --decrypt --password={} "{}" "{}"'.format(QPDF, password, in_file, out_file)
    cmd_output = run_command(cmd)
    if len(cmd_output) > 0:
        # there was some sort of unexpected error
        print cmd_output
        os.unlink(out_file)
    else:
        # Move encrypted file to replace original file
        os.rename(out_file, in_file)
    os.utime(in_file, (mtime,mtime))
    sleep(1)

def get_temp_path():
    f = NamedTemporaryFile(delete=False)
    path = f.name
    f.close()
    return path

if __name__ == '__main__':
    if (len(sys.argv)) > 3:
        print "Usage: encrypt_pdf.py in_file [-p]"
        sys.exit(1)
    main()
