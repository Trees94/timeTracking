#!/usr/bin/env python3
from collections import defaultdict
from parseDailyResults import parse_daily_results, generate_report
from datetime import timedelta
import sys
import pprint


def main():
    records = []
    aggregates = defaultdict(lambda: timedelta())
    for filename in sys.stdin.readlines():
        daily_aggregates = parse_daily_results(filename)
        for key in daily_aggregates.keys():
            aggregates[key] += daily_aggregates[key]


    aggregates = group_by_type(aggregates)

    pprint.pprint(aggregates)
    generate_report(aggregates)

def group_by_type(aggregates):
    grouped_aggregates = defaultdict(lambda: timedelta())
    other = defaultdict(lambda: timedelta())

    for key in aggregates:
        if 'command' in key.lower():
            grouped_aggregates['Command Center'] += aggregates[key]
        elif 'Deskside Chat' == key:
            grouped_aggregates['AFK - Working'] += aggregates[key]
        elif key.startswith('AFK'):
            grouped_aggregates[key] += aggregates[key]
        elif key.startswith('TT') or 'refactor' in key.lower() or 'coe' in key.lower() or 'spring' in key.lower() or 'ticket' in key.lower() or 'sev' in key.lower():
            grouped_aggregates['OpEx'] += aggregates[key]
        elif key.startswith('RP') or key.startswith('BC') or 'sdp' in key.lower() or 'cr2' in key.lower() or 'phase' in key.lower() or 'pm' in key.lower() or 'speed' in key.lower() or 'rejection' in key.lower():
            grouped_aggregates['SIM Tasks'] += aggregates[key]
        elif 'pdp' in key.lower() or 'ctf' in key.lower():
            grouped_aggregates['Personal Dev'] += aggregates[key]
        elif 'cr' in key.lower() or key.lower() == 'code review':
            grouped_aggregates['Reviews (code, docs, etc)'] += aggregates[key]
        else:
            print('"' + key + '" collapsed into other')
            grouped_aggregates['other'] += aggregates[key]
            other[key] = aggregates[key]

    pprint.pprint(other)

    return grouped_aggregates

if __name__=="__main__":
    main()
