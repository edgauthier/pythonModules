#!/usr/bin/env python

import os, sys, argparse
from datetime import datetime
from time import mktime
import dateutil.parser as date_parser
import plistlib
from uuid import uuid4
import requests
from PIL import Image
from dayone_settings import FORECASTIO_APIKEY

DAYONE_DIR = '/Users/ed/Dropbox/Apps/Day One/Journal.dayone'
DAYONE_ENTRIES = os.path.join(DAYONE_DIR, 'entries')
DAYONE_PHOTOS = os.path.join(DAYONE_DIR, 'photos')
FORECASTIO_QUERY_URL = None
if FORECASTIO_APIKEY:
    FORECASTIO_QUERY_URL = 'https://api.forecast.io/forecast/{0}/{{coords}},{{time}}' \
                    '?exclude=minutely,hourly,daily,alerts,flags'.format(FORECASTIO_APIKEY)

def main():
    args = get_args()
    entry = process_args(args)
    add_dayone_entry(**entry)

def add_dayone_entry(creation_date=None, entry_text='', location=None, weather=True, photo=None, tags=None):
    uuid = uuid4().hex.upper()
    entry = {}
    entry['UUID'] = uuid
    entry['Time Zone'] = 'America/New_York' # default to NY tz

    if not creation_date:
        creation_date = datetime.now()
    # entry['Creation Date'] = convert_date_for_dayone(creation_date)
    entry['Creation Date'] = creation_date

    entry['Entry Text'] = entry_text

    if tags:
        entry['Tags'] = tags

    if location:
        loc = {}
        lat, lon = location.split(',')
        loc['Latitude'] = lat
        loc['Longitude'] = lon
        # TODO set place
        entry['Location'] = loc
        
        w = get_weather(location, convert_date_for_dayone(entry['Creation Date']))

        # additional processing if we were able to get the weather
        if w:
            # override TZ if we have one based on location
            if 'timezone' in w:
                entry['Time Zone'] = w['timezone'] 

            # set weather information if this hasn't been disabled
            if weather:
                entry_weather = get_dayone_weather(w['currently'])
                entry['Weather'] = entry_weather

    if photo:
        try:
            dest_path = os.path.join(DAYONE_PHOTOS, uuid + '.jpg')
            max_size = (1600,1600)
            i = Image.open(photo)
            i.thumbnail(max_size, Image.ANTIALIAS)
            i.save(dest_path)
        except Exception as e:
            print 'Error saving photo: {0}'.format(e)

    entry_path = os.path.join(DAYONE_ENTRIES, uuid + '.doentry')
    entry_plist = plistlib.writePlist(entry, entry_path)

def process_args(args):
    entry = {}
    entry['creation_date'] = args.date
    entry['entry_text'] = get_entry_text(args.entry)
    if args.location:
        entry['location'] = args.location
    if args.tag:
        entry['tags'] = args.tag
    if args.weather:
        entry['weather'] = True
    if args.photo:
        entry['photo'] = args.photo
    return entry

def get_args():
    parser = argparse.ArgumentParser(description='Adds an entry to DayOne')
    parser.add_argument('-d', '--date', type=date_parser.parse, default=datetime.now(),
                        help='Specify a date/time other than the current time to use for the entry')
    parser.add_argument('-t', '--tag', nargs='+', 
                        help='One or more tags for the entry')
    # TODO consider a type attribute to validate the location format
    parser.add_argument('-l', '--location', metavar='lat,lon',
                        help='''Coordinates to use as the location in the format lat,lon.
                        The current location will be used if the coordinates are not specified. If
                        the flag isn\'t present, no location will be set.''')
    parser.add_argument('-w', '--weather', action='store_true', default=True,
                        help='Add weather for date of entry - enabled by default.')
    parser.add_argument('-e', '--entry', 
                        help='Entry text to be used rather than stdin')
    parser.add_argument('-p', '--photo', type=check_file_exists, 
                        help='Attach photo to entry')
    args = parser.parse_args()
    return args

def check_file_exists(path):
    if not os.path.exists(path):
        msg = 'File does not exist: {0}'.format(path)
        raise argparse.ArgumentTypeError(msg)
    return path

def get_utc_date(local_date):
    utc_date = datetime.utcfromtimestamp(mktime(local_date.replace(microsecond=0).timetuple()))
    return utc_date

def get_entry_text(entry):
    if entry:
        return entry
    # Otherwise, read from stdin
    return sys.stdin.read()

def get_weather(coords, time):
    if FORECASTIO_QUERY_URL == None:
        return None
    weather_url = FORECASTIO_QUERY_URL.format(coords=coords, time=time)
    response = requests.get(weather_url)
    return response.json()

def convert_date_for_dayone(d):
    utc_date = get_utc_date(d)
    return utc_date.isoformat() + 'Z'

def get_dayone_weather(weather):
    w = {}
    w['Service'] = 'Forecast.io'
    if 'temperature' in weather:
        w['Fahrenheit'] = str(int(weather['temperature']))
    if 'summary' in weather:
        w['Description'] = weather['summary']
    if 'humidity' in weather:
        w['Relative Humidity'] = str(int(float(weather['humidity'])*100))
    if 'icon' in weather:
        w['IconName'] = get_dayone_icon_name(weather['icon'])
    if 'visibility' in weather:
        w['Visibility M'] = str(int(weather['visibility']))
    if 'windBearing' in weather:
        w['Wind Bearing'] = str(weather['windBearing'])
    if 'windSpeed' in weather:
        w['Wind Speed MPH'] = str(float(weather['windSpeed']))
    if 'pressure' in weather:
        w['Pressure MB'] = str(int(weather['pressure']))
    return w

def get_dayone_icon_name(icon):
    parts = icon.split('-')
    if parts[0].lower() in ('partly', 'mostly'):
        parts[0] = parts[0][0]
    if parts[-1].lower() == 'day':
        parts.pop(-1)
    if parts[-1].lower() == 'night':
        parts[-1] = 'n'
    return ''.join(parts) + '.png'

if __name__ == '__main__':
    main()
