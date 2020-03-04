#!/usr/bin/env python3
from sys import stdout
from sys import stderr
from traceback import print_exc
from os import path as Path
from urllib import request as urllib
#
#
from config import backup_dir
from config import backup_urls
#
#
class Downloads:
    def __init__(self, urls, work):
        self._work = work if Path.exists(work) else '/tmp'
        self._urls = list(map(urllib.urlparse, urls))
    #
    def _download(self, url, file):
        try: urllib.urlretrieve(url, file)
        except Exception as error: print(error, file=stderr)
    #
    def _show(self, prefix, url, file):
        return '{}: {}:{}{} -> {}'.format(
            prefix,
            url.hostname,
            url.port,
            url.path,
            file
        )
    #
    def run(self):
        for item in iter(self._urls):
            url = item.geturl()
            file = Path.basename(item.path)
            file = Path.join(self._work, file)
            #
            if not Path.exists(file):
                print(self._show('Download', item, file))
                #
            else:
                print(self._show('Rewrite', item, file), file=stderr)
            #
            self._download(url, file)
#
#
if __name__ == '__main__': pass

