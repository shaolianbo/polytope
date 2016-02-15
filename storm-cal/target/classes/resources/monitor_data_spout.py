# coding: utf-8
from time import time, sleep

from storm import Spout, emit


class MonitorDataSpout(Spout):
    def nextTuple(self):
        sleep(0.5)
        t = time()
        emit([t, 'testing'])
        with open('/root/logs/result.txt', 'a') as f:
            f.write("%s\n" % t)


MonitorDataSpout().run()
