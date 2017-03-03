# -*- coding: utf-8 -*-

import os
import sys
import time
import re
import logging
import subprocess
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler


class CIHandler(FileSystemEventHandler):

    def __init__(self, context):
        super(FileSystemEventHandler, self).__init__()
        self.context = context

    def on_created(self, event):
        # test(self.context)
        test(event)

    def on_modified(self, event):
        # test(self.context)
        test(event)


def test(context):
    try:
        if not context.is_directory and re.compile(".py$").search(context.src_path):
            # pep8
            logging.info("Static code analysis with pep8 :%s", context.src_path)
            subprocess.call(["pep8", context.src_path])
            logging.info("Unit test :%s", context.src_path)
            # unittest
            test_file_name = "test_" + context.src_path.split("/")[-1]
            test_file_path = os.path.join(current_path(), "tests", test_file_name)
            if os.path.exists(test_file_path):
                subprocess.call(["python", "-m", "unittest", test_file_path])
            else:
                logging.warn("No such file %s", test_file_path)

    except Exception:
        pass


def current_path():
    return os.path.abspath(
            os.path.join(
                os.path.dirname(__file__), '..'
                )
            )

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d%H:%M:%S')
    # path = sys.argv[1] if len(sys.argv) > 1 else '.'
    path = current_path() + "/msgiver"
    # event_handler = LoggingEventHandler()
    event_handler = CIHandler(path)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join