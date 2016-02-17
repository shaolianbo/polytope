# coding: utf-8
import sys

from storm import Spout, emit
from settings import SPOUT_ENGINE
from models.record import RecordIndex, PerformanceData
import spout_source


def generate_tuple(raw_index, raw_data):
    indexes = RecordIndex.make_index(**raw_index)
    performance_data = PerformanceData.get_performance_data(raw_data)
    for index in indexes:
        yield [index, performance_data]


class MonitorDataSpout(Spout):
    def initialize(self, conf, context):
        self.spout_source = None
        self.spout_conf = {}

        if SPOUT_ENGINE['engine'] == 'file':
            self.spout_source = spout_source.FileSpout
            self.spout_conf = SPOUT_ENGINE['file']
        if SPOUT_ENGINE['engine'] == 'kafka':
            self.spout_source = spout_source.KafkaSpout
            self.spout_conf = SPOUT_ENGINE['kafka']

        self.spout_source.init(**self.spout_conf)
        self.tuples = []
        super(MonitorDataSpout, self).initialize(conf, context)

    def nextTuple(self):
        if self.tuples:
            emit(self.tuples.pop())
            return
        else:
            end, index, data = self.spout_source.read()
            if end:
                sys.exit(0)
            for t in generate_tuple(index, data):
                print t
                self.tuples.append(t)
            emit(self.tuples.pop())
            return


def run():
    MonitorDataSpout().run()


if __name__ == '__main__':
    run()
