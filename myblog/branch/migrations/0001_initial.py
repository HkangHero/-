# Generated by Django 2.0.5 on 2019-02-16 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Master',
            fields=[
                ('username', models.CharField(max_length=12, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Students',
            fields=[
                ('student_id', models.CharField(max_length=12, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=16)),
                ('photo', models.CharField(default=None, max_length=200, null=True)),
                ('college', models.CharField(max_length=30, null=True)),
                ('major', models.CharField(max_length=20, null=True)),
                ('phone_number', models.CharField(max_length=11, null=True)),
                ('idCard', models.CharField(max_length=19, null=True)),
                ('power', models.CharField(default=0, max_length=2)),
                ('student_token', models.CharField(default=None, max_length=300)),
                ('password', models.CharField(max_length=20)),
                ('Pass', models.CharField(default='未审核', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('teacher_id', models.CharField(max_length=12, primary_key=True, serialize=False)),
                ('teacher_name', models.CharField(max_length=16)),
                ('teacher_work', models.CharField(max_length=10, null=True)),
                ('teacher_token', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='VoluntaryLabor',
            fields=[
                ('ud', models.AutoField(primary_key=True, serialize=False)),
                ('work_id', models.CharField(max_length=12)),
                ('teacher_id', models.CharField(max_length=12)),
                ('date', models.CharField(max_length=10)),
                ('time', models.IntegerField()),
                ('addres', models.CharField(max_length=30)),
            ],
        ),
    ]
