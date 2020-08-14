# coding: utf-8
import os
import yaml
import logging.config
from mongoengine import connect

BASE_PATH = os.path.dirname(__file__)

conf_path = os.path.join(BASE_PATH, "config.yml")
with open(conf_path) as stream:
    conf = yaml.safe_load(stream)

connect(**conf["database"])

SYSTEM = conf["system"]
SERVICES = conf["services"]
SERVER = conf["server"]

AUTH_PARAMETERS = conf['tmall_auth']

LOGGING = {
    "version":1,
    'disable_existing_loggers': False,
    "handlers":{
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'daemon_log_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': SYSTEM["daemon_log_path"],
            'formatter': 'verbose'
        },
        'tmall_log_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': SYSTEM["tmall_log_path"],
            'formatter': 'verbose'
        },
    },
    "loggers":{
        "daemon_log":{
            "handlers": ["daemon_log_file", "console"],
            "level":"INFO",
            "propagate": False
        },
        "tmall_log":{
            "handlers": ["tmall_log_file", "console"],
            "level":"INFO",
            "propagate": False
        }
    },
    "formatters":{
        'verbose': {
            'format': '%(asctime)s | %(processName)-12s | %(name)-25s | '
                      '%(levelname)-8s | %(message)s'
        },
    },
}

logging.config.dictConfig(LOGGING)