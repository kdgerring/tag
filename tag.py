#!/usr/bin/env python
# Copyright 2014 (C) Sean R. Spillane
# This program is hereby released under the BSD license.

import argparse
import logging
import yaml

def list_tag(args):
    file_name = args.file
    log = logging.getLogger("tags")
    log.info("Called tags")
    log.info("Getting tags for {}".format(file_name))

def get_tag(args):
    tag_list = args.tags
    log = logging.getLogger("get")
    log.info("Called get")
    log.info("Getting files for {}".format(tag_list))

def set_tag(args):
    file_name = args.file
    tag_list = args.tags
    log = logging.getLogger("set")
    log.info("Called set")
    log.info("Setting tags for file {} to: {}".format(file_name, tag_list))

def parser(log):
    parser = argparse.ArgumentParser(description="A program that tags arbitrary files with arbitrary strings.")
    parser.add_argument("--verbose", action="store_true", help="If set, make the application emit DEBUG log statements.")
    parser.add_argument("--quiet",   action="store_true", help="If set, make the application silent except for errors.")

    subparsers = parser.add_subparsers(help="Action to perform.")

    parser_tag = subparsers.add_parser("tags", help="Given a file, return the set of associated tags.")
    parser_tag.set_defaults(func=list_tag)
    parser_tag.add_argument("file", help="Specifies the file to list.")

    parser_get = subparsers.add_parser("get",  help="Given a tag expression, return the set of matching files.")
    parser_get.set_defaults(func=get_tag)
    parser_get.add_argument("tags", help="Specifies the tag expression to match.", nargs=argparse.REMAINDER)

    parser_set = subparsers.add_parser("set",  help="Given a file and a tag expression, apply the expression to the file.")
    parser_set.set_defaults(func=set_tag)
    parser_set.add_argument("file", help="Specifies the file to tag.")
    parser_set.add_argument("tags", help="Specifies the tag expression to apply.", nargs=argparse.REMAINDER)

    args = parser.parse_args()

    if args.verbose:
        log.setLevel(logging.DEBUG)
        log.debug("Maximum verbosity enabled!")
    if args.quiet:
        log.setLevel(logging.WARNING)

    return args

def main():
    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger()
    args = parser(log)
    log.info("Starting program")
    args.func(args)
    log.info("Program complete")
    logging.shutdown()

if __name__ == '__main__':
    main()