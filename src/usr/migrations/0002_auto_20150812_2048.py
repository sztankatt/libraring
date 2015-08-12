# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import location_field.models.plain


class Migration(migrations.Migration):

    dependencies = [
        ('usr', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='institution',
            name='city',
            field=models.CharField(default='Cambridge', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='person',
            name='city',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='institution',
            name='location',
            field=location_field.models.plain.PlainLocationField(max_length=63),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='person',
            name='location',
            field=location_field.models.plain.PlainLocationField(max_length=63),
            preserve_default=True,
        ),
        migrations.DeleteModel(
            name='Location',
        ),
    ]
