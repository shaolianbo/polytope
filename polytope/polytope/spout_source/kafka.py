# -*- coding: utf-8 -*-
import json
import logging

from kazoo.client import KazooClient
from samsa.cluster import Cluster

from base import BaseDataSpout
from utils.ip_source import IpSource

logger = logging.getLogger(__name__)


class KafkaSpout(BaseDataSpout):
    consumer = None

    @classmethod
    def init_consumer(cls, hosts, topic, group, offset_reset):
        zookeeper = KazooClient(hosts)
        zookeeper.start()
        cluster = Cluster(zookeeper)
        topic = cluster.topics[topic]
        consumer = topic.subscribe(group=group, offset_reset=offset_reset)
        return consumer

    @classmethod
    def init(cls, *args, **kwargs):
        if not cls.consumer:
            cls.consumer = cls.get_consumer(*args, **kwargs)

    @classmethod
    def read(cls):
        msg = cls.consumer.next_message(block=True, timeout=0.1)
        index = {}
        data = {}
        if msg:
            msg_str = msg
            try:
                _, index, data = cls.format(json.loads(msg))
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
