#!/usr/bin/env python

from evernoteas import create_note
from datetime import datetime
from plistlib import readPlist
from markdown import markdown
from dateutil.tz import tzutc, tzlocal
import os
import sys

DAYONE_DIR = '/Users/ed/Dropbox/Apps/Day One/Journal.dayone'
DAYONE_ENTRIES = os.path.join(DAYONE_DIR, 'entries')
DAYONE_PHOTOS = os.path.join(DAYONE_DIR, 'photos')

def main():
    for entry in dayone_entries():
        save_entry_to_evernote(entry)

def dayone_entries():
    for root, dirs, files in os.walk(DAYONE_ENTRIES):
        for filename in files:
            name, ext = os.path.splitext(filename)
            if ext != '.doentry':
                continue
            filepath = os.path.join(root, filename)
            print filepath
            entry = readPlist(filepath)
            yield entry

def save_entry_to_evernote(entry):
    note_params = {}
    created_date = _get_created(entry)
    note_params['created'] = created_date
    entry_text, tags = _process_entry_text_and_tags(entry)
    note_params['is_html'] = True
    note_params['content'] = markdown(entry_text)
    note_params['tags'] = tags
    note_params['latitude'], note_params['longitude'] = _get_location(entry)
    note_params['attachments'] = _get_attachments(entry)
    if 'daily-work-log' in tags:
        note_params['title'] = 'Work Log: {0}'.format(
            created_date.strftime('%A, %B %d, %Y %I:%M:%S %p'))
    create_note(**note_params)

def _process_entry_text_and_tags(entry):
    tags = [str.lower(tag) for tag in entry.get('Tags', [])]
    entry_text = entry['Entry Text']
    entry_text = entry_text.replace('\n===\n', '\n---\n')
    if 'Tag: OFDailyLog' in entry_text:
        tags.append('daily-work-log')
        entry_text = entry_text.replace('Tag: OFDailyLog', '')
    return entry_text, tags

def _get_location(entry):
    location = entry.get('Location', {})
    return location.get('Latitude', None), location.get('Longitude', None)

def _get_created(entry):
    created_date = entry.get('Creation Date', datetime.utcnow())
    return created_date.replace(tzinfo=tzutc()).astimezone(tzlocal())

def _get_attachments(entry):
    attachments = []
    uuid = entry.get('UUID', None)
    if uuid:
        photo_name = uuid + '.jpg'
        photo = os.path.join(DAYONE_PHOTOS, photo_name)
        if os.path.exists(photo):
            attachments.append(photo)
    return attachments

if __name__ == '__main__':
    main()
