#!/usr/bin/python

import sys
import getopt
import urllib
import urllib2
import cookielib
import getpass
import os

class PinboardExporter(object):
    """Logs into pinboard.in and exports bookmarks in various formats."""
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self._connect()
    
    def export_bookmarks(self, bookmark_formats = set(['json']), directory = os.getcwd()):
        """Exports bookmarks in each of the formats specified"""
        # sanitize formats - these will be used directly
        formats = PinboardExporter._VALID_FORMATS & bookmark_formats
        for f in formats: self._download_bookmarks(directory, f)

    def _connect(self):
        """Connects to the pinboard.in website."""
        cj = cookielib.CookieJar()
        self.site = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        login_data = urllib.urlencode({'username' : self.username, 'password' : self.password})
        self.site.open(PinboardExporter._LOGIN_PAGE, login_data)
        #TODO test if the login succeeded

    def _download_bookmarks(self, directory, bookmark_format):
        """Downloads pinboard bookmarks in a given format"""
        export_page = PinboardExporter._EXPORT_BASE_PAGE + bookmark_format + '/'
        export_file = 'bookmarks.' + bookmark_format
        export_path = os.path.join(directory, export_file)
        with open(export_path, 'w') as output:
            resp = self.site.open(export_page)
            output.writelines(resp)

    _LOGIN_PAGE = 'https://pinboard.in/auth/'
    _EXPORT_BASE_PAGE = 'http://pinboard.in/export/format:'
    _VALID_FORMATS = set(['html', 'json', 'xml'])

def usage():
    print """
    Usage: pinboardExport.py OPTIONS

    OPTIONS:

        -h | --help

        -u <username> | --username <username>
        
        -p <password> | --password <password>

        -f <formats>  | --formats <formats> 
            A comma-separated list of formats to export. Defaults to json. 
            Valid options are: json, html, xml.

        -d | --directory <directory>
            Defaults to current directory.

    """

def options(args):
    """Processes command line arguments"""

    try:
        opts, args = getopt.getopt(args, 'u:p:f:hd:',['username=','password=','formats=','help','directory='])
    except getopt.GetoptError, e:
        print str(e)
        usage()
        sys.exit(2)

    # Defaults
    username = password = None
    formats = set(['json'])
    directory = os.getcwd()
    
    for o,v in opts:
        if o in ('-u', '--username'):
            username = v
        elif o in ('-p', '--password'):
            password = v
        elif o in ('-f', '--formats'):
            formats = set(map(str.strip, v.split(',')))
        elif o in ('-d', '--directory'):
            if os.path.exists(v):
                directory = v
            else:
                print "Destination directory does not exist."
                sys.exit(2)
        elif o in ('-h', '--help'):
            usage()
            sys.exit(2)
        else:
            usage()
            sys.exit(2)

    # prompt for missing parameters if missing
    if not username:
        username = raw_input('Username: ')
    if not password:
        password = getpass.getpass('Password: ')

    return (username, password, formats, directory)

if __name__ == '__main__':
    username, password, formats, directory = options(sys.argv[1:])
    exporter = PinboardExporter(username,password)
    exporter.export_bookmarks(formats, directory)
