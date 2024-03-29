# Generated by Django 3.2.16 on 2023-05-29 17:00

import datetime

from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20230528_2051'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-pub_date'], 'verbose_name': 'публикация', 'verbose_name_plural': 'Публикации'},
        ),
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, default=datetime.datetime(2023, 5, 29, 17, 0, 26, 30353, tzinfo=utc), upload_to='posts_images', verbose_name='Фото'),
            preserve_default=False,
        ),
    ]
