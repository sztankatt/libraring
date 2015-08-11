# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import books.models
import django_countries.fields
from django.conf import settings
import queued_search.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('edition', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30)])),
                ('publication_year', books.models.IntegerRangeField(help_text=b'YYYY')),
                ('publication_city', models.CharField(max_length=100, null=True, blank=True)),
                ('publication_country', django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
                ('price', books.models.IntegerRangeField(verbose_name=b'Goal price')),
                ('includes_delivery_charges', models.BooleanField(default=False)),
                ('upload_date', models.DateField()),
                ('isbn', models.CharField(max_length=13, null=True, blank=True)),
                ('image', models.ImageField(default=b'books/no_image.png', upload_to=b'books', blank=True)),
                ('short_description', models.TextField(default=b'', blank=True)),
                ('status', models.CharField(default=b'normal', max_length=20, choices=[(b'normal', 'Without offers'), (b'offered', 'With offers present'), (b'selling', 'Has an accepted offer'), (b'finalised', 'Finalised transaction')])),
                ('author', models.ManyToManyField(to='books.Author')),
            ],
            options={
                'ordering': ['-upload_date'],
            },
            bases=(models.Model, queued_search.models.QueuedModel),
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('offered_price', books.models.IntegerRangeField()),
                ('made_time', models.DateTimeField(auto_now=True)),
                ('accepted', models.BooleanField(default=False)),
                ('book', models.ForeignKey(to='books.Book')),
                ('made_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('finalised_by_buyer', models.BooleanField(default=False)),
                ('finalised_by_seller', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TransactionRating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('seller_rating', models.IntegerField(blank=True, null=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('buyer_rating', models.IntegerField(blank=True, null=True, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('buyer', models.ForeignKey(related_name='buyer_transaction_rating', to=settings.AUTH_USER_MODEL)),
                ('seller', models.ForeignKey(related_name='seller_transaction_rating', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WatchList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('added', models.DateTimeField()),
                ('book', models.ForeignKey(to='books.Book')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='transaction',
            name='rating',
            field=models.OneToOneField(null=True, to='books.TransactionRating'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='offer',
            name='transaction',
            field=models.OneToOneField(null=True, to='books.Transaction'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='book',
            name='genre',
            field=models.ManyToManyField(to='books.Genre'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='book',
            name='publisher',
            field=models.ForeignKey(blank=True, to='books.Publisher', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='book',
            name='sold_to',
            field=models.ForeignKey(related_name='bough_book', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='book',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
