# coding: utf-8
from storm import BasicBolt
from models import engines
from models.record import FinalResult
from settings import STORE_ENGINE


class StoreBolt(BasicBolt):
    def initialize(self, stormconf, context):
        if STORE_ENGINE['engine'] == 'mysql':
            FinalResult.set_engine(engines.MysqlEngine(**STORE_ENGINE['mysql']))
        super(StoreBolt, self).initialize(stormconf, context)

    def process(self, tuple):
        finals = tuple.values[0]
        for index, result in finals.items():
            FinalResult().save(FinalResult.TIME_HOUR, index, result)


def test_store_bolt():
    import json
    from storm import Tuple
    addup_result = json.loads(open('addup_result.txt').read())
    t = Tuple(1, 2, 3, 4, [addup_result])
    store_bolt = StoreBolt()
    store_bolt.initialize(None, None)
    store_bolt.process(t)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == 'test':
            test_store_bolt()
    else:
        StoreBolt().run()
