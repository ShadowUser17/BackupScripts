#!/usr/bin/env python3
import os
import csv
import argparse
import traceback


OUT_TEMPLATE = '''\
    # {}
    "{}": [
        "Commands..."
    ],
'''


def data_read(fname):
    with open(fname) as file:
        csv_reader = csv.reader(file)
        yield from csv_reader


def data_filter(itobj, includes=['up'], byitem=0, columns=(1, 3)):
    for item in itobj:
        if item[byitem] in includes:
            yield item[slice(*columns)]


def data_build(itobj, template, tags=['devdb={\n', '}\n']):
    yield tags[0]
    for item in itobj:
        outobj = iter(template.format(*item))
        yield from outobj

    yield tags[1]


def data_write(fname, itobj, force=False):
    if os.path.exists(fname) and (not force):
        raise OSError('File {} is exist!'.format(fname))

    with open(fname, 'w') as file:
        for item in itobj:
            file.write(item)


def args_parse(args=None):
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', dest='inp_file', help='Set input file (*.csv).')
    parser.add_argument('-o', dest='out_file', help='Set output file (*.py).')
    parser.add_argument('-f', dest='force', action='store_true', help='Enable rewrite file.')
    parser.add_argument('-v', dest='show', action='store_true', help='Enable CLI output.')

    return parser.parse_args(args)


def data_show(itobj, enabled=False):
    for item in itobj:
        if enabled:
            print(item, sep='', end='')

        yield item


if __name__ == '__main__':
    try:
        args = args_parse()

        read_obj = data_read(args.inp_file)
        filter_obj = data_filter(read_obj)
        build_obj = data_build(filter_obj, OUT_TEMPLATE)
        show_obj = data_show(build_obj, args.show)
        data_write(args.out_file, show_obj, args.force)

    except Exception:
        traceback.print_exc()
