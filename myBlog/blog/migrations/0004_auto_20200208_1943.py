# Generated by Django 3.0.3 on 2020-02-08 18:43

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_blog_last_edited_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='last_edited_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 8, 18, 43, 48, 273237, tzinfo=utc), verbose_name='Last edited on'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 8, 18, 43, 48, 273237, tzinfo=utc), verbose_name='Date published'),
        ),
    ]
