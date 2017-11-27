#!/usr/bin/env python3
from collections import defaultdict
from parseDailyResults import parse_daily_results, generate_report
from datetime import timedelta
import sys


def main():
    records = []
    aggregates = defaultdict(lambda: timedelta())
    for filename in sys.stdin.readlines():
        daily_aggregates = parse_daily_results(filename)
        for key in daily_aggregates.keys():
            aggregates[key] += daily_aggregates[key]

    generate_report(aggregates)

if __name__=="__main__":
    main()

