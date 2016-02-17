#!/usr/bin/env python
# coding: utf-8
import logging
import struct
from socket import inet_aton
import os

_unpack_V = lambda b: struct.unpack("<L", b)
_unpack_N = lambda b: struct.unpack(">L", b)
_unpack_C = lambda b: struct.unpack("B", b)

logger = logging.getLogger(__name__)


class IPX:
    binary = ""
    index = 0
    offset = 0

    @classmethod
    def load(cls):
        try:
            path = os.path.join(os.path.dirname(__file__), 'mydata4vipday2.datx')
            with open(path, "rb") as f:
                cls.binary = f.read()
                cls.offset, = _unpack_N(cls.binary[:4])
                cls.index = cls.binary[4:cls.offset]
        except Exception as ex:
            logger.exception("cannot open ipip file mydata4vipday2.datx")
            exit(0)

    @classmethod
    def find(cls, ip):
        index = cls.index
        offset = cls.offset
        binary = cls.binary
        nip = inet_aton(ip)
        ipdot = ip.split('.')
        if int(ipdot[0]) < 0 or int(ipdot[0]) > 255 or len(ipdot) != 4:
            return "N/A"

        tmp_offset = (int(ipdot[0]) * 256 + int(ipdot[1])) * 4
        start, = _unpack_V(index[tmp_offset:tmp_offset + 4])

        index_offset = index_length = -1
        max_comp_len = offset - 262144 - 4
        start = start * 9 + 262144

        while start < max_comp_len:
            if index[start:start + 4] >= nip:
                index_offset, = _unpack_V(index[start + 4:start + 7] + chr(0).encode('utf-8'))
                index_length, = _unpack_C(index[start + 8:start + 9])
                break
            start += 9

        if index_offset == 0:
            return "N/A"

        res_offset = offset + index_offset - 262144
        return binary[res_offset:res_offset + index_length].decode('utf-8')

    @classmethod
    def all(cls):
        index = cls.index
        offset = cls.offset
        head = 0
        while head < (262144 - 8):
            head_start, = _unpack_V(index[head:head + 4])
            next_start, = _unpack_V(index[head+4:head+8])
            if next_start == head_start:
                head += 4
                continue

            index_start = head_start*9 + 262144
            index_end = next_start*9 + 262144
            for ip, address in cls._get_ip_addres_by_index(index_start, index_end):
                yield ip, address
            head += 4

        head_start, = _unpack_V(index[head:head + 4])
        index_start = head_start*9 + 262144
        index_end = offset - 262144 - 4
        for ip, address in cls._get_ip_addres_by_index(index_start, index_end):
            yield ip, address

    @classmethod
    def _get_ip_addres_by_index(cls, index_start, index_end):
        index = cls.index
        offset = cls.offset
        binary = cls.binary
        while index_start < index_end:
            ip = index[index_start:index_start+4]
            index_offset, = _unpack_V(index[index_start + 4:index_start + 7] + chr(0).encode('utf-8'))
            index_length, = _unpack_C(index[index_start + 8:index_start + 9])
            if index_offset:
                res_offset = offset + index_offset - 262144
                address = binary[res_offset:res_offset + index_length].decode('utf-8')
                ip_str = '.'.join(["%s" % ord(c) for c in ip])
                yield ip_str, address
            index_start += 9


if __name__ == "__main__":
    IPX.load()
    for ip, address in IPX.all():
        print ip, address
