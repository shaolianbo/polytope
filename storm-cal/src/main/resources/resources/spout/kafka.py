# -*- coding: utf-8 -*-
import json
import logging

from kazoo.client import KazooClient
from samsa.cluster import Cluster

from base import BaseDataSpout
from utils.ip_source import IpSource

logger = logging.getLogger(__name__)


class KafkaConfig(object):
    topic = 'sohuwl-seo'
    hosts = '10.11.152.97:2181,10.11.152.98:2181,10.11.152.99:2181'
    group = 'frontgroup'
    offset_reset = 'latest'


class Kafka(object):
    config = KafkaConfig
    consumer = None

    @classmethod
    def get_consumer(cls):
        config = cls.config
        if not cls.consumer:
            zookeeper = KazooClient(config.hosts)
            zookeeper.start()
            cluster = Cluster(zookeeper)
            topic = cluster.topics[config.topic]
            cls.consumer = topic.subscribe(group=config.group, offset_reset=config.offset_reset)
        return cls.consumer


class KafkaSpout(BaseDataSpout):
    consumer = None

    @classmethod
    def init(cls, *args, **kwargs):
        if not cls.consumer:
            cls.consumer = Kafka.get_consumer()

    @classmethod
    def read(cls):
        msg = cls.consumer.next_message(block=True, timeout=0.1)
        index = {}
        data = {}
        if msg:
            msg_str = msg
            try:
                -, index, data = cls.format(json.loads(msg))
            except Exception as e:
                logger.error(r"%s %r", msg_str, e)
            cls.consumer.commit_offsets()
        return False, index, data

    @classmethod
    def format(cls, msg):
        index = {}
        index['ad'] = int(msg['performance'].get('ad', 1))
        index['page'] = msg['page']
        index['net'] = msg['performance']['nettype']
        _, province, operator = IpSource.locate_ip(msg['ip'])
        index['area'] = province
        index['operator'] = operator
        return index, msg['performance']
