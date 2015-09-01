# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usr', '0003_auto_20150812_2122'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailNotifications',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('my_book_new_offer', models.BooleanField(default=True, verbose_name='One of my books has a new offer')),
                ('other_user_highest_offer', models.BooleanField(default=True, verbose_name='Someone offered a higher price for a book than me')),
                ('interesting_book_uploaded', models.BooleanField(default=True, verbose_name='A book that might be of my interest has been uploaded')),
                ('my_book_finalised_by_buyer', models.BooleanField(default=True, verbose_name='A book that I have sold has been finalised by the buyer')),
                ('new_message', models.BooleanField(default=True, verbose_name='I received a new message')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('my_book_new_offer', models.BooleanField(default=True, verbose_name='One of my books has a new offer')),
                ('other_user_highest_offer', models.BooleanField(default=True, verbose_name='Someone offered a higher price for a book than me')),
                ('interesting_book_uploaded', models.BooleanField(default=True, verbose_name='A book that might be of my interest has been uploaded')),
                ('my_book_finalised_by_buyer', models.BooleanField(default=True, verbose_name='A book that I have sold has been finalised by the buyer')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
