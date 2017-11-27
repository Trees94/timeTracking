#!/usr/bin/env python3
from datetime import datetime, date, timedelta
import os
import argparse

FILEPATH = '/home/local/ANT/tomrees/time_tracking/{year}/{month}/{day}-timeTracking.md'

def main():
    args = parse_args()
    print_time_files(args.start_date, args.end_date)

def parse_args():
    parser = argparse.ArgumentParser(
        description='Lists all the time_tracking files in the specified range.')
    parser.add_argument('--from', '-f', dest='start_date', action='store', type=lambda x: valid_date(x), default=get_date(timedelta(days=-1)),
                        help='The date at which to start searching (inclusive). E.g. 2017-07-30')
    parser.add_argument('--to', '-t', dest='end_date', action='store', type=lambda x: valid_date(x), default=get_date(timedelta(days=-1)),
                        help='The date at which to stop searching (inclusive). E.g. 2017-07-30')
    args = parser.parse_args()
    return args

def valid_date(s):
    try:
        date = datetime.strptime(s, "%Y-%m-%d")
        return date
    except ValueError:
        try:
            days_before = int(s)
            return get_date(timedelta(days=-days_before))
        except ValueError:
            msg = 'Not a valid date (expected "%Y-%m-%d" or "int"): \'{0}\'.'.format(s)
            raise argparse.ArgumentTypeError(msg)

def get_date(timedelta):
    today_date = date.today()
    return datetime(today_date.year, today_date.month, today_date.day) + timedelta

def print_time_files(start, end):
    files = []
    delta = end - start

    for i in range(delta.days + 1):
        day = start + timedelta(days=i)
        files.append(FILEPATH.format(year=day.year, month=str(day.month).zfill(2), day=str(day.day).zfill(2)))

    for f in filter(lambda x: os.path.isfile(x), files):
        print(f)

if __name__ == '__main__':
    main()
