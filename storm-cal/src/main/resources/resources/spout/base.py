# coding: utf-8
class BaseDataSpout(object):
    @classmethod
    def init(cls, *args, **kwargs):
        pass

    @classmethod
    def read(cls):
        """
        返回值： (bool, {}, {})

        第一个布尔值表示是否读完数据
        第二个字典数据为返回的索引数据
        第三个字典数据为统计数据
        """
        pass

    @classmethod
    def close(cls):
        pass
