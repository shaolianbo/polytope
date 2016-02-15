# coding: utf-8
from storm import BasicBolt


class StoreBolt(BasicBolt):
    def process(self, tuple):
        with open('/root/logs/result.txt', 'a') as f:
            f.write("%s %s %s\n" % (tuple.id, tuple.values[0], tuple.values[1]))


StoreBolt().run()
