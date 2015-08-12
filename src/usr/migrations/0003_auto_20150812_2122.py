# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usr', '0002_auto_20150812_2048'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='about',
        ),
        migrations.RemoveField(
            model_name='person',
            name='title',
        ),
    ]
