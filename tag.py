#!/usr/bin/env python
# Copyright 2014 (C) Sean R. Spillane
# This program is hereby released under the BSD license.

import argparse
import logging

def parser(log):
    parser = argparse.ArgumentParser(description="A program that tags arbitrary files with arbitrary strings.")
    parser.add_argument("--verbose", action="store_true", help="If set, make the application emit DEBUG log statements.")
    parser.add_argument("--quiet",   action="store_true", help="If set, make the application silent except for errors.")
    subparsers = parser.add_subparsers(help="Action to perform.")
    parser_tag = subparsers.add_parser("tags", help="Given a file, return the set of associated tags.")
    parser_get = subparsers.add_parser("get",  help="Given a tag expression, return the set of matching files.")
    parser_set = subparsers.add_parser("set",  help="Given a file and a set of tags, add those tags to the file.")
    
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