#!/usr/bin/env python
# Copyright 2014 (C) Sean R. Spillane
# This program is hereby released under the BSD license.

import argparse
import logging
import yaml
import os
import re
import hashlib

try:
    appdata = os.environ['TAGDIR']
except KeyError:
    if os.name is 'nt':
        appdata = os.path.join(os.environ['LOCALAPPDATA'],'tags')
    else:
        appdata = os.path.join(os.environ['HOME'],'.tags')


def list_tag(args):
    '''
    This function is used to process command lines for listing tags.
    '''
    file_name = args.file
    log = logging.getLogger("tags")
    log.info("Called tags")
    log.info("Getting tags for {}".format(file_name))

def get_tag(args):
    '''
    This function is used to process command lines for listing files.
    '''
    tag_list = args.tags
    log = logging.getLogger("get")
    log.info("Called get")
    log.info("Getting files for {}".format(tag_list))
    log.info("Starting DB.")
    tagdb = TagDB()
    log.info("Getting paths.")
    tagSet = tagdb.get(args.tags)
    log.debug("Parsed values are: {}".format(tagSet))

def set_tag(args):
    '''
    This function is used to process command lines for setting tags on files.
    '''
    def go(tags):
        return tags.union(addTags).difference(remTags)
    file_name = args.file
    tag_list = args.tags
    log = logging.getLogger("set")
    log.info("Called set")
    log.info("Setting tags for file {} to: {}".format(file_name, tag_list))
    log.info("Starting DB.")
    tagdb = TagDB()
    log.info("Getting file name.")
    fileName = args.file
    log.debug("File name is: {}.".format(fileName))
    log.info("Getting tag list.")
    tagList = args.tags
    log.debug("Tag list is: {}.".format(tagList))
    log.info("Processing tag list expression.")
    (m,d,e) = process(tagList)
    addTags = m.union(d).difference(e)
    remTags = e
    log.debug("Tags to add are: {}.".format(addTags))
    log.debug("Tags to remove are: {}.".format(remTags))
    oldTags = tagdb.get(file_name)
    log.debug("Old tags are: {}.".format(oldTags))
    newTags = (oldTags.bind(go)).fromMaybe(addTags)
    log.debug("New tags are: {}.".format(newTags))

def process(tagList):
    '''Given a list of tag expressions, return a triple of lists: (mandatory tags, discretional tags, excluded tags).'''
    mandatories = []
    discretionals = []
    excluded = []
    for tag in tagList:
        match = re.match("^\+(.*)$", tag)
        if match:
            mandatories.append(match.group(1))
        else:
            match = re.match("^\-(.*)$", tag)
            if match:
                excluded.append(match.group(1))
            else:
                discretionals.append(tag)
    return (mandatories,discretionals,excluded)

class Maybe:
    def pure(self, arg):
        if isinstance(self, Just):
            return Just(arg)
        else:
            return Nothing()

    def bind(self, func):
        if isinstance(self, Just):
            return self.bind(func)
        else:
            return Nothing()

    def fromMaybe(self, default):
        if isinstance(self, Just):
            return self.arg
        else:
            return default

class Just(Maybe):
    def __init__(self, arg):
        self.arg = arg

    def pure(self, arg):
        self.arg = arg

    def bind(self, func):
        func(self.arg)

class Nothing(Maybe):
    def __init__(self):
        ''' Do nothing '''
    def pure(self, arg):
        ''' Do nothing '''
        return Nothing()
    def bind(self, func):
        ''' Do nothing '''
        return Nothing()

class TagDB:
    def __init__(self, tagFolder=""):
        if tagFolder is "":
            self.tagFolder = appdata
        else:
            self.tagFolder = tagFolder

    def __keyToFile(self, key):
        '''
        Given a key, return a correct hash of that key.
        '''
        log = logging.getLogger(__name__)
        log.debug("DB folder is: {}.".format(self.tagFolder))
        hashKey = hashlib.sha256(str(key).encode()).hexdigest()
        log.debug("Key is: {}.".format(key))
        log.debug("Hashed key is: {}.".format(hashKey))
        return os.path.join(self.tagFolder, hashKey)

    def get(self, key):
        '''
        Given a key, retrieve the corresponding value from the object DB.
        '''
        log = logging.getLogger(__name__)
        hashFile = self.__keyToFile(key)
        log.debug("Trying to read corresponding file.")
        try:
            with open(hashFile) as value:
                log.debug("Reading key now.")
                return Just(set(yaml.load(value.read())))
        except FileNotFoundError:
            return Nothing()

    def set(self, key, value):
        '''
        Given a key and value, set the value according to the key in the object DB.
        '''
        log = logging.getLogger(__name__)
        hashFile = self.__keyToValue(key)
        log.debug("Value is: {}".format(value)) # Probably very noisy!
        log.debug("Trying to create/overwrite corresponding file.")
        with open(hashFile, mode="w") as valueFile:
            log.debug("Writing key now")
            valueFile.write(value)

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