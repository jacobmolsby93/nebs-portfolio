# Generated by Django 4.0 on 2022-01-04 07:50

import datetime
from django.db import migrations, models
import django.utils.timezone
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_alter_image_alt'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='image',
            options={'ordering': ['-created_on']},
        ),
        migrations.AlterModelOptions(
            name='video',
            options={'ordering': ['-created_on']},
        ),
        migrations.AddField(
            model_name='image',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='video',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2022, 1, 4, 7, 50, 47, 899553, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
