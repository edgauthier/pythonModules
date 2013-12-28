#!/usr/bin/env python

from datetime import datetime, timedelta
import subprocess
import os

ICAL_BUDDY = '/usr/local/bin/icalBuddy'
CALENDARS = ['Work (Ed)']
EXPORT_DIR = '/Users/plex/Dropbox/Public/Meetings'

# /usr/local/bin/icalBuddy --includeCals "Work (Ed)" --noCalendarNames --includeEventProps title,datetime --bullet "" --propertySeparators "*||*" -nrd eventsToday

def main():
    now = datetime.now()
    yesterday = get_events_for_dates(now-timedelta(days=1))
    export_events(yesterday, 'yesterday')
    today = get_events_for_dates(now)
    export_events(today, 'today')
    tomorrow = get_events_for_dates(now+timedelta(days=1))
    export_events(tomorrow, 'tomorrow')
    three_days = get_events_for_dates(now-timedelta(days=1), now+timedelta(days=1))
    export_events(three_days, 'three_days')

def get_events_for_dates(start_date, end_date = None):
    calendar_list = ','.join(['{0}'.format(c) for c in CALENDARS])
    if end_date == None:
        end_date = start_date
    start_date = start_date.strftime('%Y-%m-%d')
    end_date = end_date.strftime('%Y-%m-%d')
    event_dates_string = "eventsFrom:{0} to:{1}".format(start_date, end_date)

    cmd = [ICAL_BUDDY]
    cmd.extend(['--includeCals', calendar_list])
    cmd.append('--noCalendarNames')
    cmd.extend(['--includeEventProps', 'title,datetime'])
    cmd.extend(['--bullet', ''])
    cmd.extend(['--propertySeparators', '*||*'])
    cmd.append('--excludeAllDayEvents')
    cmd.append('--noRelativeDates')
    cmd.append('--excludeEndDates')
    cmd.extend(['--dateFormat', '%Y-%m-%d'])
    cmd.extend(event_dates_string.split())
    
    event_list = subprocess.check_output(cmd)
    return parse_event_list(event_list)

def parse_event_list(event_list):
    events = []
    for event_string in event_list.splitlines():
        event_name, event_datetime = event_string.split('||')
        events.append({'name': event_name, 'datetime': event_datetime})
    return events

def export_events(events, name):
    filename = os.path.join(EXPORT_DIR, '{0}.txt'.format(name))
    with open(filename, 'w') as f:
        for event in events:
            f.write('{0}\t{0}||{1}\n'.format(event['name'], event['datetime']))
        pass

if __name__ == '__main__':
    main()
