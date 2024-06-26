# Generated by Django 5.0.4 on 2024-04-19 05:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lmsapp', '0003_alter_book_book_add_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='book_pic_url',
            field=models.CharField(default=1, max_length=2000),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='book',
            name='book_add_date',
            field=models.DateField(default=datetime.date(2024, 4, 19)),
        ),
        migrations.AlterField(
            model_name='book',
            name='book_add_time',
            field=models.TimeField(default=datetime.datetime(2024, 4, 19, 5, 43, 59, 327961, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='issueditem',
            name='issue_date',
            field=models.DateField(default=datetime.date(2024, 4, 19)),
        ),
    ]
