#!/usr/bin/env python

from applescript import asrun, asquote
from datetime import datetime

def create_note(content, title = None, is_html = False, notebook = None, tags = []):
    en_script = 'tell application "Evernote"\n'
    en_script += 'create note title {0}'.format(_get_title(title))
    en_script += ' with {0} {1}'.format(_get_format(is_html), _get_content(content))
    if len(tags):
        en_script += ' tags {{{0}}}'.format(_get_tags(tags))
    if notebook != None:
        en_script += ' notebook {0}'.format(_get_notebook(notebook))
    en_script += '\nend tell'
    asrun(en_script)

def _get_title(title):
    if title == None:
        title = datetime.now().strftime('%A, %B %d, %Y %I:%M:%S %p')
    return asquote(title)

def _get_format(is_html):
    if is_html:
        return 'html'
    else:
        return 'text'

def _get_content(content):
    return asquote(content)

def _get_tags(tags):
   return ','.join(['"{0}"'.format(t) for t in tags]) 

def _get_notebook(notebook):
    return asquote(notebook)

def self_test():
    create_note('Content only')
    create_note('Content with title', title='This is the title')
    create_note('Content with title and notebook', title='This is the title', notebook='!Inbox')
    create_note('Content with title, notebook, and tags', title='This is the title', notebook='!Inbox', tags=['daily-work-log','wish-list'])
    create_note('<b>HTML content with title</b><ul><li>Item 1</li><li>Item 2</li></ul>', is_html=True, title='This is the title')
