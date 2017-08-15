#!/usr/bin/env python3
#
# score.py
#
# Execute: ./score.py urls.txt rapports.csv

import json
import subprocess
from urllib.parse import urlparse
from collections import OrderedDict

import numpy as np
import pandas as pd

class ShellError(Exception):
    pass


def execute_lighthouse(url):
    o = urlparse(url)
    report_name = o.path[1:].replace('/', '-')
    if report_name == '':
        report_name = 'index'
    hostname = o.hostname
    cmd = ['lighthouse {} --output=json --output-path=./{}-{}.json'.format(
                url,
                hostname,
                report_name
            )]
    status = subprocess.call(cmd, shell=True)
    if status != 0:
        raise ShellError


def get_reports(urls_filename):
    with open(urls_filename, 'r') as desc:
        urls = desc.readlines()
    for url in urls:
        try:
            execute_lighthouse(url.strip())
        except ShellError:
            continue

def aggregate_reports(report_filenames, csv_filename):
    scores = list()
    for report_filename in report_filenames:
        score = compute_score(report_filename)
        scores.append(score)
    df = pd.DataFrame(scores)
    df.to_csv(csv_filename, index=False)
    return df


def compute_score(report_filename):
    score = dict()
    with open(report_filename, 'r') as desc:
        content_json = json.load(desc)
    for reportCategory in content_json['reportCategories']:
        category = reportCategory['id']
        note = reportCategory['score']
        score[category] = note
    return OrderedDict(sorted(score.items(), key=lambda x: x[0]))


def stats_score(scores):
    stats = dict()
    values = list(scores.values())
    stats['min'] = min(values)
    stats['max'] = max(values)
    stats['avg'] = np.average(values)
    stats['std'] = np.std(values)
    ordered_scores = OrderedDict(sorted(scores.items(), key=lambda x: x[1]))
    stats['categories'] = list(ordered_scores.keys())
    stats['scores'] = list(ordered_scores.values())
    return stats


if __name__ == "__main__":
    import sys
    import os

    import config

    args = sys.argv[1:]
    urls_filename = args[0]
    csv_filename = args[1]

    get_reports(urls_filename)
    report_filenames = [f for f in os.listdir('.') if f.endswith('.json')]
    df = aggregate_reports(report_filenames, csv_filename)
