# coding: utf-8
from storm import BasicBolt, emit


class AddupBolt(BasicBolt):
    def process(self, tuple):
        emit([tuple.values[0], tuple.values[1] + '1'])
        with open('/root/logs/addup.txt', 'a') as f:
            f.write("%s %s %s\n" % (tuple.id, tuple.values[0], tuple.values[1]))


AddupBolt().run()
