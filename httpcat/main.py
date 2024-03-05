#! /usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

from httpcat import file_md5


def main():
    parser = argparse.ArgumentParser(prog='httpcat')
    sub_parsers = parser.add_subparsers()

    parser_etag = sub_parsers.add_parser(
        'md5',
        description='calculate the md5 of the file',
        help='md5 [file...]')
    parser_etag.add_argument(
        'md5_files',
        metavar='N',
        nargs='+',
        help='the file list for calculate')

    args = parser.parse_args()

    try:
        md5_files = args.md5_files

    except AttributeError:
        md5_files = None

    if md5_files:
        r = [file_md5(file) for file in md5_files]
        if len(r) == 1:
            print(r[0])
        else:
            print(' '.join(r))


if __name__ == '__main__':
    main()
