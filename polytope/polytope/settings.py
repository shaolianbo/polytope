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
    'source': 'file',
    'file': {
        'path': 'test.log',
    },
    'kafka': {
        'topic': 'sohuwl-seo',
        'hosts': '10.11.152.97:2181,10.11.152.98:2181,10.11.152.99:2181',
        'group': 'frontgroup',
        'offset_reset': 'latest',
    }
}
