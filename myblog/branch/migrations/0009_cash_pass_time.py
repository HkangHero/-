# Generated by Django 2.0.5 on 2019-03-04 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0008_auto_20190303_2027'),
    ]

    operations = [
        migrations.AddField(
            model_name='cash',
            name='pass_time',
            field=models.CharField(default=None, max_length=20),
        ),
    ]
