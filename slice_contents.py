
import pandas as pd

from common import load_config

import os
import glob
import csv



def read_events(ann_fn):
    with open(ann_fn, 'rt') as f:
        lines = f.read().splitlines()

    events = []

    for line in lines:
        parts = line.split('\t')
        if len(parts) == 3:
            st = float(parts[0].replace(',', '.'))
            et = float(parts[1].replace(',', '.'))
            cls = parts[2]
            events.append([st, et, cls])
        elif len(parts) > 3:
            st = float(parts[2])
            et = float(parts[3])
            cls = parts[4]
            events.append([st, et, cls])

    return events

def get_classes_at_time(events_list, time, ignore_classes=None):
    cls = []

    if ignore_classes is None:
        ignore_classes = []

    for event in events_list:
        if event[2] in ignore_classes:
            continue

        if event[0] <= time and time <= event[1]:
            cls.append(event[2])

    return cls

def get_classes_in_period(events_list, start_time, end_time, separate_events=False, ignore_classes=None):
    cls = []

    if ignore_classes is None:
        ignore_classes = []

    for event in events_list:
        if event[2] in ignore_classes:
            continue

        if start_time <= event[0] and event[0] <= end_time:
            # event start is in the period
            cls.append(event[2])
        elif start_time <= event[1] and event[1] <= end_time:
            # event end is in the period
            cls.append(event[2])
        elif event[0] <= start_time and end_time <= event[1]:
            cls.append(event[2])

    if not separate_events:
        cls = sorted(set(cls))

    return cls

def key_from_fn(fn):
    key = os.path.splitext(os.path.basename(fn))[0]
    return key


def write_csv(csv_fn, hdr, rows):
    with open(csv_fn, 'wt') as f:
        csv_writer = csv.writer(f, delimiter=',')

        csv_writer.writerow(hdr)
        csv_writer.writerows(rows)



def main():
    cfg = load_config()

    csv_fn = cfg['output_csv']

    output_files = pd.read_csv(csv_fn)

    #src_dir = '../ss_synth/soundscapes'
    src_dir = '../longscapesynth/soundscapes'

    #txt_fns = glob.glob(os.path.join(src_dir, '*.txt'))
    txt_fns = glob.glob(os.path.join(src_dir, '*.ann'))

    events = {}

    slice_len = 10.0

    ignore_classes = ['(object) banging']
    rename_classes = {
        'car passing by': 'car',
        'children shouting': 'children'
    }

    slice_rows = []

    all_classes = set()

    # read all the metadata for the dataset
    for fn in sorted(txt_fns):
        events_list = read_events(fn)
        key = key_from_fn(fn)
        events[key] = events_list

    # iterate through every every line in the output csv
    for _, row in output_files.iterrows():
        key = key_from_fn(row['source'])
        start_time = row['offset']
        end_time = start_time + slice_len

        # get event classes for the current slice
        ev = get_classes_in_period(events[key], start_time, end_time, ignore_classes=ignore_classes)

        # rename classes if needed:
        ev = list(map(lambda s: rename_classes.get(s, s), ev))

        # construct output line
        bfn = os.path.basename(row['filename'])
        slice_rows.append([key, bfn, start_time, ev])

        # collect all classes
        all_classes.update(set(ev))

    hdr = ['source', 'filename', 'offset', 'events']
    write_csv('contents.csv', hdr, slice_rows)

    print('found classes:', ', '.join(sorted(all_classes)))

if __name__ == '__main__':
    main()
