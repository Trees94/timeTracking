#!/usr/bin/env python3
from dateutil.parser import parse
from datetime import datetime, timedelta
from collections import defaultdict
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import sys


def parse_daily_results(filename):
    records = []
    with open(filename.strip(), 'r') as f:
        record_lines = f.readlines()
        records += [parse_line(line) for line in record_lines]

    times = time_deltas(records)
    aggregate_times = aggregate_deltas(times)
    return aggregate_times


# Wed, 18 Oct 2017 03:55:17 +0100 : bonana
def parse_line(line):
    parts = line.strip().rsplit(':', 1)
    date = parse(parts[0].strip())
    task = parts[1].strip()
    return (date, task)


def generate_report(aggregate_times):
    labels = aggregate_times.keys()
    sizes = [(value.days * 3600 * 24) + value.seconds for value in aggregate_times.values()]
    total = sum(sizes)
    plt.title("Time Spent: " + formatSeconds(total))
    plt.pie(sizes, labels=labels, autopct=lambda x: formatSeconds((x*total/100.0)+0.5))
    plt.savefig(sys.argv[1])


def formatSeconds(seconds):
    return str(int(seconds / 3600)) + "h" + str(int((seconds % 3600) / 60)) + "m"


def time_deltas(records):
    times = []
    for index, record in enumerate(records):
        if index < len(records) - 1:
            time_spent =  records[index + 1][0] - record[0]
            times.append((record[1], time_spent))

    return times


def aggregate_deltas(time_deltas):
    aggregates = defaultdict(lambda: timedelta())
    for delta in time_deltas:
        aggregates[delta[0]] += delta[1]
    
    return aggregates


if __name__=="__main__":
    aggregates = parse_daily_results(sys.stdin.readlines()[0])
    generate_report(aggregates)

