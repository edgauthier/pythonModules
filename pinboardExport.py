#!/usr/bin/python

import sys
import getopt
import urllib
import urllib2
import cookielib

class PinboardExporter(object):
    """Logs into pinboard.in and exports bookmarks in various formats."""
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self._connect()
    
    def export_bookmarks(self, bookmark_formats = set(['json'])):
        """Exports bookmarks in each of the formats specified"""
        # sanitize formats - these will be used directly
        formats = set(['html', 'json', 'xml']) & bookmark_formats
        map(self._download_bookmarks, formats)

    def _connect(self):
        """Connects to the pinboard.in website."""
        cj = cookielib.CookieJar()
        self.site = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        login_data = urllib.urlencode({'username' : self.username, 'password' : self.password})
        self.site.open(PinboardExporter._LOGIN_PAGE, login_data)
        #TODO test if the login succeeded

    def _download_bookmarks(self, bookmark_format):
        """Downloads pinboard bookmarks in a given format"""
        export_page = PinboardExporter._EXPORT_BASE_PAGE + bookmark_format + '/'
        export_file = 'bookmarks.' + bookmark_format
        with open(export_file, 'w') as output:
            resp = self.site.open(export_page)
            output.writelines(resp)

    _LOGIN_PAGE = 'https://pinboard.in/auth/'
    _EXPORT_BASE_PAGE = 'http://pinboard.in/export/format:'

def usage():
    print "\nUsage: pinboardExport.py -u|--username <username> -p|--password <password> [-f|--formats <formats>]\n"

def options(args):
    """Processes command line arguments"""

    try:
        opts, args = getopt.getopt(args, 'u:p:f:',['username=','password=','formats='])
    except getopt.GetoptError, e:
        print str(e)
        usage()
        sys.exit(2)

    username = password = formats = None
    
    for o,v in opts:
        if o in ('-u', '--username'):
            username = v
        elif o in ('-p', '--password'):
            password = v
        elif o in ('-f', '--formats'):
            formats = set(v.split(','))
        else:
            usage()
            sys.exit(2)

    #TODO prompt for missing parameters instead of exiting
    if not username or not password or not formats:
        usage()
        sys.exit(2)

    return (username, password, formats)

if __name__ == '__main__':
    username, password, formats = options(sys.argv[1:])
    exporter = PinboardExporter(username,password)
    exporter.export_bookmarks(formats)
