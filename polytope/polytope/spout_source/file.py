# coding: utf-8
import json

from base import BaseDataSpout
from utils.ip_source import IpSource


class FileSpout(BaseDataSpout):
    file_object = None
    _end = False

    @classmethod
    def init(cls, path):
        if not cls.file_object:
            cls.file_object = open(path)
            cls._end = False

    @classmethod
    def read(cls):
        if not cls.file_object:
            raise Exception("FileSpout not init file_object")

        if cls._end:
            return cls._end, {}, {}

        line = {}
        while True:
            line = cls.file_object.readline()
            if not line:
                cls._end = True
                return cls._end, {}, {}
            try:
                line = json.loads(line.strip())
            except ValueError:
                continue
            break

        index = {}
        data = {}
        if line:
            index, data = cls.format(line)
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

    @classmethod
    def close(cls):
        if cls.file_object:
            cls.file_object.close()
            cls.file_object = None
            cls._end = False
