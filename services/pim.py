# coding: utf8
import logging

logger = logging.getLogger("daemon_log")


class PIMService(object):

    def handle(self, message):
        logger.warn("PIM message handler not implemented!")