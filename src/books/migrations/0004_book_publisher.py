# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_remove_book_publisher'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='publisher',
            field=models.ManyToManyField(to='books.Publisher', null=True, blank=True),
            preserve_default=True,
        ),
    ]
