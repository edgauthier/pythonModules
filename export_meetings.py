#!/usr/bin/env python

from datetime import datetime, timedelta
import subprocess
from pprint import pprint

ICAL_BUDDY = '/usr/local/bin/icalBuddy'
CALENDARS = ['Work (Ed)']

# /usr/local/bin/icalBuddy --includeCals "Work (Ed)" --noCalendarNames --includeEventProps title,datetime --bullet "" --propertySeparators "*||*" -nrd eventsToday

def main():
    now = datetime.now()
    yesterday = get_events_for_dates(now-timedelta(days=1))
    today = get_events_for_dates(now)
    tomorrow = get_events_for_dates(now+timedelta(days=1))
    three_days = get_events_for_dates(now-timedelta(days=1), now+timedelta(days=1))

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
    cmd.append('-nrd')
    cmd.extend(event_dates_string.split())
    
    event_list = subprocess.check_output(cmd)
    return parse_event_list(event_list)

def parse_event_list(event_list):
    events = []
    for event_string in event_list.splitlines():
        event_name, event_datetime = event_string.split('||')
        events.append({'name': event_name, 'datetime': event_datetime})
    return events


if __name__ == '__main__':
    main()
