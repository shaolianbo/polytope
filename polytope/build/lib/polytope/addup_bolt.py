# coding: utf-8
from datetime import datetime

from storm import BasicBolt, emit, Tuple
from models.record import AddupData


class AddupBolt(BasicBolt):
    def initialize(self, stormconf, context):
        self.start_time = datetime.now().hour
        self.addup_target = {}
        super(AddupBolt, self).initialize(stormconf, context)

    def process(self, tuple, is_emit=False):
        key = tuple.values[0]
        if key not in self.addup_target:
            self.addup_target[key] = AddupData()
        self.addup_target[key].addup(tuple.values[1])
        now = datetime.now()
        if now.hour != self.start_time or is_emit:
            result = {}
            for index, data in self.addup_target.items():
                result[index] = data.get_result()
            emit([result])
            self.start_time = now.hour
            self.addup_target = {}


def test_addup_bolt():
    index = u'page:1-area:湖北-net:unknown-ad:True-operator:移动'
    data = {
        'adImg': 7.884,
        'blankScreen': 2.146,
        'cache': 0.081,
        'cmImg': 8.697,
        'dns': 0.0,
        'domComplete': 15.014,
        'domReady': 6.951,
        'firstByte': 0.902,
        'firstScreen': 9.325,
        'interactive': 6.95,
        'redirect': 0.0,
        'response': 0.504,
        'sgo': 4.822,
        'tcp': 1.066,
        'total': 17.163
    }
    t = Tuple(1, 2, 3, 4, [index, data])
    addup = AddupBolt()
    addup.initialize(None, None)
    addup.process(t)
    addup.process(t)
    addup.process(t, True)


def run():
    AddupBolt().run()


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == 'test':
            test_addup_bolt()
    else:
        AddupBolt().run()
