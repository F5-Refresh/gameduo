# Generated by Django 3.2.14 on 2022-07-13 14:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('raid', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='raidhistory',
            name='raid_status',
        ),
    ]