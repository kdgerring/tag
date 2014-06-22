'''
Tag DB.

Provide a very simple key/value store. No attempt is made to be ACID. This module uses the GIT
approach, where objects are hashed (sha256), then written to files by hash in a folder.

We do not use the .git subdir approach, instead using a home directory based location. This was
because we wanted to support the notion of a single tag database for all tags.
'''

import os
import logging
import hashlib
import yaml
from Monads.Maybe import *

try:
    appdata = os.environ['TAGDIR']
except KeyError:
    if os.name is 'nt':
        appdata = os.path.join(os.environ['LOCALAPPDATA'],'tags')
    else:
        appdata = os.path.join(os.environ['HOME'],'.tags')


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
        log.debug("Key is: {}.".format(key))
        hashFile = self.__keyToFile(key)
        log.debug("Trying to read corresponding file.")
        try:
            with open(hashFile) as value:
                log.debug("Reading key now.")
                yamlData = value.read()
                log.debug("Raw string is: {}".format(yamlData))
                yamlData = yaml.load(yamlData)
                log.debug("Parsed data string is: {}".format(yamlData))
                if yamlData is not None:
                    return Just(set(yamlData))
                else:
                    return Nothing()
        except FileNotFoundError:
            return Nothing()

    def set(self, key, value):
        '''
        Given a key and value, set the value according to the key in the object DB.
        '''
        log = logging.getLogger(__name__)
        hashFile = self.__keyToFile(key)
        log.debug("Key is: {}.".format(key))
        log.debug("Key path is: {}.".format(hashFile))
        log.debug("Value is: {}".format(value)) # Probably very noisy!
        log.debug("Ensuring that tag dir exists.")
        os.makedirs(self.tagFolder,exist_ok=True)
        log.debug("Trying to create/overwrite corresponding file.")
        with open(hashFile, mode="w") as valueFile:
            log.debug("Item to write is: {}".format(value))
            value = yaml.dump(value)
            log.debug("Serialized item is: {}".format(value))
            log.debug("Writing key now")
            valueFile.write(value)
