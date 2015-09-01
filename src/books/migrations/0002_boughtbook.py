# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import books.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BoughtBook',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_bought', models.DateTimeField(auto_now_add=True)),
                ('accepted_price', books.models.IntegerRangeField()),
                ('book', models.OneToOneField(null=True, to='books.Book')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
