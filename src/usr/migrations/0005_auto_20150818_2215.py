# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('usr', '0004_emailnotifications_notifications'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppNotifications',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('my_book_new_offer', models.BooleanField(default=True, verbose_name='One of my books has a new offer')),
                ('other_user_highest_offer', models.BooleanField(default=True, verbose_name='Someone offered a higher price for a book than me')),
                ('interesting_book_uploaded', models.BooleanField(default=True, verbose_name='A book that might be of my interest has been uploaded')),
                ('book_finalised_by_other_user', models.BooleanField(default=True, verbose_name='A book that I have sold has been finalised by the buyer')),
                ('user', models.OneToOneField(related_name='app_notifications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.DeleteModel(
            name='Notifications',
        ),
        migrations.RenameField(
            model_name='emailnotifications',
            old_name='my_book_finalised_by_buyer',
            new_name='book_finalised_by_other_user',
        ),
        migrations.AddField(
            model_name='emailnotifications',
            name='user',
            field=models.OneToOneField(related_name='email_notifications', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
