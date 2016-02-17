# coding: utf-8

STORE_ENGINE = {
    'engine': 'mysql',
    'mysql': {
        'host': '0.0.0.0',
        'db': 'polytope',
        'user': 'root',
        'password': '123',
    },
    'hbase': {
    }
}

SPOUT_ENGINE = {
    'engine': 'file',
    'file': {
        'path': '/Users/lianbo/tmpt/test.log',
    },
    'kafka': {
        'topic': 'sohuwl-seo',
        'hosts': '10.11.152.97:2181,10.11.152.98:2181,10.11.152.99:2181',
        'group': 'frontgroup',
        'offset_reset': 'latest',
    }
}

import logging
import logging.handlers
import os

LOG_NAME = 'all.log'
LOG_PATH = os.path.join(os.path.dirname(__file__), LOG_NAME)
LOG_BACKUP_DAY_COUNT = 7
LOG_FORMAT = '[%(asctime)s][%(name)s][%(process)d][%(levelname)s] %(message)s'
LOG_LEVEL = 'INFO'


logging.root.setLevel(LOG_LEVEL)
hander = logging.handlers.TimedRotatingFileHandler(LOG_PATH, when='D', backupCount=LOG_BACKUP_DAY_COUNT)
formatter = logging.Formatter(LOG_FORMAT)
hander.setFormatter(formatter)
hander.setLevel(LOG_LEVEL)
logging.root.addHandler(hander)
