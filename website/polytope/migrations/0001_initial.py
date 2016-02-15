# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import __builtin__
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Statistics',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_type', models.IntegerField(verbose_name='\u65f6\u95f4\u7c7b\u578b', choices=[(1, '\u5c0f\u65f6'), (2, '\u5929')])),
                ('time', models.DateTimeField(verbose_name='\u65f6\u95f4')),
                ('index_type', models.IntegerField(verbose_name='\u7d22\u5f15\u7c7b\u578b', choices=[(1, '\u8be6\u7ec6\u7d22\u5f15'), (2, '\u6709\u7ec4\u5408\u5b57\u6bb5\u7684\u7d22\u5f15')])),
                ('index', models.CharField(max_length=100, verbose_name='\u7d22\u5f15')),
                ('average', jsonfield.fields.JSONField(default=__builtin__.dict, verbose_name='\u5e73\u5747\u6570', blank=True)),
                ('distribute', jsonfield.fields.JSONField(default=__builtin__.dict, verbose_name='\u5206\u5e03', blank=True)),
                ('count', jsonfield.fields.JSONField(default=__builtin__.dict, verbose_name='\u5404\u4e2a\u7edf\u8ba1\u503c\u7684\u4e2a\u6570', blank=True)),
            ],
            options={
                'verbose_name': '\u76d1\u63a7\u6570\u636e\u7edf\u8ba1\u7ed3\u679c',
                'verbose_name_plural': '\u76d1\u63a7\u6570\u636e\u7edf\u8ba1\u7ed3\u679c',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='statistics',
            unique_together=set([('time_type', 'time', 'index')]),
        ),
    ]
