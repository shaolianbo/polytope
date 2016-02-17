# coding: utf-8
from datetime import datetime
import logging


logger = logging.getLogger(__name__)


INDEX_FIELDS = [
    'page', 'area', 'net', 'ad', 'operator'
]

NET_TYPE_NUM_MAP = {
    '1': 'ethernet',
    '2': 'wifi',
    '3': '2g',
    '4': '3g',
    '5': '4g',
    '6': 'unknown'
}

# 网络运营商
OPERATORS = [
    u'电信',  u'联通', u'移动', u'教育网', u'铁通', u'鹏博士'
]

CHINA_PROVINCE_LIST = [
    u'北京',
    u'上海',
    u'天津',
    u'重庆',
    u'黑龙江',
    u'吉林',
    u'辽宁',
    u'内蒙古',
    u'河北',
    u'新疆',
    u'甘肃',
    u'青海',
    u'陕西',
    u'宁夏',
    u'河南',
    u'山东',
    u'山西',
    u'安徽',
    u'湖北',
    u'湖南',
    u'江苏',
    u'四川',
    u'贵州',
    u'云南',
    u'广西',
    u'西藏',
    u'浙江',
    u'江西',
    u'广东',
    u'福建',
    u'台湾',
    u'海南',
    u'香港',
    u'澳门',
]


class RecordIndex(object):
    """
    生成统计结果的索引

    make_index生成索引列表
        eg:
        RecordIndex.make_index(page=1, area=u'北京', net='4g', ad=True, 'operator'=u'移动')
        生成8个索引为：
        [
            "page:1-are:北京-net:4g－ad:True-operator:移动",
            "page:1-are:all-net:4g－ad:True-operator:移动",
            "page:1-are:北京-net:all－ad:True-operator:移动",
            "page:1-are:北京-net:4g－ad:True-operator:all",
            "page:1-are:all-net:all－ad:True-operator:移动",
            "page:1-are:all-net:4g－ad:True-operator:all",
            "page:1-are:北京-net:all－ad:True-operator:all",
            "page:1-are:all-net:all－ad:True-operator:all",
        ]

    使用装饰器hook_process关联字段处理逻辑：
        eg:

        @hook_process('net')
        def process_net(value):
            pass

        net字段使用process_net处理，函数体返回tuple, 表示该字段值可产生的维度
        比如 process_net('4g'), 返回 ['4g', 'all']
        如果字段值不合理抛出ValueError

    """
    province_hash = {p: 1 for p in CHINA_PROVINCE_LIST}
    net_type = NET_TYPE_NUM_MAP.values()
    index_fields = [
        'page', 'area', 'net', 'ad', 'operator'
    ]
    obscure_filed_value = u'all'
    field_process = {
        'page': lambda x: [int(x)],
        'ad': lambda x: [bool(x)],
    }

    @classmethod
    def make_index(cls, **kwargs):
        result = ['']
        for field in cls.index_fields:
            if field not in kwargs:
                return []
            try:
                vs = map(lambda x: "%s:%s" % (field, x), cls.field_process.get(field, lambda x: [x])(kwargs[field]))
            except ValueError:
                return []
            new_result = []
            for s in result:
                for s_part in vs:
                    new_result.append(s and "%s-%s" % (s, s_part) or s_part)
            result = new_result
        return result


def hook_process(field):
    def decorator(func):
        RecordIndex.field_process[field] = func
        return func
    return decorator


@hook_process('area')
def process_area(value):
    if value not in RecordIndex.province_hash:
        return [RecordIndex.obscure_filed_value]
    return value, RecordIndex.obscure_filed_value


@hook_process('net')
def process_net(value):
    if value.isdigit():
        v = NET_TYPE_NUM_MAP.get(value, 'unknown')
    elif value in ('NULL', 'none'):
        v = 'unknown'
    elif value not in RecordIndex.net_type:
        return ValueError('net type value error')
    else:
        v = value
    return v, RecordIndex.obscure_filed_value


@hook_process('operator')
def process_operator(value):
    for operator in OPERATORS:
        if value.find(operator) > -1:
            return operator, RecordIndex.obscure_filed_value
    return [RecordIndex.obscure_filed_value]


