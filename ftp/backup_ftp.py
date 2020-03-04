#!/usr/bin/env python3
import logging
from os import path as Path
from urllib import request as urllib
#
#
#from test import (
from config import (
    backup_dir,
    backup_log,
    backup_urls
)
#
#
class Downloads:
    def __init__(self, urls, work, log):
        self._urls = list(map(urllib.urlparse, urls))
        self._work = work
        self._log = log
        self._logging()
    #
    def _logging(self):
        logging.basicConfig(filename=self._log, filemode='w',
                            format='%(asctime)s %(levelname)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            level=logging.INFO)
    #
    def _download(self, url, file):
        try: urllib.urlretrieve(url, file)
        except Exception as error: logging.error(error)
    #
    def run(self):
        for item in iter(self._urls):
            url = item.geturl()
            file = Path.basename(item.path)
            file = Path.join(self._work, file)
            self._download(url, file)
#
#
if __name__ == '__main__':
    backup = Downloads(backup_urls, backup_dir, backup_log)
    backup.run()
