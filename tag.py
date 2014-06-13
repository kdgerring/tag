#!/usr/bin/env python
# Copyright 2014 (C) Sean R. Spillane
# This program is hereby released under the BSD license.

import argparse
import logging

def parser(log):
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", action="store_true", help="If set, make the application emit DEBUG log statements.")
    parser.add_argument("--quiet",   action="store_true", help="If set, make the application silent except for errors.")
    args = parser.parse_args()
    if args.verbose:
        log.setLevel(logging.DEBUG)
    if args.quiet:
        log.setLevel(logging.WARNING)
    return args

def main():
    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger()
    args = parser(log)
    log.info("Starting program")
    print(args)
    log.info("Program complete")
    logging.shutdown()

if __name__ == '__main__':
    main()