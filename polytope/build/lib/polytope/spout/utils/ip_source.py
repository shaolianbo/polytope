# coding: utf-8
from ipip import IPX
import logging

logger = logging.getLogger(__name__)

IPX.load()


class IpSource(object):

    @staticmethod
    def is_ipv4(ip):
        if not ip:
            return False
        if not isinstance(ip, basestring):
            return False
        items = ip.split('.')
        if len(items) != 4:
            return False
        for item in items:
            try:
                int_item = int(item)
            except ValueError:
                return False
            if int_item < 0 or int_item > 255:
                return False
        return True

    @staticmethod
    def split_address(address):
        result = []
        s = ''
        tag = 0
        for a in address:
            if a == '\t':
                if tag:
                    s = ''
                    tag = 0
                else:
                    result.append(s)
                    s = ''
                    tag = 1
            else:
                tag = 0
                s += a
        result.append(s)
        return result

    @staticmethod
    def locate_ip(ip, default=u'unknown'):

        if not IpSource.is_ipv4(ip):
            return default, default, default

        try:
            address = IPX.find(ip)
        except Exception:
            logger.exception(u'根据IP获取城市失败 IP:[%s]', ip)
            address = ""

        if address:
            address_parts = IpSource.split_address(address)
            if address_parts[0] == u'中国':
                province = address_parts[1]
                city = address_parts[2]
                operator = address_parts[-9]
            else:
                province = address_parts[0]
                city = ''
                operator = ''
        else:
            province = ''
            city = ''
            operator = ''

        if city:
            return city, province, operator
        elif not province or province in (u'本机地址', u'局域网', u'N/A'):
            return default, default, default
        else:
            return city, province, operator
