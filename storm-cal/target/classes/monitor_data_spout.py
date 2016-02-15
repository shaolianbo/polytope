# coding: utf-8
from time import time, sleep

from strom import Spout, emit


class MonitorDataSpout(Spout):
    def nextTuple(self):
        emit([time(), 'testing'])
        sleep(1)

MonitorDataSpout().run()