class PerformanceData(object):
    fields = ['redirect', 'cache', 'dns', 'tcp', 'firstByte', 'response', 'interactive',
              'domReady', 'firstScreen', 'domComplete', 'blankScreen', 'total',
              'cmImg', 'fImg', 'adImg', 'otherImg', 'sgo']
    max_value = 2000

    @classmethod
    def get_performance_data(cls, msg):
        """
        返回包含各个字段值的扁平字典
        """
        result = {}
        for key in cls.fields:
            value = msg.get(key, None)
            if value is None:
                continue
            try:
                value = float(value)
                if value > cls.max_value or value < 0:
                    continue
            except ValueError:
                continue
            if key in ('domComplete', 'domReady', 'firstScreen', 'interactive', 'total', 'sgo') and value == 0:
                continue
            result[key] = value
        return result


class AddupData(object):
    DATA_DIS = [0, 2, 4, 8, 10, 12, 14, 16, 18, 20, 10000]

    def __init__(self):
        self.sum = {}
        self.dis = {}
        self.count = {}
        self.addup_count = 0
        for field in PerformanceData.fields:
            self.sum[field] = 0.0
            self.count[field] = 0
            dis = {}
            for i in range(1, len(self.DATA_DIS)):
                dis['%s-%s' % (self.DATA_DIS[i-1], self.DATA_DIS[i])] = 0
            self.dis[field] = dis

    def addup(self, performance_data):
        self.addup_count += 1
        for key, value in performance_data.items():
            self.sum[key] += value
            self.count[key] += 1
            for i in range(1, len(self.DATA_DIS)):
                if value < self.DATA_DIS[i]:
                    v_range = "%s-%s" % (self.DATA_DIS[i-1], self.DATA_DIS[i])
                    self.dis[key][v_range] += 1
                    break

    def get_result(self):
        """
        统计结果的格式：
        {
            aver: {  # 平均值
                'total': 11.0,
                'firstScreen': 10.0,
                ...
            },
            dis: {  # 分布百分比
                'total': {
                    '0-1': 10,
                    ...
                }
                ...
            },
            count: { # 总数
                'total': 111111,
                ...
            },
            addup_count: 12345  # 原始数据个数
        }
        """
        aver = {}
        dis = {}
        for key, count in self.count.items():
            if not count:
                aver[key] = 0.0
                dis[key] = []
                continue
            aver[key] = round(self.sum[key] / count, 2)
            dis[key] = {}
            for r, c in self.dis[key].items():
                dis[key][r] = round(float(c) / count * 100,  2)
        result = {
            "aver": aver,
            "dis": dis,
            "count": self.count,
            "addup_count": self.addup_count
        }
        return result


class FinalResult(object):
    store_engine = None

    TIME_HOUR = 1
    TIME_DAY = 2

    INDEX_DETAIL = 1
    INDEX_COMBINE = 2

    @classmethod
    def set_engine(cls, engine):
        cls.store_engine = engine

    def __init__(self):
        self.time_type = 0  # 1: hour, 2: day
        self.time = None
        self.index_type = 0  # 1: 详细索引，2: 组合索引
        self.index = ""
        self.average = {}
        self.distribute = {}
        self.count = {}  # 各监控指标的个数
        self.addup_count = 0  # 整体统计量

    def save(self, time_type, index, addup_data):
        self.time_type = time_type
        now = datetime.now()
        if self.time_type == self.TIME_HOUR:
            self.time = now.strftime('%Y-%m-%d %H:00:00')
        elif self.time_type == self.TIME_HOUR:
            self.time = now.strftime('%Y-%m-%d 00:00:00')
        else:
            logger.error("wrong time type %s", time_type)
            return

        if index.find('all') == -1:
            self.index_type = self.INDEX_DETAIL
        else:
            self.index_type = self.INDEX_COMBINE
        self.index = index

        self.average = addup_data.get('aver', {})
        self.distribute = addup_data.get('dis', {})
        self.count = addup_data.get('count', {})
        self.addup_count = addup_data.get('addup_count', 0)
        self.store_engine.save(self)
