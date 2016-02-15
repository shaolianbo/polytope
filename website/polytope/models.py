# coding: utf-8
from __future__ import unicode_literals

from django.db import models
import jsonfield


HOUR = 1
DAY = 2
TIME_TYPE_CHOICE = {
    HOUR: "小时",
    DAY: "天"
}

DETAIL_INDEX = 1
COMBINE_INDEX = 2
INDEX_TYPE = {
    DETAIL_INDEX: "详细索引",
    COMBINE_INDEX: "有组合字段的索引"
}


# Create your models here.
class Statistics(models.Model):

    time_type = models.IntegerField(choices=TIME_TYPE_CHOICE.items(), blank=False, verbose_name='时间类型')
    time = models.DateTimeField(blank=False, verbose_name='时间')
    index_type = models.IntegerField(choices=INDEX_TYPE.items(), blank=False, verbose_name='索引类型')
    index_str = models.CharField(max_length=100, blank=False, verbose_name='索引')
    average = jsonfield.JSONField(blank=True, verbose_name='平均数')
    distribute = jsonfield.JSONField(blank=True, verbose_name='分布')
    count = jsonfield.JSONField(blank=True, verbose_name='各个统计值的个数')
    addup_count = models.IntegerField(blank=False, default=0, verbose_name='样本个数')

    def __unicode__(self):
        return "%s-%s-%s" % (self.time_type, self.time, self.index)

    class Meta:
        verbose_name = verbose_name_plural = '监控数据统计结果'
        unique_together = ('time_type', 'time', 'index_str')
