#!/usr/bin/python
import pyinotify
import subprocess
import time
import logging
import sys

mask = pyinotify.IN_CREATE | pyinotify.IN_DELETE | pyinotify.IN_CLOSE_WRITE
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class EventHandler(pyinotify.ProcessEvent):
    last = 0

    def process_default(self, event):
        parts = event.path.split('/')
        if len(parts) != 5:
            logger.debug('Not 5 parts to path, skipping')
            return

        site = parts[2]
        config = event.name
        target = '/'.join(parts[3:5])

        if target != 'config/dns':
            logger.debug('Not a dns file, skipping')
            return

        # Don't murder the servers
        if self.last > time.time()-10:
            logger.debug('Sleeping due to recent update')
            time.sleep(5)

        self.last = time.time()
        logger.info("Triggering update for %s (%s)" % (config, site))
        subprocess.call('/usr/sbin/symbiosis-dns-generate')

if __name__ == '__main__':
    log_handler = logging.FileHandler('/var/log/dns-watcher.log')
    con_handler = logging.StreamHandler()

    #logger.addHandler(con_handler)
    logger.addHandler(log_handler)

    logger.info('Starting')
    wm = pyinotify.WatchManager()
    handler = EventHandler()

    notifier = pyinotify.Notifier(wm, handler)
    wdd = wm.add_watch('/srv', mask, rec=True)
    notifier.loop(daemonize=True, pid_file='/var/run/dns-watcher.pid')
