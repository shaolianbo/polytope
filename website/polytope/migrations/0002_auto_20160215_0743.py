# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polytope', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='statistics',
            old_name='index',
            new_name='index_str',
        ),
        migrations.AddField(
            model_name='statistics',
            name='addup_count',
            field=models.IntegerField(default=0, verbose_name='\u6837\u672c\u4e2a\u6570'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='statistics',
            unique_together=set([('time_type', 'time', 'index_str')]),
        ),
    ]
