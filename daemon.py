# coding: utf8

import signal
import sys
import logging
from Queue import Queue
from channel_connector import ChannelConnector
import config

logger = logging.getLogger("daemon_log")


def main():
    queue = Queue()

    def sig_handler(signum, frame):
        queue.task_done()
        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)

    for connector in range(len(config.SERVICES)):
        connector = ChannelConnector(queue)
        connector.setDaemon(True)
        connector.start()

    for kwargs in config.SERVICES.values():
        queue.put(dict(server=config.SERVER, **kwargs))

    print ' [*] Waiting for messages. To exit press CTRL+C'

    signal.pause()
    # queue.join()

if __name__ == "__main__":
    main()