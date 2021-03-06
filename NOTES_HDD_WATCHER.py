#!/usr/bin/env python

import os
import sys
import argparse
import time
import shutil
import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from datetime import datetime
from threading import Thread
from queue import Queue
import shutil
from PyQt5.QtWidgets import QPlainTextEdit, QDialog, QApplication
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget, QFileDialog
from NotesStructure import process_file


# Logging main watchdog events
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

fh = TimedRotatingFileHandler('watchdog.log', when="W6", backupCount=52)
# fh = TimedRotatingFileHandler(r'E:\ProjectDatabase\NoteWebSite\logs\watchdog.log', when="W6", backupCount=52)
fh.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

log.addHandler(fh)
log.addHandler(ch)


class UpdateWatcher(PatternMatchingEventHandler):
    ''' Watches a nominated directory and when a trigger file is
        moved to take the ".trigger" extension it proceeds to execute
        the commands within that trigger file.

        Notes
        ============
        Intended to be run in the background
        and pickup trigger files generated by other ETL process
    '''

    def __init__(self, queue, patterns):
        PatternMatchingEventHandler.__init__(self, patterns=patterns)
        self.queue = queue

    def process(self, event):
        '''
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        '''
        self.queue.put(event)

    def on_created(self, event):
        #ic(event)
        # CHECK IF THE FILE WAS CREATED IN ARCHIVED TO AVOID SECOND PARSING
        # CAN WE REARRANGE FILE TO AVOID THIS?

        log.info("NEW FILE CREATED: " + event.src_path)
        time.sleep(1)
        self.process(event)

    def on_moved(self, event):
        #ic(event)
        log.info("RECEIVED MOVED EVENT: %s." % event.src_path)
        time.sleep(1)
        pass

    def on_modified(self, event):
        #ic(event)
        log.info("RECEIVED MODIFIED EVENT: %s." % event.src_path)
        time.sleep(1)
        pass

    def on_deleted(self, event):
        #ic(event)
        # # Take action when a file is deleted
        # if 'deleted' in event.event_type:
        log.info("RECEIVED DELETED EVENT: %s." % event.src_path)
        time.sleep(1)
        pass


def process_load_queue(q, ARCHIVE_PATH):
    '''This is the worker thread function. It is run as a daemon
       threads that only exit when the main thread ends.

       Args
       ==========
         q:  Queue() object
    '''
    while True:
        if not q.empty():
            event = q.get()
            now = datetime.utcnow()
            #ic("{0} -- Pulling {1} off the queue ...".format(now.strftime("%Y/%m/%d %H:%M:%S"), event.src_path))
            log.info("{0} -- Processing {1}...\n".format(now.strftime("%Y/%m/%d %H:%M:%S"), event.src_path))
            if event.is_directory:
                #ic("{0} -- Path is a Directory -- Exiting Cleanly", event.src_path)
                log.info("{0} -- Path is a Directory -- Exiting Cleanly", event.src_path)
                pass
            elif 'created' in event.event_type:
                # Take action when a file is first created
                log.info("RECEIVED CREATED EVENT: %s." % event.src_path)

                process_file(event.src_path)

                log.info("FILE PROCESSED SUCCESSFULLY")

                # wait 5 seconds before moving file
                # time.sleep(5)
                # Move file to archive
                # archive_folder = r"ImagesArchive"
                # archive_folder = os.path.abspath(ARCHIVE_PATH)
                # file_name = Path(event.src_path).name
                # new_file = os.path.join(archive_folder, file_name)
                # try:
                #     shutil.move(str(os.path.abspath(event.src_path)), new_file)
                #     log.info("FILE ARCHIVED SUCCESSFULLY")
                # except WindowsError:
                #     log.error(WindowsError)
                #     log.info('FILE NOT ARCHIVED')

                # log the operation has been completed successfully
                now = datetime.utcnow()
                log.info("{0} -- Finished processing {1}...\n".format(now.strftime("%Y/%m/%d %H:%M:%S"), event.src_path))
                time.sleep(2)
        else:
            time.sleep(10)


class Watcher:
    # CODE TO HANDLE DISCONNECTS BETWEEN WATCHDOG AND FILESERVER
    log.info("CHANGE IN DIRECTORY DETECTED")

    def __init__(self, event_handler, directory):
        self.observer = Observer()
        self.event_handler = event_handler
        self.directory2watch = directory

        self.run()

    def run(self):
        self.observer.schedule(self.event_handler, self.directory2watch, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except ValueError:
            log.exception("Error in Watcher run function")
        finally:
            self.observer.stop()

        self.observer.join()




if __name__ == '__main__':

    print(os.getpid())
    parser = argparse.ArgumentParser(description='Monitor folder to process files and move to archive')
    parser.add_argument('-w', '--watch_folder', help="Folder to monitor for input files")
    parser.add_argument('-a', '--archive_folder', help="Folder to move files into")

    args = parser.parse_args()

    ## RUNNING GLOBAL CONSTANTS
    # DIRECTORY_TO_WATCH = args.watch_folder
    # ARCHIVE_PATH = args.archive_folder
    DIRECTORY_TO_WATCH = r'C:\Users\rbwolf\iCloudDrive\iCloud~com~novosoft~TurboScan\Uploads'
    ARCHIVE_PATH = r'E:\ImagesArchive'

    # create queue
    events_queue = Queue()

    # Set up a worker thread to process database load
    worker = Thread(target=process_load_queue, args=(events_queue, ARCHIVE_PATH,))
    worker.setDaemon(True)
    worker.start()

    # setup watchdog to monitor directory for trigger files
    patt = ["*.png", "*.jpg", "*.jpeg"]
    event_handler = UpdateWatcher(events_queue, patt)
    event_watcher = Watcher(event_handler, DIRECTORY_TO_WATCH)

    # DIRECTORY_TO_WATCH = r'/mnt/freenas/ADVT_Equipment/DEV'
    # DIRECTORY_TO_WATCH = r'E:\Images'
    # watcher_worker = Thread(target=Watcher, args=(event_worker, DIRECTORY_TO_WATCH))
    # watcher_worker.setDaemon(True)
    # watcher_worker.start()





