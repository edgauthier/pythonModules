#!/usr/bin/env python

from applescript import asrun, asquote
from datetime import datetime

def create_note(content, title = None, is_html = False, notebook = None, 
        tags = None, created = None, attachments = None, url = None, 
        latitude = None, longitude = None):
    en_script = 'tell application "Evernote"\n'
    en_script += u'set n to create note title {0}'.format(_get_title(title, created))
    en_script += u' with {0} {1}'.format(_get_format(is_html), _get_content(content))
    if tags:
        en_script += u' tags {{{0}}}'.format(_get_tags(tags))
    if notebook:
        en_script += u' notebook {0}'.format(_get_notebook(notebook))
    if created:
        en_script += u' created {0}'.format(_get_created(created))
    if attachments:
        en_script += u' attachments {{{0}}}'.format(_get_attachments(attachments))
    en_script += '\n'
    if created:
        en_script += 'set modification date of n to {0}\n'.format(_get_created(created))
    if url:
        en_script += 'set source URL of n to {0}\n'.format(_get_url(url))
    if latitude:
        en_script += 'set latitude of n to {0}\n'.format(_get_lat(latitude))
    if longitude:
        en_script += 'set longitude of n to {0}\n'.format(_get_long(longitude))
    en_script += 'end tell'
    asrun(en_script)

def _get_title(title, created):
    if title == None:
        if created == None:
            created = datetime.now()
        title = created.strftime('%A, %B %d, %Y %I:%M:%S %p')
    return asquote(title)

def _get_format(is_html):
    if is_html:
        return 'html'
    else:
        return 'text'

def _get_content(content):
    return asquote(content)

def _get_tags(tags):
   return u','.join([u'"{0}"'.format(t) for t in tags]) 

def _get_attachments(attachments):
   return u','.join([u'"{0}"'.format(a) for a in attachments]) 

def _get_notebook(notebook):
    return asquote(notebook)

def _get_created(created):
    return 'date "{0}"'.format(created.strftime('%A, %B %d, %Y %I:%M:%S %p'))

def _get_url(url):
    return '"{0}"'.format(url)

def _get_lat(latitude):
    return latitude

def _get_long(longitude):
    return longitude

def self_test():
    import os
    create_note('Content only')
    create_note('Content with title', title='This is the title')
    create_note('Content with title and notebook', title='This is the title', 
        notebook='!Inbox')
    create_note('Content with title, notebook, and tags', 
        title='This is the title', notebook='!Inbox', 
        tags=['daily-work-log','wish-list'])
    create_note('<b>HTML content</b><ul><li>Item 1</li><li>Item 2</li></ul>', 
        is_html=True, title='This is the title')
    create_note('Content', title='Blast from the past', 
        created=datetime(1970, 1, 1, 18, 59))
    create_note('Content', title='Note with attachments', 
        attachments=[os.path.realpath(__file__)])
    create_note('Content', title='Blast from the past with file', 
        created=datetime(1980, 1, 1, 18, 59), 
        attachments=[os.path.realpath(__file__)])
    create_note('Apple website', title='Apple link', url='http://apple.com')
    create_note('location', title='Note with location', 
        latitude='43.097270199999997', longitude='-77.382071699999997')
