# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usr', '0005_auto_20150818_2215'),
    ]

    operations = [
        migrations.AddField(
            model_name='appnotifications',
            name='accepted_offer',
            field=models.BooleanField(default=True, verbose_name='One of your offers has been accepted'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='emailnotifications',
            name='accepted_offer',
            field=models.BooleanField(default=True, verbose_name='One of your offers has been accepted'),
            preserve_default=True,
        ),
    ]
