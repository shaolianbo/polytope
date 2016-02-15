# coding: utf-8
from storm import BasicBolt, emit


class AddupBolt(BasicBolt):
    def process(self, tuple):
        emit([tuple.values[0], tuple.values[1] + '1'])


AddupBolt().run()
