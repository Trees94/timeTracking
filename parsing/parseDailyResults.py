#!/usr/bin/env python3
import pprint
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

    fixed_records = []
    for index, entry in enumerate(records):
        if not entry[1]:
            if index > 1:
                for i in range(0, index):
                    print(records[index - i])
                    if records[index - i][1] and 'AFK' not in records[index -i][1]:
                        print('HIT!')
                        fixed_records.append((entry[0], records[index - i][1]))
        else:
            fixed_records.append(entry)

    pprint.pprint(fixed_records)

    times = time_deltas(list(filter(lambda x: 'Interrupt' not in x[1], fixed_records)))
    aggregate_times = aggregate_deltas(times)
    return aggregate_times


# Wed, 18 Oct 2017 03:55:17 +0100 : bonana
def parse_line(line):
    parts = line.strip().split(' : ', 1)
    if len(parts) == 1:
        return (parse(parts[0][:31]), None)
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
