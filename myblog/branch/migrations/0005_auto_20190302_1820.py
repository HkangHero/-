# Generated by Django 2.0.5 on 2019-03-02 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branch', '0004_bill_number_peoplr'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cash',
            fields=[
                ('ud', models.AutoField(primary_key=True, serialize=False)),
                ('cid', models.CharField(max_length=5)),
                ('student_id', models.CharField(max_length=16)),
            ],
        ),
        migrations.AlterField(
            model_name='bill',
            name='number_peoplr',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='bill',
            name='peoples',
            field=models.IntegerField(),
        ),
    ]
