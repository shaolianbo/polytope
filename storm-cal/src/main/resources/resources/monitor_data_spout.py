# coding: utf-8
import sys

from storm import Spout, emit
from models.record import RecordIndex, PerformanceData
from spout import FileSpout as DataSpout


def generate_tuple(raw_index, raw_data):
    indexes = RecordIndex.make_index(**raw_index)
    performance_data = PerformanceData.get_performance_data(raw_data)
    for index in indexes:
        yield [index, performance_data]


class MonitorDataSpout(Spout):
    def initialize(self, conf, context):
        DataSpout.init()
        self.tuples = []
        super(MonitorDataSpout, self).initialize(conf, context)

    def nextTuple(self):
        if self.tuples:
            emit(self.tuples.pop())
            return
        else:
            end, index, data = DataSpout.read()
            if end:
                sys.exit(0)
            for t in generate_tuple(index, data):
                print t
                self.tuples.append(t)
            emit(self.tuples.pop())
            return


MonitorDataSpout().run()
